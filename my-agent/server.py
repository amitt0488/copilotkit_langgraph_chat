from fastapi import FastAPI, HTTPException, UploadFile, File

from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
from copilotkit.integrations.fastapi import add_fastapi_endpoint
from copilotkit import CopilotKitRemoteEndpoint, LangGraphAgent

from io import BytesIO
import os
from dotenv import load_dotenv


app = FastAPI(title="FastAPI CopilotKit LangGraph Server")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["POST", "GET"],
    allow_headers=["*"],
)

# Initialize the CopilotKit SDK
from agent import graph
sdk = CopilotKitRemoteEndpoint(
    agents=[
        LangGraphAgent(
            name="agent",
            description="An example agent to use as a starting point for your own agent.",
            graph=graph,
        )
    ],
    actions=[],
)
add_fastapi_endpoint(app, sdk, "/copilotkit_remote", max_workers=10)


# Load environment variables
load_dotenv()


def main():
    """Run the uvicorn server."""
    import uvicorn
    uvicorn.run("server:app", host="0.0.0.0", port=8000, reload=True)
 
if __name__ == "__main__":
    main()

