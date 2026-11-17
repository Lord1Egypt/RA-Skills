"""Shared constants and path resolution for the youcam_core scripts.

Layout of a skill:

  skills/<skill-name>/
  ├── SKILL.md
  ├── credentials.example.json   # template for credentials.json
  ├── credentials.json           # CREDENTIALS_FILE (user-provided)
  └── scripts/                   # SKILL_SCRIPT_ROOT (this file's folder)
      ├── constants.py, youcam_api.py, ...
      ├── api-fallback.yaml      # API_FALLBACK_DOC
      ├── requirements.txt       # REQUIREMENTS_FILE
      └── .venv/                 # VENV_DIR

Every path the scripts use resolves inside `SKILL_SCRIPT_ROOT`, except credentials.json, which lives
one level up in the skill root so users edit it next to SKILL.md rather than inside the vendored code.
"""

import os

SKILL_SCRIPT_ROOT = os.path.dirname(os.path.abspath(__file__))
API_FALLBACK_DOC = os.path.join(SKILL_SCRIPT_ROOT, "api-fallback.yaml")
CREDENTIALS_FILE = os.path.join(os.path.dirname(SKILL_SCRIPT_ROOT), "credentials.json")

# Install dependencies into a local virtual environment in the skill script folder.
VENV_DIR = os.path.join(SKILL_SCRIPT_ROOT, ".venv")
REQUIREMENTS_FILE = os.path.join(SKILL_SCRIPT_ROOT, "requirements.txt")

TASK_STATUS = {"success", "error"}
SUPPORT_FILE_TYPES = {".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".png": "image/png", ".mp4": "video/mp4"}

REQUEST_TIMEOUT = 30  # seconds, for quick metadata/task status calls
UPLOAD_TIMEOUT = 300  # seconds, for the actual file PUT
DEFAULT_POLL_INTERVAL = 5.0
DEFAULT_MAX_POLLS = 20

DEFAULT_API_BALANCE_PATH = "/s2s/v1.0/client/credit"
DEFAULT_API_FEAT_COST_PATH = "/s2s/v2.0/credit/feature-cost"
DEFAULT_UPLOAD_PATH = "/s2s/v2.0/file"
