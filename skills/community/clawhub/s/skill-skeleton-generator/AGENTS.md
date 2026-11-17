# AGENTS.md — skill-skeleton-generator

Machine-readable entry for AI agents.

## Purpose
Generate a four-angle-compliant AI skill skeleton in one command.

## Invocation
```bash
python scripts/skeleton.py --name my-skill --description "..." [--out dir]
```

## Output contract
- Structured JSON available via `--json` (fields: verdict, score, sha256_8, hits).
- Exit code: 0 = PASS, 1 = FAIL (fail-closed).

## Rules
- Static analysis only; never executes external commands.
- FAIL verdict requires human decision before proceeding.
- No placeholders in outputs.
