from fastapi import FastAPI, Request, HTTPException, Depends, status
from fastapi.middleware.cors import CORSMiddleware  # Import the CORS middleware
from mangum import Mangum
import uvicorn
from ai import OpenAITrained, OpenAIUntrained, GeminiAI

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],  # Allow both POST and OPTIONS methods
    allow_headers=["*"],
)

@app.post("/openai_basic")
async def openai_basic(request: Request):
    data = await request.json()  # Correct way to access the JSON data
    question = data.get("message")  # Assuming you are sending the message in the "message" field
    ai = OpenAIUntrained()
    response = ai.respond(question)
    return response

@app.post("/openai_trained")
async def openai_trained(request: Request):
    data = await request.json()
    question = data.get("message")
    ai = OpenAITrained()

@app.post("/gemini")
async def gemini(request: Request):
    data = await request.json()
    question = data.get("message")
    ai = GeminiAI()
    return ai.response(question)


handler = Mangum(app)

if __name__ == "__main__":
   uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)