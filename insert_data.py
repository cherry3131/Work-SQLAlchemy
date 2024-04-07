
import os
import pymysql
import pandas as pd

# 資料庫連線設定
db_config = {
    "host": "your_host",
    "port": port_number,
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}

# path
folder_path = r'your_folder_path'

# check if the folder exist
if not os.path.exists(folder_path):
    print(f"folder '{folder_path}' is not exist!")
    exit()

print(f"folder '{folder_path}' is exist!")

# get all the csv file
file_list = os.listdir(folder_path)
csv_files = [file for file in file_list if file.lower().endswith('.csv')]

# connection
total_insert = 0  
try:
    connection = pymysql.connect(**db_config)
    try:
        with connection.cursor() as cursor:
            # insert product_info
            sql = """INSERT INTO price_record_re (                    
                    product_id,
                    update_date,
                    pxgo_price,
                    pxbox_price,
                    rmart_price,
                    crf_price)
                    VALUES 
                    (%s, %s, %s, %s, %s, %s)"""
            
            for csv_file in csv_files:
                # read CSV
                csv_path = os.path.join(folder_path, csv_file)
                datas = pd.read_csv(csv_path).drop(["name", "weight"], axis=1)
                
                for i in range(len(datas["id"])):
                    data_to_insert = tuple(datas.iloc[i, x] for x in range(6))
                    # transfer vlaue
                    data_to_insert = tuple(0 if pd.isna(value) or value == "lost" or value == "error" else value for value in data_to_insert)
                    cursor.execute(sql, data_to_insert)
                    total_insert += 1  # count
                    
                connection.commit()
                print(f"insert file: {csv_file}")

    except Exception as e:
        print(e)
    finally:
        connection.close()
except Exception as e:
    print("connect fail")
    print(e)

print(f"total {total_insert}")





