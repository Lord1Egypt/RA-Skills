#!/usr/bin/env python3
"""Stage 3: rank modules, detect API/CLI surface and external SDK usage."""
import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

SDK_HINTS = {
    # Python
    "openai": "OpenAI LLM API", "anthropic": "Anthropic LLM API",
    "boto3": "AWS SDK", "redis": "Redis client",
    "kafka": "Kafka client", "sqlalchemy": "SQL ORM",
    "fastapi": "FastAPI web framework", "flask": "Flask web framework",
    "django": "Django web framework", "pandas": "DataFrame analysis",
    "numpy": "Numerical computing", "torch": "PyTorch ML",
    "tensorflow": "TensorFlow ML", "transformers": "HuggingFace models",
    "celery": "Distributed task queue", "pydantic": "Data validation",
    # JS
    "express": "Express web framework", "react": "React UI",
    "vue": "Vue UI", "next": "Next.js framework",
    "axios": "HTTP client", "prisma": "Database ORM",
    "mongoose": "MongoDB ORM",
    # Go
    "gin-gonic/gin": "Gin web framework", "gorilla/mux": "HTTP router",
}

# HTTP route patterns by language
ROUTE_PATTERNS = [
    # Python: @app.route, @router.get/post/...
    (r'@\w+\.(?:route|get|post|put|delete|patch)\(["\']([^"\']+)["\']', "HTTP"),
    # Express: app.get('/path', ...
    (r'\b(?:app|router)\.(?:get|post|put|delete|patch)\(["\']([^"\']+)["\']', "HTTP"),
    # Go: r.HandleFunc("/path"  or  r.GET("/path"
    (r'\.(?:HandleFunc|GET|POST|PUT|DELETE)\(["\']([^"\']+)["\']', "HTTP"),
    # Django urls.py: path('foo/', ...)
    (r'\bpath\(["\']([^"\']+)["\']', "HTTP"),
]

CLI_PATTERNS = [
    # Python click/argparse
    (r'@\w+\.command\(["\']?([a-zA-Z\-_]*)["\']?\)', "CLI"),
    (r'add_parser\(["\']([a-zA-Z\-_]+)["\']', "CLI"),
    # cobra (Go)
    (r'Use:\s*["\']([a-zA-Z\-_]+)["\']', "CLI"),
]


def scan_code(root: Path, scan_data: dict):
    structure = scan_data["structure"]
    file_count = defaultdict(int)  # dir -> count
    sdk_evidence = defaultdict(list)
    routes = []
    clis = []
    inbound_imports = Counter()

    # gather code files
    code_exts = {".py", ".js", ".ts", ".jsx", ".tsx", ".go", ".java", ".rb", ".rs"}
    code_files = []
    for p in root.rglob("*"):
        if not p.is_file():
            continue
        if any(part.startswith(".") or part in {"node_modules", "venv", "vendor", "dist", "build"} for part in p.relative_to(root).parts):
            continue
        if p.suffix.lower() in code_exts:
            code_files.append(p)

    # cap to avoid huge runs
    code_files = code_files[:2000]

    for fp in code_files:
        try:
            text = fp.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        rel = str(fp.relative_to(root))
        top_dir = rel.split("/")[0] if "/" in rel else "."
        file_count[top_dir] += 1

        # SDK detection
        for kw, purpose in SDK_HINTS.items():
            for m in re.finditer(rf"\b(?:import|from|require\(|\"){re.escape(kw)}\b", text):
                line = text[:m.start()].count("\n") + 1
                sdk_evidence[kw].append(f"{rel}:{line}")
                if len(sdk_evidence[kw]) >= 3:
                    break

        # Routes
        for pat, ptype in ROUTE_PATTERNS:
            for m in re.finditer(pat, text):
                line = text[:m.start()].count("\n") + 1
                routes.append({"path": m.group(1), "evidence": f"{rel}:{line}"})

        # CLI
        for pat, ptype in CLI_PATTERNS:
            for m in re.finditer(pat, text):
                line = text[:m.start()].count("\n") + 1
                cmd = m.group(1) or "(default)"
                clis.append({"command": cmd, "evidence": f"{rel}:{line}"})

        # naive inbound import counting (Python style only for MVP)
        if fp.suffix == ".py":
            for m in re.finditer(r"^\s*from\s+([\w\.]+)\s+import|^\s*import\s+([\w\.]+)", text, re.M):
                mod = (m.group(1) or m.group(2)).split(".")[0]
                inbound_imports[mod] += 1

    # rank top dirs by file count
    top_dirs = sorted(file_count.items(), key=lambda x: -x[1])[:10]

    out = {
        "code_file_count": len(code_files),
        "top_modules": [
            {"path": d, "file_count": c} for d, c in top_dirs
        ],
        "sdk_usage": [
            {"sdk": kw, "purpose": SDK_HINTS[kw], "evidence": ev[:3]}
            for kw, ev in sdk_evidence.items()
        ],
        "http_routes": routes[:50],
        "cli_commands": clis[:30],
        "inbound_imports_top": dict(inbound_imports.most_common(20)),
    }
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("repo_path")
    ap.add_argument("scan_json")
    args = ap.parse_args()
    scan = json.loads(Path(args.scan_json).read_text())
    analysis = scan_code(Path(args.repo_path), scan)
    print(json.dumps(analysis, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
