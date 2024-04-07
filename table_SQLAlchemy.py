#商品資訊
#Test Error
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime #因usertable使用 db.DateTime

# create the app
app = Flask(__name__)

# 關掉警告訊息
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# 連結
# app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:password@34.172.156.246:3306/gcpproject'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://user1:password@34.172.156.246:3306/Test'


# create the extension
db = SQLAlchemy(app)

# ------Table1
class product_info(db.Model):
    __tablename__ = "product_info"  #記得改table名稱
    product_id = db.Column(db.Integer ,primary_key=True ,index=True) #設定自動產生，並為primarykey
    name = db.Column(db.String(50), nullable=False)   
    weight = db.Column(db.Integer)
    pxgo_url = db.Column(db.String(100))
    pxbox_url = db.Column(db.String(100))
    rmart_url = db.Column(db.String(100))
    crf_url = db.Column(db.String(100))


    #------Table2 #假設設計一次列出四個賣場價格，就不太需要primary?
class price_record(db.Model):
    __tablename__ = "price_record"  #記得改table名稱
    update_date = db.Column(db.Date, nullable=False, index=True ,primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_info.product_id'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)   #一般推薦64
    pxgo_price = db.Column(db.Integer)
    pxbox_price = db.Column(db.Integer)
    rmart_price = db.Column(db.Integer)
    crf_price = db.Column(db.Integer)

#------Table3
class mart(db.Model):  #存放賣場資訊
    __tablename__="mart"
    mart_id = db.Column(db.Integer, primary_key=True, nullable=False)  #可能要確認id會多長
    mart_name = db.Column(db.String(20), unique=True)  
    
#------Table4  #存放使用者
class users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  #可能要確認id會多長
    username = db.Column(db.String(40), index=True) # username欄位，字串型態
    email = db.Column(db.String(100), unique=True, index=True)  # email欄位，字串型態，設定為Unique，不接受相同的email註冊
    password_hash = db.Column(db.String(255)) # password欄位，字串型態
    created_at = db.Column(db.DateTime, default= datetime.now) # create_at欄位，DateTime型態，用戶註冊時間
    updated_at = db.Column(db.DateTime, default= datetime.now, onupdate=datetime.now) # update_at欄位，DateTime型態，用戶更新資料時間
    line_id = db.Column(db.String(40),db.ForeignKey('line_users.line_id'))  #原本官網設定33
    
    line_user = db.relationship('line_users', back_populates='user')

#------Table5 
class line_users(db.Model):
    __tablename__="line_users"
    line_id = db.Column(db.String(40),primary_key=True)
    username = db.Column(db.String(40), index=True) # username欄位，字串型態
    email = db.Column(db.String(100), unique=True, index=True)  # email欄位，字串型態，設定為Unique，不接受相同的email註冊
    password_hash = db.Column(db.String(255)) # password欄位，字串型態
    created_at = db.Column(db.DateTime, default= datetime.now) # create_at欄位，DateTime型態，用戶註冊時間
    updated_at = db.Column(db.DateTime, default= datetime.now, onupdate=datetime.now) # update_at欄位，DateTime型態，用戶更新資料時間

    user = db.relationship('users', back_populates='line_user')



# 使用時再打開
with app.app_context():
    db.create_all()
    # db.drop_all()   

    # 多個mart，pxgo小時達，pxbox隔日達，rtmart大潤發，crf家樂福
    all_marts = [
        {"mart_id": 1, "mart_name": "小時達"},
        {"mart_id": 2, "mart_name": "隔日達"},
        {"mart_id": 3, "mart_name": "大潤發"},
        {"mart_id": 4, "mart_name": "家樂福"}
       
    ]
    # 按照mart_id做排序
    sorted_marts = sorted(all_marts, key=lambda x: x["mart_id"])

    # 插入Mart資料
    for mart_data in sorted_marts:
        new_mart = mart(
            mart_id=mart_data["mart_id"],
            mart_name=mart_data["mart_name"]
        )
        db.session.add(new_mart)
    
    db.session.commit()

print('執行成功')

#====================================================================
#插入productinfo資料
import re
import os
import csv    
folder_path = r'D:\01_Taipei_AI\52_ProjectTest\Documents\productinfo'


if not os.path.exists(folder_path):
    print(f"資料夾 '{folder_path}' 不存在!")  #當指定資料夾不存在時，仍舊印出來，mark掉直接不顯示
    exit()

print(f"資料夾 '{folder_path}' 存在!") #有指定資料夾時會印出來

file_list = os.listdir(folder_path)

# 從資料夾過濾，副檔名要是csv檔案
csv_files = [file for file in file_list if file.lower().endswith('.csv')]

values_list = [] 
total_insert = 0

with app.app_context():
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)

        with open(file_path, newline='', encoding='utf-8-sig') as file:
            table = csv.reader(file)
            next(table)  # 跳过第一行，CSV 标题行
            print(f"處理檔案: {file}")
            rows_insert = 0
            for row in table:
                if row[0] and re.match(r'^\d+$', row[0]): 
                    new_id = product_info(
                        product_id=int(row[0],10),
                        name=row[1],  #根據csv調整
                        weight=int(row[2]),                               
                        pxgo_url=row[3],  
                        pxbox_url=row[4],
                        rmart_url=row[5],
                        crf_url=row[6],
                    )
                    db.session.add(new_id)
                    rows_insert += 1

 # 提交資料            
                
            db.session.commit()
            total_insert += rows_insert

# 關閉連接
# session.close()

print('成功插入', total_insert, '個 CSV 文件的數據')


#=======================================================



