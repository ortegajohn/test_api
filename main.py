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

@app.get("/")
async def root(request: Request):
    json_data = None
    try:
        json_data = await request.json()
    except Exception as e:
        print(e)
    query_params = dict(request.query_params)
    if 'challenge' in query_params.keys():
        return query_params['challenge']
    # return {"message": "Hello World"}
    return_data = {
        "isBase64Encoded": False,
        "statusCode": 200,
        "statusDescription": "200 OK",
        "headers": {
            "Set-cookie": "cookies",
            "Content-Type": "application/json"
        },
        "body": json_data,
        "query": query_params
    }
    return return_data

@app.post("/post")
async def read_json(request: Request):
    json_data = await request.json()
    insert_postgres(json_data=json_data)
    return {"received_json": json_data}
