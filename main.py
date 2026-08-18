import logging
from contextlib import asynccontextmanager
from pathlib import Path

from fastapi import FastAPI
from app.openapi import custom_openapi
from fastapi.middleware.cors import CORSMiddleware
from langchain_groq import ChatGroq

from app.config import settings
from app.rag_chain import get_embeddings, get_qdrant_client
from app.api import app_state
from app.routes import router


logging.basicConfig(
    level=logging.INFO,
    format="%(levelname)s | %(message)s"
)

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Code before yield runs once when the server starts.

    Code after yield runs once when the server shuts down.

    Expensive objects are loaded here so every request
    can reuse them.
    """

    # Load embedding model
    logger.info("Loading embedding model...")

    app_state["embeddings"] = get_embeddings(
        settings.embedding_provider
    )

    # Connect to Qdrant
    logger.info("Connecting to Qdrant...")

    app_state["qdrant_client"] = get_qdrant_client(
        settings.qdrant_url,
        settings.qdrant_api_key
    )

    # Connect to Groq LLM
    logger.info("Connecting to Groq LLM...")

    app_state["llm"] = ChatGroq(
        model=settings.llm_model,
        temperature=0,
        api_key=settings.groq_api_key,
    )

    # Create upload directory
    Path(settings.upload_dir).mkdir(
        parents=True,
        exist_ok=True
    )

    logger.info(
        f"Ready | embeddings={settings.embedding_provider} "
        f"| collection={settings.qdrant_collection}"
    )

    # Server runs here
    yield

    # Shutdown
    app_state.clear()

    logger.info("Server shut down.")


# ─────────────────────────────────────────
# APP
# ─────────────────────────────────────────

app = FastAPI(
    title="RAG API — Lecture 17",
    description="Upload files → Ask questions → Get answers with exact source references",
    version="1.0.0",
    lifespan=lifespan,
)
app.openapi = lambda: custom_openapi(app)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)


# Routes
app.include_router(router)


# ─────────────────────────────────────────
# ENTRY POINT
# ─────────────────────────────────────────

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )


