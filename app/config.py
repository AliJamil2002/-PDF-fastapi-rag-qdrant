from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    # LLM
    groq_api_key: str
    llm_model: str = "openai/gpt-oss-120b"

    # Embedding
    embedding_provider: str = "huggingface"

    # Vector database
    qdrant_url: str
    qdrant_api_key: str
    qdrant_collection: str

    # Upload
    upload_dir: str = "uploads_temp"
    max_upload_size_mb: int = 50

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
