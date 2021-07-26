import requests
import psycopg2

with requests.get("http://127.0.0.1:5000/very_large_request/100", stream=True) as r:
     ''' change the last digits on the link to change the number of generated rows'''

     conn = psycopg2.connect(dbname="stream_test",
                            user="postgres",
                            password="postgres") # connecting to the database

     cur = conn.cursor()
     sql = "INSERT INTO transactions (txid, uid, amount) VALUES (%s, %s, %s)"

     buffer = ""
     for chunk in r.iter_content(chunk_size=1):
         '''The for loop iterates over the response data and inserts each row into the table'''

        if chunk.endswith(b'\n'):
            t = eval(buffer)
            print(t)
            cur.execute(sql, (t[0], t[1], t[2]))
            conn.commit()
            buffer = ""
        else:
            buffer += chunk.decode()