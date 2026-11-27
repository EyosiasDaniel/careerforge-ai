import re
import unicodedata
from io import BytesIO

from pypdf import PdfReader

MAX_PAGES = 30
SKILLS = {
    "Python": ("python",), "Java": ("java",), "JavaScript": ("javascript", "js"),
    "TypeScript": ("typescript",), "C++": ("c++",), "C#": ("c#",),
    "SQL": ("sql",), "MySQL": ("mysql",), "PostgreSQL": ("postgresql", "postgres"),
    "FastAPI": ("fastapi",), "Spring Boot": ("spring boot",),
    "Git": ("git",), "GitHub": ("github",), "Docker": ("docker",),
    "Kubernetes": ("kubernetes",), "Linux": ("linux",),
    "AWS": ("aws", "amazon web services"), "Azure": ("azure",),
    "Machine Learning": ("machine learning",), "Deep Learning": ("deep learning",),
    "NLP": ("nlp", "natural language processing"), "PyTorch": ("pytorch",),
    "TensorFlow": ("tensorflow",), "scikit-learn": ("scikit-learn", "sklearn"),
    "Pandas": ("pandas",), "NumPy": ("numpy",), "React": ("react", "react.js"),
    "HTML": ("html",), "CSS": ("css",), "LLM": ("llm", "llms", "large language models"),
    "RAG": ("rag", "retrieval augmented generation", "retrieval-augmented generation"),
}


def preprocess_text(text: str) -> str:
    return " ".join(unicodedata.normalize("NFKC", text).split())


def extract_skills(text: str) -> list[str]:
    text = preprocess_text(text).casefold()
    return sorted(
        name for name, aliases in SKILLS.items()
        if any(re.search(r"(?<![\w+#])" + re.escape(alias) + r"(?![\w+#])", text)
               for alias in aliases)
    )


def parse_pdf(data: bytes) -> tuple[str, int]:
    if not data.startswith(b"%PDF-"):
        raise ValueError("Invalid PDF signature.")
    try:
        reader = PdfReader(BytesIO(data))
        if reader.is_encrypted:
            raise ValueError("Encrypted PDFs are not supported.")
        pages = len(reader.pages)
        if not 1 <= pages <= MAX_PAGES:
            raise ValueError("PDF must contain between 1 and 30 pages.")
        raw = "\n".join(page.extract_text() or "" for page in reader.pages)
    except ValueError:
        raise
    except Exception as exc:
        raise ValueError("Unable to parse PDF.") from exc
    cleaned = preprocess_text(raw)
    if not cleaned:
        raise ValueError("No extractable text found. Scanned PDFs require OCR.")
    return cleaned, pages
