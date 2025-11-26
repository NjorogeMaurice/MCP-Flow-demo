

---

# Building a Simple MCP Flow Using the Python SDK

*A complete beginner-friendly, step-by-step guide*

## What You Will Build

By the end of this tutorial, you will create:

### An MCP **Server** that:

* Exposes a simple `add(a, b)` tool
* Provides a dynamic greeting resource (`greeting://{name}`)
* Includes a simple prompt (`greet_user`)
* Runs using the **Streamable-HTTP** transport

### An MCP **Client** that:

* Connects to the server
* Lists tools
* Calls the `add` tool
* Retrieves a greeting resource
* Calls a prompt

---

# 1. Prerequisites

Ensure you have:

* **Python 3.10+**
* **pip** or **uv** (repo recommends uv)
* A terminal (PowerShell / bash)

---

# 2. Create Your Project & Install the SDK

### **Option A — Using pip**

```bash
python -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate       # Windows

pip install "mcp[cli]"
```

### **Option B — Using uv (recommended)**

```bash
pip install uv
uv init mcp-demo
cd mcp-demo
uv add "mcp[cli]"
```

---

# 3. Create the MCP Server

Create a new file named **`mcp_server.py`**:

```python
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("Demo", json_response=True)

# 1) Tool: Add two numbers
@mcp.tool()
def add(a: int, b: int) -> int:
    return a + b

# 2) Resource: Dynamic greeting
@mcp.resource("greeting://{name}")
def get_greeting(name: str) -> str:
    return f"Hello, {name}!"

# 3) Prompt: Greeting generator
@mcp.prompt()
def greet_user(name: str, style: str = "friendly") -> str:
    styles = {
        "friendly": "Please write a warm, friendly greeting",
        "formal": "Please write a formal, professional greeting",
        "casual": "Please write a casual, relaxed greeting",
    }
    return f"{styles.get(style, styles['friendly'])} for someone named {name}."

if __name__ == "__main__":
    mcp.run(transport="streamable-http")
```

---

# 4. Run Your MCP Server

Run the server in your terminal:

```bash
python mcp_server.py
```

Or if using uv:

```bash
uv run mcp_server.py
```

You should see output indicating the MCP endpoint, usually:

```
http://localhost:8000/mcp
```

---

# 5. Create the MCP Client

Create a new file named **`mcp_client.py`**:

```python
import asyncio
from pydantic import AnyUrl
from mcp import ClientSession, types
from mcp.client.streamable_http import streamable_http_client

async def run():
    server_url = "http://localhost:8000/mcp"

    params = types.ClientParameters(url=AnyUrl(url=server_url))
    async with ClientSession(params=params) as session:
        async with streamable_http_client(session) as client:

            # List available tools
            tools = await client.list_tools()
            print("Tools:", [t.name for t in tools.items])

            # Call the add tool
            result = await client.call_tool("add", {"a": 5, "b": 7})
            print("add(5,7) ->", result.result)

            # Fetch a greeting resource
            resource = await client.get_resource("greeting://Alice")
            print("resource:", resource.data)

            # Request prompt output
            prompt_out = await client.call_prompt("greet_user", {"name": "Bob", "style": "casual"})
            print("Prompt response:", prompt_out.response)

if __name__ == "__main__":
    asyncio.run(run())
```

---

# 6. Run the Client

```bash
python mcp_client.py
```

Expected output:

```
Tools: ['add']
add(5,7) -> 12
resource: Hello, Alice!
Prompt response: <generated text>
```

---


# Done!

You now have a working **end-to-end MCP flow**:

| Component       | What it does                                      |
| --------------- | ------------------------------------------------- |
| `mcp_server.py` | Provides tools, resources, and prompts via MCP    |
| `mcp_client.py` | Connects to server and interacts programmatically |
| Transport       | Streamable-HTTP                                   |

