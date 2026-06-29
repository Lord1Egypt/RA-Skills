"""
_lib.py — shared helpers for skill-sign (init/sign/verify/export-public).

Keep this lean — it's imported by 4 CLI scripts.
"""

import os
import sys
import json
import base64
import hashlib
from pathlib import Path


# ============================================================
# Paths (XDG Base Directory + cross-platform fallback)
# ============================================================

def config_dir() -> Path:
    """~/.config/skill-sign/ (or $XDG_CONFIG_HOME/skill-sign/)."""
    xdg = os.environ.get("XDG_CONFIG_HOME", "").strip()
    base = Path(xdg) if xdg else Path.home() / ".config"
    d = base / "skill-sign"
    return d


def private_key_path() -> Path:
    return config_dir() / "private.key"


def public_key_path() -> Path:
    return config_dir() / "public.key"


def public_key_txt_path() -> Path:
    """Base64 text version of public.key for easy copy-paste."""
    return config_dir() / "public.key.txt"


def trusted_keys_dir() -> Path:
    """Where users store public keys they trust (one .pub per author)."""
    return config_dir() / "trusted"


# ============================================================
# File I/O with permissions
# ============================================================

def write_secret_file(path: Path, data: bytes) -> None:
    """Write binary data and set chmod 600. Parent dir gets chmod 700."""
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        os.chmod(path.parent, 0o700)
    except OSError:
        pass  # Windows / some FS
    # Atomic write
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "wb") as f:
        f.write(data)
    try:
        os.chmod(tmp, 0o600)
    except OSError:
        pass
    os.replace(tmp, path)


def write_public_file(path: Path, data: bytes) -> None:
    """Write binary data and set chmod 644."""
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    with open(tmp, "wb") as f:
        f.write(data)
    try:
        os.chmod(tmp, 0o644)
    except OSError:
        pass
    os.replace(tmp, path)


def check_private_key_permissions(path: Path) -> str | None:
    """Return warning string if permissions are too loose; None if OK."""
    if not path.exists():
        return None
    try:
        st = os.stat(path)
        mode = st.st_mode & 0o777
        if mode != 0o600:
            return (
                f"⚠️  Private key at {path} has mode {oct(mode)}; "
                f"recommended 0o600. Fix with: chmod 600 {path}"
            )
    except OSError:
        pass
    return None


# ============================================================
# File set walker (what gets hashed)
# ============================================================

EXCLUDE_DIRS = {
    ".git", "__pycache__", "node_modules", ".pytest_cache",
    ".mypy_cache", ".tox", ".venv", "venv",
}
EXCLUDE_FILES = {"sign.key", ".DS_Store"}
EXCLUDE_EXTS = {".pyc", ".pyo", ".bak", ".swp", ".tmp"}


def should_exclude(rel_path: str) -> bool:
    parts = rel_path.replace("\\", "/").split("/")
    for p in parts:
        if p in EXCLUDE_DIRS:
            return True
        if p in EXCLUDE_FILES:
            return True
        if p.startswith("._"):  # macOS metadata
            return True
    _, ext = os.path.splitext(rel_path)
    if ext.lower() in EXCLUDE_EXTS:
        return True
    return False


def collect_files(skill_dir: Path) -> list[str]:
    """Return sorted list of relative paths of files to be hashed."""
    skill_dir = Path(skill_dir).resolve()
    result = []
    for root, dirs, files in os.walk(skill_dir):
        # In-place prune
        dirs[:] = sorted(d for d in dirs if d not in EXCLUDE_DIRS and not d.startswith("._"))
        for fname in sorted(files):
            full = Path(root) / fname
            rel = str(full.relative_to(skill_dir)).replace("\\", "/")
            if not should_exclude(rel):
                result.append(rel)
    return sorted(result)


# ============================================================
# Content hash (streaming, handles large files)
# ============================================================

def compute_content_hash(skill_dir: Path, file_list: list[str]) -> str:
    """SHA-256 over (sorted) [rel_path:content\n] for each file. Streamed."""
    h = hashlib.sha256()
    skill_dir = Path(skill_dir)
    for rel in file_list:
        full = skill_dir / rel
        h.update(rel.encode("utf-8"))
        h.update(b":")
        with open(full, "rb") as f:
            while True:
                chunk = f.read(65536)
                if not chunk:
                    break
                h.update(chunk)
        h.update(b"\n")
    return "sha256:" + h.hexdigest()


# ============================================================
# Key serialization (base64 short-form for human use)
# ============================================================

def encode_pubkey(pubkey_bytes: bytes) -> str:
    """ed25519:base64nopad — short form for SKILL.md / sign.key embedding."""
    b64 = base64.b64encode(pubkey_bytes).decode("ascii").rstrip("=")
    return "ed25519:" + b64


def decode_pubkey(s: str) -> bytes:
    """Parse ed25519:base64 form. Accepts with/without padding, prefix optional."""
    s = s.strip()
    if s.startswith("ed25519:"):
        s = s[len("ed25519:"):]
    # Restore padding
    pad = (-len(s)) % 4
    s += "=" * pad
    try:
        b = base64.b64decode(s, validate=True)
    except Exception as e:
        raise ValueError(f"Invalid public key encoding: {e}")
    if len(b) != 32:
        raise ValueError(f"Public key must be 32 bytes (got {len(b)})")
    return b


def encode_signature(sig_bytes: bytes) -> str:
    """base64nopad — for sign.key embedding."""
    return base64.b64encode(sig_bytes).decode("ascii").rstrip("=")


def decode_signature(s: str) -> bytes:
    s = s.strip()
    pad = (-len(s)) % 4
    s += "=" * pad
    b = base64.b64decode(s, validate=True)
    if len(b) != 64:
        raise ValueError(f"Signature must be 64 bytes (got {len(b)})")
    return b


# ============================================================
# Ed25519 wrapper (isolates vendor impl from CLI)
# ============================================================

# Add vendor to path
_HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(_HERE / "_vendor"))

try:
    from ed25519_rfc8032 import Ed25519 as _Ed25519
except ImportError as e:
    print(f"[FATAL] vendor ed25519 implementation missing: {e}", file=sys.stderr)
    print(f"        Expected at: {_HERE / '_vendor' / 'ed25519_rfc8032.py'}", file=sys.stderr)
    sys.exit(2)


def ed25519_keygen(seed: bytes) -> tuple[bytes, bytes]:
    """Return (private_seed, public_key). RFC 8032: pubkey derived from seed."""
    if len(seed) != 32:
        raise ValueError("Ed25519 seed must be exactly 32 bytes")
    _, pubkey = _Ed25519.keygen(seed)
    return seed, pubkey


def ed25519_sign(private_seed: bytes, public_key: bytes, message: bytes) -> bytes:
    """Return 64-byte signature."""
    if len(private_seed) != 32:
        raise ValueError("private seed must be 32 bytes")
    if len(public_key) != 32:
        raise ValueError("public key must be 32 bytes")
    return _Ed25519.sign(private_seed, public_key, message)


def ed25519_verify(public_key: bytes, message: bytes, signature: bytes) -> bool:
    if len(public_key) != 32 or len(signature) != 64:
        return False
    try:
        return _Ed25519.verify(public_key, message, signature)
    except Exception:
        return False


# ============================================================
# sign.key (re)read/write
# ============================================================

SIGN_KEY_FILENAME = "sign.key"


def read_sign_key(skill_dir: Path) -> dict:
    """Read sign.key from skill_dir. Returns {} if missing."""
    p = Path(skill_dir) / SIGN_KEY_FILENAME
    if not p.exists():
        return {}
    with open(p, "r", encoding="utf-8") as f:
        return json.load(f)


def write_sign_key(skill_dir: Path, data: dict) -> Path:
    p = Path(skill_dir) / SIGN_KEY_FILENAME
    with open(p, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
        f.write("\n")
    return p
