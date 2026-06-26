# Usage Reference

## Install dependencies

From `resources/latex_convert_project/`:

```bash
python3 -m pip install -e .
python3 -m pip install -r services/api/requirements.txt
cd apps/web && npm install
```

Windows users who want Microsoft Word automation need Microsoft Word and `pywin32`. Linux users need LibreOffice for legacy Word conversion and PDF preview.

## Supported inputs and outputs

Inputs: `.doc`, `.docx`, `.wps`.

Output: `.docx` with editable Word OMML equations.

## Conversion engines

- `--engine auto`: Microsoft Word first on macOS/Windows, LibreOffice fallback; LibreOffice on Linux.
- `--engine word`: require Microsoft Word automation.
- `--engine libreoffice`: use LibreOffice only.

## AI configuration

Optional environment file name: `.env`.

Supported keys:

```dotenv
OPENAI_API_KEY=your-api-key-here
OPENAI_BASE_URL=https://api.openai.com/v1
OPENAI_MODEL=gpt-4.1-mini
AI_BATCH_SIZE=10
AI_MAX_WORKERS=5
AI_FAILURE_FALLBACK=rule
```

Use `--no-ai-progress` for quieter CLI logs. Use `--ai-failure-fallback keep` for sensitive documents when failed model calls should preserve source text.
