#!/usr/bin/env bash
# NOTE: On CIFS/SMB mounts, run with: bash scaffold.sh
# Creates a documentation project structure with ADRs, runbooks, and API docs

set -euo pipefail

PROJECT_NAME="${1:-docs}"
echo "Creating documentation project: $PROJECT_NAME"

mkdir -p "$PROJECT_NAME"/{adr,runbooks,api,guides,references,assets}

# ADR index
cat > "$PROJECT_NAME/adr/index.md" << 'ADREOF'
# Architecture Decision Records

| # | Title | Status | Date |
|---|-------|--------|------|
| 001 | [Template](./0001-template.md) | Template | — |

## Creating a new ADR

1. Copy `0001-template.md` to `NNNN-short-title.md`
2. Fill in all sections
3. Submit as a PR for team review
4. Update this index
ADREOF

# ADR template
cat > "$PROJECT_NAME/adr/0001-template.md" << 'TMPLEOF'
# ADR-001: [Decision Title]

## Status
Proposed

## Context
[What is the issue?]

## Decision
[What did we decide?]

## Consequences
### Positive
- [Benefit]

### Negative
- [Tradeoff]

## Alternatives Considered
### [Alternative]
[Why rejected]
TMPLEOF

# Runbook template
cat > "$PROJECT_NAME/runbooks/template.md" << 'RBEOF'
# Runbook: [Title]

**Severity:** P1/P2/P3
**Team:** [Team]
**Updated:** YYYY-MM-DD

## Symptoms
- [ ] [Observable symptom]

## Diagnosis
```bash
# Step 1: Check service health
curl -s https://api.example.com/health
```

## Remediation
```bash
# Immediate fix
sudo systemctl restart my-service
```

## Escalation
| Time | Action |
|------|--------|
| 15 min | Page secondary on-call |
| 30 min | Escalate to team lead |
RBEOF

# Main README
cat > "$PROJECT_NAME/README.md" << 'RDEOF'
# Documentation

## Structure

```
docs/
├── adr/          Architecture Decision Records
├── runbooks/     Incident response procedures
├── api/          API reference documentation
├── guides/       How-to guides and tutorials
├── references/   Technical reference material
└── assets/       Images, diagrams, etc.
```

## Contributing

1. Create a branch for your changes
2. Write or update documentation
3. Submit a PR for review
4. Ensure CI checks pass (linting, link checking)
RDEOF

# markdownlint config
cat > "$PROJECT_NAME/.markdownlint.json" << 'MLEOF'
{
  "MD013": false,
  "MD033": { "allowed_elements": ["br", "details", "summary", "img"] },
  "MD041": false,
  "MD024": { "siblings_only": true }
}
MLEOF

# cspell config
cat > "$PROJECT_NAME/cspell.json" << 'CSEOF'
{
  "version": "0.2",
  "language": "en",
  "words": ["runbook", "runbooks", "frontmatter"],
  "ignorePaths": ["node_modules"]
}
CSEOF

# .gitignore
cat > "$PROJECT_NAME/.gitignore" << 'GIEOF'
node_modules/
.DS_Store
*.swp
GIEOF

echo ""
echo "Documentation project '$PROJECT_NAME' created!"
echo ""
echo "Structure:"
echo "  adr/        — Architecture Decision Records"
echo "  runbooks/   — Incident response runbooks"
echo "  api/        — API documentation"
echo "  guides/     — How-to guides"
echo "  references/ — Technical references"
echo ""
echo "Optional CI tools:"
echo "  npm install -D markdownlint-cli2 cspell"
echo "  npx markdownlint-cli2 '**/*.md'"
echo "  npx cspell '**/*.md'"
