from mysql.connector import connection

def create_con():
    cnx = connection.MySQLConnection(user='bb9ec0ae9cfec0', password='68704f35',
                              host='us-cdbr-east-03.cleardb.com',
                              database='heroku_4039ed9669d1447',
                              use_pure=False)
    return cnx

cnx = create_con()
cursor = cnx.cursor()

#cursor.execute("CREATE TABLE IDs (ID_RT INT, ID_REPLY INT, nome VARCHAR(10))")
#cursor.execute("DROP TABLE IDs")
#me) VALUES (666, 123, 'IDs')")
cursor.execute("SELECT * FROM IDs")
id = cursor.fetchall()
#cursor.execute("ALTER TABLE IDs MODIFY ID_RT BIGINT")
#cursor.execute(f"UPDATE IDs SET ID_REPLY = 1435609464569221119 WHERE nome = 'IDs'")
print(id)

cnx.commit()

cursor.close()
cnx.close()
