from fastapi import FastAPI

app = FastAPI(title="Task Hub API")

@app.get("/")

def health_check():
    return {"status": "ok"}
