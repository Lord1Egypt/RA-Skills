# Prevention Guide

How to prevent secrets from being committed in the future.

## Pre-commit Hook Setup

### Option 1: git-secrets (AWS)

```bash
# Install
brew install git-secrets  # macOS
# or
git clone https://github.com/awslabs/git-secrets.git && cd git-secrets && make install

# Set up in repo
cd /path/to/project
git secrets --install
git secrets --register-aws

# Add custom patterns
git secrets --add 'sk_live_[0-9a-zA-Z]{24,}'
git secrets --add 'sk-proj-[A-Za-z0-9_-]{40,}'
```

### Option 2: pre-commit framework

```yaml
# .pre-commit-config.yaml
repos:
  - repo: https://github.com/Yelp/detect-secrets
    rev: v1.4.0
    hooks:
      - id: detect-secrets
        args: ['--baseline', '.secrets.baseline']
```

```bash
pip install pre-commit
pre-commit install
```

### Option 3: Simple bash hook

```bash
#!/bin/bash
# .git/hooks/pre-commit

PATTERNS=(
  'AKIA[0-9A-Z]{16}'
  'sk_live_'
  'sk-proj-'
  'ghp_[A-Za-z0-9_]{36}'
  '-----BEGIN.*PRIVATE KEY-----'
)

for pattern in "${PATTERNS[@]}"; do
  if git diff --cached --diff-filter=ACM | grep -qE "$pattern"; then
    echo "ERROR: Potential secret detected matching pattern: $pattern"
    echo "Use 'git diff --cached' to review."
    exit 1
  fi
done
```

## .gitignore Essentials

Add these to every project's `.gitignore`:

```
# Environment files
.env
.env.local
.env.*.local
.env.production
.env.staging

# Key files
*.pem
*.key
*.p12
*.pfx
id_rsa*
*.jks

# Credentials
credentials.json
service-account*.json
*-credentials.json
```

## Secrets Manager Options

| Tool | Best For | Price |
|------|----------|-------|
| AWS Secrets Manager | AWS-native apps | $0.40/secret/month |
| HashiCorp Vault | Multi-cloud, on-prem | Free (OSS) |
| 1Password CLI | Small teams, individuals | From $2.99/month |
| Doppler | Dev-friendly, any stack | Free tier available |
| Azure Key Vault | Azure-native apps | Pay per operation |
| GCP Secret Manager | GCP-native apps | $0.06/10K operations |
