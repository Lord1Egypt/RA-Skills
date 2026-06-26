# Python Package Compatibility Database for HarmonyOS

This database tracks known compatibility status of popular Python packages on HarmonyOS (OpenHarmony).

## Status Legend

- ✅ **Compatible** - Works without issues
- ⚠️ **Partial** - Works with limitations or warnings
- ❌ **Incompatible** - Does not work
- ❓ **Unknown** - Not yet tested

## Web & HTTP

| Package | Status | Notes |
|---------|--------|-------|
| requests | ✅ | Fully compatible |
| httpx | ✅ | Async support works |
| urllib3 | ✅ | Core library |
| aiohttp | ⚠️ | Async may have issues |
| flask | ✅ | Web server works |
| django | ✅ | Full framework support |
| fastapi | ✅ | Recommended for async |
| tornado | ⚠️ | Some async features limited |
| gunicorn | ❌ | Unix-specific |
| uvicorn | ✅ | ASGI server |

## Data Science

| Package | Status | Notes |
|---------|--------|-------|
| numpy | ✅ | Core numerical ops |
| pandas | ✅ | Data manipulation |
| scipy | ⚠️ | Some modules need BLAS |
| matplotlib | ⚠️ | GUI backends don't work |
| seaborn | ✅ | With matplotlib caveats |
| scikit-learn | ⚠️ | Some estimators need compilation |
| tensorflow | ❌ | No HarmonyOS support |
| pytorch | ❌ | No HarmonyOS support |
| jupyter | ❌ | Web-based, needs server |

## Image Processing

| Package | Status | Notes |
|---------|--------|-------|
| pillow | ✅ | Image ops work |
| opencv-python | ⚠️ | May need system OpenCV |
| scikit-image | ⚠️ | Depends on scipy |
| imageio | ✅ | Pure Python fallback |

## Text & NLP

| Package | Status | Notes |
|---------|--------|-------|
| beautifulsoup4 | ✅ | HTML parsing |
| lxml | ⚠️ | Needs libxml2 |
| nltk | ✅ | NLP toolkit |
| spacy | ⚠️ | Large models may fail |
| transformers | ❌ | Depends on PyTorch/TF |

## Database

| Package | Status | Notes |
|---------|--------|-------|
| sqlite3 | ✅ | Built-in |
| psycopg2 | ⚠️ | Needs PostgreSQL client |
| pymysql | ✅ | Pure Python MySQL |
| sqlalchemy | ✅ | ORM works |
| redis | ✅ | Client works |
| pymongo | ✅ | MongoDB client |

## System & OS

| Package | Status | Notes |
|---------|--------|-------|
| os | ✅ | Built-in |
| sys | ✅ | Built-in |
| pathlib | ✅ | Built-in |
| shutil | ✅ | Built-in |
| subprocess | ⚠️ | Limited on HarmonyOS |
| psutil | ❌ | System-specific |
| pywin32 | ❌ | Windows only |
| python-xlib | ❌ | X11 only |

## Testing

| Package | Status | Notes |
|---------|--------|-------|
| pytest | ✅ | Test framework |
| unittest | ✅ | Built-in |
| nose | ⚠️ | Deprecated |
| coverage | ✅ | Code coverage |
| mock | ✅ | Built-in as unittest.mock |

## Utilities

| Package | Status | Notes |
|---------|--------|-------|
| click | ✅ | CLI framework |
| typer | ✅ | Modern CLI |
| rich | ✅ | Terminal formatting |
| tqdm | ✅ | Progress bars |
| python-dotenv | ✅ | Config management |
| pyyaml | ✅ | YAML parsing |
| toml | ✅ | TOML parsing |
| json | ✅ | Built-in |

## Cryptography

| Package | Status | Notes |
|---------|--------|-------|
| cryptography | ⚠️ | Needs OpenSSL |
| pyopenssl | ⚠️ | Depends on cryptography |
| paramiko | ⚠️ | SSH client works |
| bcrypt | ⚠️ | Needs compilation |
| pyjwt | ✅ | JWT tokens |

## Known Incompatible Packages

### Windows-Specific
- pywin32
- wmi
- pythoncom
- winreg (use registry alternatives)

### macOS-Specific
- applescript
- quartz
- cocoa
- appnope

### Linux/X11-Specific
- python-xlib
- xcb
- dbus-python (use alternatives)

### Heavy Binary Dependencies
- tensorflow
- pytorch
- opencv-python (full version)

## Adding to Database

To report compatibility status:

1. Run the compatibility checker
2. Document test results
3. Note any workarounds
4. Submit to database

## Version Notes

Compatibility may vary by:
- Python version (3.8, 3.9, 3.10, 3.11, 3.12)
- HarmonyOS version (3.x, 4.x, NEXT)
- Device architecture (ARM64, x64)

Always test with your specific environment.
