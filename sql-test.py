from tokenize import Special
import pymysql

db = pymysql.connect(host='masterpasswordvault.cwhx4xtc0ihm.us-east-1.rds.amazonaws.com', port=3306, user='admin', password='Team404error')
cursor = db.cursor()

# cursor.execute("CREATE DATABASE masterpasswordvault")
# cursor.execute("SHOW DATABASES")

# for x in cursor:
#     print(x)

cursor.execute("USE masterpasswordvault")

vaultName = "osu"
service = "linkedin"
username = "spotify"
password = "ringel"
cursor.execute("DROP TABLE buckeye")
# cursor.execute("CREATE TABLE " + vaultName + " (SERVICE VARCHAR(32), USERNAME VARCHAR(32), PASSWORD VARCHAR(32))")


# goToVault = ask_utils.request_util.get_slot_value(handler_input, "vaultName")
# getService = ask_utils.request_util.get_slot_value(handler_input, "service")

# getSQL = "SELECT USERNAME FROM " + vaultName + " WHERE SERVICE=%s"

# cursor.execute(getSQL, (service))
# speak_output = "The Username is " + cursor.fetchone()[0]

# getSQLPass = "SELECT PASSWORD FROM " + vaultName + " WHERE SERVICE=%s"

# cursor.execute(getSQLPass, (service))
# speak_output = speak_output + ", and the Password is " + cursor.fetchone()[0]

# print(speak_output)

# sql = "INSERT INTO " + vaultName + " (SERVICE, USERNAME, PASSWORD) VALUES (%s, %s, %s)"

# cursor.execute(sql, (service,username,password))

# cursor.execute("SELECT * from school")

# for x in cursor:
#     print(x)

# deleteSQL = "UPDATE " + vaultName + " SET SERVICE=%s WHERE SERVICE=%s"

# cursor.execute(deleteSQL, (service,username))

cursor.execute("SELECT * from osu")

# cursor.execute("EXPLAIN school")

# cursor.execute("SHOW TABLES")

for y in cursor:
    print(y)
