import pymysql

db = pymysql.connect(host='masterpasswordvault.cwhx4xtc0ihm.us-east-1.rds.amazonaws.com', port=3306, user='admin', password='Team404error')
cursor = db.cursor()

# cursor.execute("CREATE DATABASE masterpasswordvault")
# cursor.execute("SHOW DATABASES")

# for x in cursor:
#     print(x)

cursor.execute("USE masterpasswordvault")
cursor.execute("DROP TABLE school")
cursor.execute("SHOW TABLES")

for y in cursor:
    print(y)
