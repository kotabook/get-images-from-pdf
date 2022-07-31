import os, sys, fitz, shutil
from datetime import datetime, timedelta

class GetImage():

    # ファイルを読み込む関数
    def get_fitz_pdf(self, pdf_path):
        return fitz.open(pdf_path)
    
    # 画像データを取得する関数
    def get_image_data(self, doc):
        image_list = []
        for page in range(len(doc)):
            image_list.append(doc[page].get_images())
        return image_list
    
    # 画像情報を順番に処理する関数
    def conduct_image_data(self, doc, page_num, image, tempolary_dir):
        # ページにある画像が1つでもあれば保存処理を行う
        if image != []:
            image_path_list = []
            for i in range(len(image)):
                xref, smask = image[i][:2]
                # 拡張子について場合分け
                if image[i][8] == "FlateDecode":
                    extension = "png"
                elif image[i][8] == "DCTDecode":
                    extension = "jpg"
                else:
                    continue
                # マスク情報の取得と画像の再構築
                pix = fitz.Pixmap(doc.extract_image(xref)["image"])
                if smask > 0:
                    mask = fitz.Pixmap(doc.extract_image(smask)["image"])
                    pix  = fitz.Pixmap(pix, 0) 
                    pix  = fitz.Pixmap(pix, mask)
                # 画像を保存
                image_name = os.path.join(tempolary_dir, "image{}_{}.{}".format(page_num + 1, i + 1, extension))
                pix.save(image_name)
                image_path_list.append("{}/image{}_{}.{}".format(tempolary_dir[9:], page_num + 1, i + 1, extension))
            return image_path_list
        else:
            return False
    
    # zipファイルを作成する関数
    def create_zip_file(self, root_dir, move_dir):
        # zipファイルを作成
        shutil.make_archive("download_all", format="zip", root_dir=root_dir)
        # zipファイルを移動
        shutil.move("/work/get-images-from-pdf/download_all.zip", move_dir)