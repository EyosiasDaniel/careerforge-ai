# careerforge-ai
AI-powered career development platform featuring resume analysis, semantic job matching, skill gap detection, and intelligent interview preparation.

## Day 3: Resume analysis

From the repository root:

```sh
cd backend
python -m pip install -r requirements.txt
python -m uvicorn app.main:app --reload
```

Open http://127.0.0.1:8000/docs and use POST /api/v1/resumes/analyze with a PDF file.
The response includes filename, page_count, normalized text, and recognized skills.

```sh
python -m pytest -q
```

The endpoint accepts text-based PDFs up to 5 MiB and 30 pages. Scanned and encrypted PDFs are not supported. Skill extraction is dictionary-based and does not infer proficiency or context. Uploaded resumes are not intentionally persisted by the application; the API returns extracted personal text, so use synthetic resumes during development. Before public deployment, add authentication, request-body limits at the proxy, rate limiting and isolated PDF processing.
