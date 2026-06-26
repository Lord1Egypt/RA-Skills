import hashlib
import json
import re
from pathlib import Path


DEFAULT_REPLAY_FILE = Path.home() / ".openclaw" / "workspace" / ".learnings" / "skill-replay-cases.jsonl"

EMAIL_RE = re.compile(r"\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}\b")
PHONE_RE = re.compile(
    r"(?<!\d)(?:\+\d{1,3}[-.\s])?(?:\(\d{2,4}\)|\d{2,4})[-.\s]\d{2,4}[-.\s]\d{2,4}(?!\d)"
)
IPV4_RE = re.compile(r"\b(?:\d{1,3}\.){3}\d{1,3}\b")
IPV6_RE = re.compile(r"\b(?:[A-Fa-f0-9]{1,4}:){4,7}[A-Fa-f0-9]{1,4}\b")
TELEGRAM_BOT_RE = re.compile(r"\b\d{8,12}:[A-Za-z0-9_\-]{30,}\b")
TOKEN_RE = re.compile(
    r"\b(?:sk|tvly|ntn|xox[baprs]|ghp|github_pat|gho|ghu|ghs|ghr|AKIA|ASIA|AIza)[-_A-Za-z0-9]{12,}\b"
)
JWT_RE = re.compile(r"\beyJ[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\.[A-Za-z0-9_\-]{10,}\b")
PRIVATE_KEY_RE = re.compile(
    r"-----BEGIN [A-Z ]*PRIVATE KEY-----.*?-----END [A-Z ]*PRIVATE KEY-----",
    re.DOTALL,
)
LONG_SECRET_RE = re.compile(r"(?<![A-Za-z0-9_\-/.])[A-Za-z0-9_\-]{40,}(?![A-Za-z0-9_\-/.])")
URL_QUERY_RE = re.compile(r"(https?://[^\s?]+)\?[^\s]+")


def stable_id(*parts: str) -> str:
    digest = hashlib.sha256("\n".join(parts).encode("utf-8")).hexdigest()
    return digest[:16]


def redact_text(text: str) -> str:
    text = PRIVATE_KEY_RE.sub("[REDACTED_PRIVATE_KEY]", text)
    text = EMAIL_RE.sub("[REDACTED_EMAIL]", text)
    text = JWT_RE.sub("[REDACTED_JWT]", text)
    text = TELEGRAM_BOT_RE.sub("[REDACTED_BOT_TOKEN]", text)
    text = TOKEN_RE.sub("[REDACTED_TOKEN]", text)
    text = LONG_SECRET_RE.sub("[REDACTED_SECRET]", text)
    text = URL_QUERY_RE.sub(r"\1?[REDACTED_QUERY]", text)
    text = IPV6_RE.sub("[REDACTED_IPV6]", text)
    text = IPV4_RE.sub("[REDACTED_IPV4]", text)
    text = PHONE_RE.sub(lambda m: "[REDACTED_PHONE]" if sum(c.isdigit() for c in m.group(0)) >= 7 else m.group(0), text)
    return text


def load_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.read_text(encoding="utf-8", errors="ignore").splitlines():
        if not line.strip():
            continue
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue
    return rows


def append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        for row in rows:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_json(path: Path, payload: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
