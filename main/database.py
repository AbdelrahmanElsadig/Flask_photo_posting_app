import psycopg2
import yaml
with open('db.yaml') as file:
    global db_info
    db_info = yaml.safe_load(file)
db = psycopg2.connect(
    host = db_info['hostname'],
    dbname = db_info['database'],
    user = db_info['username'],
    password = db_info['password'],
    port = db_info['port']
)
db.autocommit = True
db.set_session(autocommit=True)

