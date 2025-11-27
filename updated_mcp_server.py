from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from fastapi_mcp import FastApiMCP
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="FastAPI MCP Example")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ----------------------------
# RESOURCE: Read text file
# ----------------------------

TEXT_FILE_PATH = "data/message.txt"

@app.get("/read-text", operation_id="read_text", summary="Read a text file")
async def read_text():
    """
    MCP Resource:
    Reads the content of a local .txt file and returns it.
    GET endpoints become MCP resources.
    """
    if not os.path.exists(TEXT_FILE_PATH):
        raise HTTPException(status_code=404, detail="Text file not found")

    with open(TEXT_FILE_PATH, "r", encoding="utf-8") as f:
        content = f.read()

    return {
        "filename": TEXT_FILE_PATH,
        "content": content
    }


# ----------------------------
# TOOL: Multiply two numbers
# ----------------------------

class MultiplyRequest(BaseModel):
    x: float
    y: float

class MultiplyResponse(BaseModel):
    x: float
    y: float
    product: float

@app.post("/multiply", operation_id="multiply_numbers", response_model=MultiplyResponse, summary="Multiply two numbers")
async def multiply(body: MultiplyRequest):
    """
    MCP Tool:
    POST endpoints become MCP tools.
    """
    return {
        "x": body.x,
        "y": body.y,
        "product": body.x * body.y
    }


# ----------------------------
# MOUNT MCP
# ----------------------------

mcp = FastApiMCP(
    app,
    name="FastAPI MCP Server",
    description="Demo app with one MCP resource and one tool"
)
mcp.mount() 


# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "FastAPI-MCP server is running",
        "resource": "/read-text",
        "tool": "/multiply",
        "mcp": "/mcp"
    }
