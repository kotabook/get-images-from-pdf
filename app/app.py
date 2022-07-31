import os
import werkzeug
from flask import Flask, render_template, request
from .pdf_class import CreateData, GetImage, DeleteImage

file_dir  = "/app/app/static"
json_path = "/app/app/image_dir.json"

create_data  = CreateData.CreateData(path=file_dir, json_path=json_path)
get_image    = GetImage.GetImage()
delete_image = DeleteImage.DeleteImage()

# ファイルが正常かどうかを判定する関数
def allowed_file(filename):
    return "." in filename and filename.rsplit('.', 1)[1].lower() in ["pdf"]

#Flaskオブジェクトの生成
app = Flask(__name__)

# 最大容量を指定 (5MB)
app.config['MAX_CONTENT_LENGTH'] = 5 * 1024 * 1024

@app.route("/", methods=["GET", "POST"])

def index():
    # もしPOSTリクエストであれば
    if request.method == "POST": 
        # もしファイルがない場合
        if "uploadFile" not in request.files:
            message = "Error. Please select a PDF file."
            return render_template("index.html", request_type="get", message=message)
        else:
            # pdfファイルとファイル名を取得
            pdf_file = request.files["uploadFile"]
            pdf_filename = pdf_file.filename

            if pdf_filename == "":
                message = "Error. Please select a PDF file."
                return render_template("index.html", request_type="get", message=message)

            # ファイルがpdfである場合、処理を行う
            elif allowed_file(pdf_filename):

                unique_id, images_dir, others_dir = create_data.get_unique_id() # 画像保存先のパスを生成する
                create_data.add_json(unique_id=unique_id) # jsonファイルに情報を保存
                pdf_file.save(os.path.join(others_dir, pdf_filename)) # pdfを保存する

                # try-except文
                try:
                    # pdfをインポート
                    doc = get_image.get_fitz_pdf(pdf_path=f"{others_dir}/{pdf_filename}")
                    # 画像データを取得
                    image_list = get_image.get_image_data(doc)
                except:
                    message = "Error. Could not read PDF file. Please check if it's a PDF file."
                    return render_template("index.html", request_type="get", message=message)

                # ページごとの画像を保存する
                image_path_all_list = []
                for page_num, image in enumerate(image_list):
                    image_path_list = get_image.conduct_image_data(doc=doc, page_num=page_num,image=image, tempolary_dir=images_dir)
                    if image_path_list:
                        image_path_all_list += image_path_list
                if image_path_all_list != []:
                    # 圧縮ファイルのダウンロードパスを作成
                    # root_dir = "{}/{}/images".format(file_dir, unique_id)
                    zip_file_path = "/static/{}/others/download_all.zip".format(unique_id)
                    get_image.create_zip_file(root_dir=images_dir, move_dir=others_dir)
                    return render_template("index.html", request_type="post", image_path_list=image_path_all_list, pdf_filename=pdf_filename, zip_file_path=zip_file_path)
                else:
                    message = "Error. Could not detect image from PDF."
                    return render_template("index.html", request_type="get", message=message)

            else:
                message = "Error. Please select a PDF file."
                return render_template("index.html", request_type="get", message=message)
    
    else: # もしPOSTリクエスト以外であれば
        # ファイルを削除する処理を行う
        json_data = create_data.get_json()
        json_delete_keys = []
        # for文で繰り返し処理を行う
        for i in list(json_data):
            json_time = int(json_data[i])
            # ファイルが保存して1時間経過していれば
            if delete_image.is_past(json_time=json_time):
                # 削除するフォルダのパスを作成
                delete_dir = "{}/{}".format(file_dir, i)
                # フォルダを削除
                delete_image.delete(delete_dir=delete_dir)  
                json_delete_keys.append(i)        
            else:
                break

        # 削除対象があれば削除処理を行う
        if json_delete_keys != []:
            create_data.delete_json(keys=json_delete_keys)
        return render_template("index.html", request_type="get")

# 容量が大きい場合は例外処理を行う
@app.errorhandler(werkzeug.exceptions.RequestEntityTooLarge)
def handle_over_max_file_size(error):
    print("werkzeug.exceptions.RequestEntityTooLarge")
    message = "Error. File is too large. Please keep it under 5 MB."
    return render_template("index.html", request_type="get", message=message)

if __name__ == "__main__":
    app.run()