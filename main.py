from fastapi import FastAPI, Request

app = FastAPI()


@app.get("/get")
async def root():
    return {"message": "Hello World"}

@app.post("/post")
async def read_json(request: Request):
    json_data = await request.json()
    return {"received_json": json_data}
