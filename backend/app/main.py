from fastapi import FastAPI

app = FastAPI(
    title="CareerForge AI",
    description="AI-powered career development platform",
    version="0.1.0"
)


@app.get("/")
def root():
    return {
        "application": "CareerForge AI",
        "version": "0.1.0",
        "message": "Welcome to CareerForge AI"
    }


@app.get("/api/v1/health")
def health_check():
    return {
        "status": "healthy",
        "service": "careerforge-backend"
    }