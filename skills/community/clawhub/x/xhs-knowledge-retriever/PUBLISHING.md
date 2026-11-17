# Publishing

## Pre-publish Audit

Run from this Skill directory:

```bash
python3 -m py_compile scripts/retrieve.py
clawhub skill publish . --version 0.1.0 --changelog "Initial release: local XHS competitor-note RAG retrieval." --tags xhs,rag,retrieval,content-strategy --categories productivity --topics "xiaohongshu,rag,competitor-analysis,content-strategy" --dry-run
```

Expected audit result:

- No dynamic execution.
- No direct network calls.
- No credential reads.
- No setup section asking users to run installer commands.
- Runtime metadata matches actual behavior.

## Publish

```bash
clawhub login
clawhub whoami
clawhub skill publish . --version 0.1.0 --changelog "Initial release: local XHS competitor-note RAG retrieval." --tags xhs,rag,retrieval,content-strategy --categories productivity --topics "xiaohongshu,rag,competitor-analysis,content-strategy"
clawhub inspect xhs-knowledge-retriever --files
```

After publishing, wait for ClawHub scan state to become `clean` before submitting.
