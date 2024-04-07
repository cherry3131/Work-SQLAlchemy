#product info
#Test Error
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime 

# create the app
app = Flask(__name__)

# close the warning information
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False  

# connect
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://username:password@your_ip:your_port/your_database'


# create the extension
db = SQLAlchemy(app)

# ------Table1
class product_info(db.Model):
    __tablename__ = "product_info"  # table name
    product_id = db.Column(db.Integer ,primary_key=True ,index=True) #auto，primarykey
    name = db.Column(db.String(50), nullable=False)   
    weight = db.Column(db.Integer)
    pxgo_url = db.Column(db.String(100)) # set length
    pxbox_url = db.Column(db.String(100))
    rmart_url = db.Column(db.String(100))
    crf_url = db.Column(db.String(100))


    #------Table2 
class price_record(db.Model):
    __tablename__ = "price_record"  
    update_date = db.Column(db.Date, nullable=False, index=True ,primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('product_info.product_id'), primary_key=True)
    name = db.Column(db.String(50), nullable=False)   
    pxgo_price = db.Column(db.Integer)
    pxbox_price = db.Column(db.Integer)
    rmart_price = db.Column(db.Integer)
    crf_price = db.Column(db.Integer)

#------Table3
class mart(db.Model): 
    __tablename__="mart"
    mart_id = db.Column(db.Integer, primary_key=True, nullable=False)  
    mart_name = db.Column(db.String(20), unique=True)  
    
#------Table4  #user
class users(db.Model):
    __tablename__="users"
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)  
    username = db.Column(db.String(40), index=True) #username，string
    email = db.Column(db.String(100), unique=True, index=True)  # email，Unique
    password_hash = db.Column(db.String(255)) # password，string
    created_at = db.Column(db.DateTime, default= datetime.now) # create_at，DateTime
    updated_at = db.Column(db.DateTime, default= datetime.now, onupdate=datetime.now) # update_at，DateTime型態，user_update_time
    line_id = db.Column(db.String(40),db.ForeignKey('line_users.line_id'))  #according to Line's information, set 33
    
    line_user = db.relationship('line_users', back_populates='user')

#------Table5 
class line_users(db.Model):
    __tablename__="line_users"
    line_id = db.Column(db.String(40),primary_key=True)
    username = db.Column(db.String(40), index=True) # username，string
    email = db.Column(db.String(100), unique=True, index=True)  # email，string，Unique
    password_hash = db.Column(db.String(255)) # password，string
    created_at = db.Column(db.DateTime, default= datetime.now) # create_at，DateTime，regist_time
    updated_at = db.Column(db.DateTime, default= datetime.now, onupdate=datetime.now) # update_at，DateTime，update_time

    user = db.relationship('users', back_populates='line_user')



# use if you need
with app.app_context():
    db.create_all()
    # db.drop_all()   

    # all marts
    all_marts = [
        {"mart_id": 1, "mart_name": "小時達"},
        {"mart_id": 2, "mart_name": "隔日達"},
        {"mart_id": 3, "mart_name": "大潤發"},
        {"mart_id": 4, "mart_name": "家樂福"}
       
    ]
    # sort marts
    sorted_marts = sorted(all_marts, key=lambda x: x["mart_id"])

    # insert marts 
    for mart_data in sorted_marts:
        new_mart = mart(
            mart_id=mart_data["mart_id"],
            mart_name=mart_data["mart_name"]
        )
        db.session.add(new_mart)
    
    db.session.commit()

print('Success!')

#-------------------------------------
#insert productinfo
import re
import os
import csv    
folder_path = r'your_folder_path'


if not os.path.exists(folder_path):
    print(f"folder '{folder_path}' is not exist!")  
    exit()

print(f"folder '{folder_path}' is exist!") 

file_list = os.listdir(folder_path)

# get all the csv file
csv_files = [file for file in file_list if file.lower().endswith('.csv')]

values_list = [] 
total_insert = 0

with app.app_context():
    for csv_file in csv_files:
        file_path = os.path.join(folder_path, csv_file)

        with open(file_path, newline='', encoding='utf-8-sig') as file:
            table = csv.reader(file)
            next(table)  # pass the title
            print(f"loading: {file}")
            rows_insert = 0
            for row in table:
                if row[0] and re.match(r'^\d+$', row[0]): 
                    new_id = product_info(
                        product_id=int(row[0],10),
                        name=row[1],  
                        weight=int(row[2]),                               
                        pxgo_url=row[3],  
                        pxbox_url=row[4],
                        rmart_url=row[5],
                        crf_url=row[6],
                    )
                    db.session.add(new_id)
                    rows_insert += 1

 # commit            
                
            db.session.commit()
            total_insert += rows_insert

# close it
session.close()

print('success insert:', total_insert, 'data')





