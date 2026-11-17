"""Server endpoints that spend money on a paid API with no login check in sight."""
from __future__ import annotations

import re
from pathlib import Path

from common import iter_files, read_text, rel
from probes import Finding
from probes.util import CODE, line_at, line_text, local_imports

NAME = "paid_api_unauthed"
APPLIES_TO = {"nextjs", "express"}
PAID = re.compile(
    r"""(?:from\s+|require\(\s*)['"](openai|@anthropic-ai/sdk|replicate|stripe|twilio|resend"""
    r"""|@google/generative-ai|@google/genai|groq-sdk|cohere-ai|elevenlabs|@elevenlabs/elevenlabs-js)['"]"""
    r"""|https://api\.(openai|anthropic|replicate|stripe|elevenlabs)\.(?:com|io)""")
AUTH = re.compile(
    r"getUser\(|getSession\(|getServerSession\(|\bauth\(\)|currentUser\(|verifyIdToken\(|jwt\.verify\("
    r"|requireAuth|isAuthenticated|withAuth|clerkClient|getAuth\(|req\.user\b|supabase\.auth\."
    r"|passport\.authenticate|ensureLoggedIn|authMiddleware", re.I)
NEXT_ROUTE = re.compile(r"(?:^|/)(?:app/(?:.+/)?route|pages/api/.+)\.(?:t|j)sx?$")
EXPRESS = re.compile(r"\b(?:app|router)\.(?:get|post|put|patch|delete|all)\(")
HANDLER = re.compile(
    r"export\s+(?:async\s+)?function\s+(?:GET|POST|PUT|PATCH|DELETE)\b"
    r"|export\s+const\s+(?:GET|POST|PUT|PATCH|DELETE)\b|export\s+default\s+(?:async\s+)?function"
    r"|\b(?:app|router)\.(?:get|post|put|patch|delete|all)\(|['\"]use server['\"]")


def _service(m: re.Match) -> str:
    name = next(g for g in m.groups() if g)
    return name.split("/")[-1].replace("@", "").replace("-sdk", "").replace("sdk", "").strip("-") or name


def run(root, stack) -> list[Finding]:
    root = Path(root).resolve()
    out: list[Finding] = []
    for p in iter_files(root, CODE):
        r, text = rel(p, root), read_text(p)
        is_endpoint = NEXT_ROUTE.search(r) or EXPRESS.search(text) or "use server" in text
        if not is_endpoint or AUTH.search(text):
            continue
        m = PAID.search(text)
        if not m:
            for dep in local_imports(root, p, text):
                m = PAID.search(read_text(dep))
                if m:
                    break
        if not m:
            continue
        h = HANDLER.search(text)
        ln = line_at(text, h.start()) if h else 1
        service = m.group(1) or m.group(2)
        label = "anthropic" if "anthropic" in service else _service(m)
        out.append(Finding(NAME, "hint", r, ln, line_text(text, ln),
                           f"This server endpoint calls a paid service ({label}) and no login check was found in the file"))
    return out
