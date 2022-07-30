import os, sys, fitz, shutil
from datetime import datetime

class DeleteImage():
    
    # 1時間経過しているかどうかを判断
    def is_past(self, json_time):
        # 現在時刻のdatetimeを取得
        datetime_now = int(datetime.now().timestamp())
        if json_time < datetime_now:
            return True
        else:
            return False
    
    # 削除する関数
    def delete(self, delete_dir):
        shutil.rmtree(delete_dir)