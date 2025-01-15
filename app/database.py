import psycopg2
from psycopg2.extras import RealDictCursor
from ..constants import HOSTNAME, DATABASE, USER, PASSWORD

try:
    conn = psycopg2.connect(host=HOSTNAME, database=DATABASE, user=USER, password=PASSWORD, 
                            cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("Database Connectioon successful")
except Exception as error:
    print("connection to database failed")
    print("Error: ", error)