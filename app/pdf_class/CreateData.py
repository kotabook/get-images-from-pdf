import os, uuid, json
from datetime import datetime, timedelta

class CreateData():
    def __init__(self, path, json_path):
        self.path = path
        self.json_path = json_path

    # uuidを取得して、ディレクトリを作成する関数
    def get_unique_id(self):
        unique_id = uuid.uuid4()
        tempolary_dir = f"{self.path}/{unique_id}"
        os.makedirs(tempolary_dir, exist_ok=True)
        return unique_id, tempolary_dir

    # jsonファイルに保存する関数
    def add_json(self, unique_id):
        # 現在時刻から1時間後のdatetimeを取得
        datetime_after_1h = datetime.now() + timedelta(minutes=10)
        with open(self.json_path) as f:
            json_load = json.load(f)
            json_load[str(unique_id)] = int(datetime_after_1h.timestamp())
        with open(self.json_path, "w") as f:
            json.dump(json_load, f, indent=4)

    # jsonファイルを取得する関数
    def get_json(self):
        with open(self.json_path) as f:
            json_load = json.load(f)
            return json_load
    
    # jsonファイルの要素を削除する関数
    def delete_json(self, keys):
        with open(self.json_path) as f:
            json_load = json.load(f)
            for key in keys:
                del json_load[key]
        with open(self.json_path, "w") as f:
            json.dump(json_load, f, indent=4)
        