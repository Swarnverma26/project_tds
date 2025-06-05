"""
Virtual Teaching Assistant for IIT Madras Data Science Course
FastAPI application with discourse scraping, embeddings, and Q&A capabilities
"""

from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse
import uvicorn
import logging
from typing import Optional
import base64
import io
from PIL import Image

from app.models.requests import QuestionRequest, QuestionResponse
from app.services.qa_service import QAService
from app.services.ocr_service import OCRService
from app.utils.config import settings

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="TDS Virtual Teaching Assistant",
    description="AI-powered Q&A system for IIT Madras Data Science course",
    version="1.0.0"
)

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount static files
app.mount("/static", StaticFiles(directory="frontend"), name="static")

# Initialize services
qa_service = QAService()
ocr_service = OCRService()

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Serve the frontend HTML"""
    try:
        with open("frontend/index.html", "r") as f:
            return HTMLResponse(content=f.read(), status_code=200)
    except FileNotFoundError:
        return HTMLResponse(
            content="<h1>TDS Virtual TA API</h1><p>Frontend not found. API is running at /docs</p>",
            status_code=200
        )

@app.post("/api/", response_model=QuestionResponse)
async def answer_question(
    question: str = Form(...),
    image: Optional[UploadFile] = File(None)
):
    """
    Main endpoint for answering questions with optional image input
    """
    try:
        final_question = question

        # Process image if provided
        if image:
            logger.info(f"Processing image: {image.filename}")

            # Read image content
            image_content = await image.read()
            image_base64 = base64.b64encode(image_content).decode('utf-8')

            # Extract text using OCR
            extracted_text = await ocr_service.extract_text_from_image(image_base64)

            if extracted_text.strip():
                final_question = f"{question}\n\nExtracted from image: {extracted_text}"
                logger.info(f"Extracted text: {extracted_text[:100]}...")

        # Get answer from QA service
        response = await qa_service.get_answer(final_question)

        return QuestionResponse(
            question=final_question,
            answer=response["answer"],
            sources=response["sources"],
            confidence=response["confidence"]
        )

    except Exception as e:
        logger.error(f"Error processing question: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "TDS Virtual TA"}

@app.get("/stats")
async def get_stats():
    """Get system statistics"""
    try:
        stats = await qa_service.get_stats()
        return stats
    except Exception as e:
        logger.error(f"Error getting stats: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
