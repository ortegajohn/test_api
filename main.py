from fastapi import FastAPI, Request
import psycopg2
import json
import os
from dotenv import load_dotenv
load_dotenv()

app = FastAPI()
def insert_postgres(json_data):
    # Replace these values with your actual connection details
    conn = psycopg2.connect(
        dbname=os.getenv('DBNAME'),
        user="postgres",
        password=os.getenv('PASSWORD'),
        host=os.getenv('HOST'),  # or your database host
        port=os.getenv('PORT')  # default PostgreSQL port
    )

    cur = conn.cursor()

    # Example JSON data and status
    # json_data = {"message": "Hello, world!", "id": 123}
    status = "pending"

    # Insert data into the table
    cur.execute("""
        INSERT INTO drip (data, status)
        VALUES (%s, %s)
    """, [json.dumps(json_data), status])

    conn.commit()
    print("Row inserted.")

    cur.close()
    conn.close()

@app.get("/get")
async def root():
    return {"message": "Hello World"}

@app.post("/post")
async def read_json(request: Request):
    json_data = await request.json()
    insert_postgres(json_data=json_data)
    return {"received_json": json_data}
