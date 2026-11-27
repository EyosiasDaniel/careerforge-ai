from io import BytesIO

from fastapi.testclient import TestClient
from pypdf import PdfWriter
from pypdf.generic import (
    DecodedStreamObject, DictionaryObject, NameObject,
)

from app.main import app
from app.resume import extract_skills, preprocess_text

client = TestClient(app)


def sample_pdf(with_text=True):
    writer = PdfWriter()
    page = writer.add_blank_page(width=300, height=300)
    if with_text:
        font = DictionaryObject({
            NameObject("/Type"): NameObject("/Font"),
            NameObject("/Subtype"): NameObject("/Type1"),
            NameObject("/BaseFont"): NameObject("/Helvetica"),
        })
        page[NameObject("/Resources")] = DictionaryObject({
            NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})
        })
        stream = DecodedStreamObject()
        stream.set_data(b"BT /F1 12 Tf 20 200 Td (Python, SQL and C++) Tj ET")
        page[NameObject("/Contents")] = writer._add_object(stream)
    output = BytesIO()
    writer.write(output)
    return output.getvalue()


def upload(data, name="resume.pdf"):
    return client.post("/api/v1/resumes/analyze",
                       files={"file": (name, data, "application/pdf")})


def test_preprocessing():
    assert preprocess_text("Python\n  SQL\t") == "Python SQL"


def test_skills():
    assert extract_skills("JavaScript, Python, python, C++, NLP") == [
        "C++", "JavaScript", "NLP", "Python"
    ]


def test_valid_pdf():
    response = upload(sample_pdf())
    assert response.status_code == 200
    assert response.json()["skills"] == ["C++", "Python", "SQL"]
    assert response.json()["page_count"] == 1


def test_invalid_pdf():
    assert upload(b"not a pdf").status_code == 422


def test_wrong_extension():
    assert upload(b"hello", "resume.txt").status_code == 415


def test_blank_pdf():
    assert upload(sample_pdf(False)).status_code == 422


def test_large_pdf():
    assert upload(b"x" * (5 * 1024 * 1024 + 1)).status_code == 413


def test_missing_file():
    assert client.post("/api/v1/resumes/analyze").status_code == 422
