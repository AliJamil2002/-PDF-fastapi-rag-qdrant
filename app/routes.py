from fastapi import FastAPI,APIRouter
from app.api import (delete_document,health,list_documents,query,upload_files)
from app.models import(DeleteResponse,DocumentListResponse,QueryResponse,UploadResponse)


router=APIRouter()


router.add_api_route("/upload", upload_files,methods=['Post'], response_model=UploadResponse)
router.add_api_route("/query", query, methods=["Post"], response_model=QueryResponse)
router.add_api_route("/documents", list_documents,methods=["Get"],response_model=DocumentListResponse)
router.add_api_route("delete",delete_document,methods=["Delete"],response_model=DeleteResponse)
router.add_api_route("/health",health,methods=["Get"])