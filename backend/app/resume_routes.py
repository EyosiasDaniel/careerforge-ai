from fastapi import APIRouter, File, HTTPException, UploadFile
from pydantic import BaseModel

from .resume import extract_skills, parse_pdf

router = APIRouter(prefix="/api/v1/resumes", tags=["Resumes"])
MAX_BYTES = 5 * 1024 * 1024


class ResumeAnalysis(BaseModel):
    filename: str
    page_count: int
    text: str
    skills: list[str]


@router.post("/analyze", response_model=ResumeAnalysis)
def analyze_resume(file: UploadFile = File(...)):
    try:
        if not (file.filename or "").lower().endswith(".pdf"):
            raise HTTPException(415, "Only PDF files are supported.")
        data = file.file.read(MAX_BYTES + 1)
        if len(data) > MAX_BYTES:
            raise HTTPException(413, "PDF exceeds the 5 MiB limit.")
        try:
            text, pages = parse_pdf(data)
        except ValueError as exc:
            # Avoid exposing internal parser errors to clients.
            message = str(exc)
            if message not in {
                "Invalid PDF signature.", "Encrypted PDFs are not supported.",
                "PDF must contain between 1 and 30 pages.",
                "No extractable text found. Scanned PDFs require OCR.",
            }:
                message = "Unable to parse PDF."
            raise HTTPException(422, message) from exc
        return ResumeAnalysis(filename=file.filename, page_count=pages,
                              text=text, skills=extract_skills(text))
    finally:
        file.file.close()
