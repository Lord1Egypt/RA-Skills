# Python FastAPI Template

When planning a Python web service with FastAPI, ensure the following standards are met:

## Project Structure
- `pyproject.toml` or `requirements.txt` with `fastapi`, `uvicorn`, `pydantic-settings`.
- `main.py`: FastAPI app initialization.
- `api/v1/`: Versioned API routes.
- `core/`: Config and security logic.

## Patterns
- **Pydantic**: Use for all request and response models.
- **Dependencies**: Use `Depends` for DB sessions and authentication.
- **Testing**: Use `httpx` with `pytest` for integration tests.
- **Environment**: Use `pydantic-settings` for `.env` management.

## Code Preview
```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello FastAPI"}
```

---
*Last Updated: 2026-03-06 06:36 UTC*
