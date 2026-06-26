#!/bin/bash
# audit-repo.sh - Full security audit of a GitHub repository

set -e

REPO_URL="$1"
if [ -z "$REPO_URL" ]; then
    echo "Usage: $0 <github-url>"
    exit 1
fi

REPO_NAME=$(basename "$REPO_URL" .git | tr '[:upper:]' '[:lower:]')
TIMESTAMP=$(date +%Y%m%d-%H%M%S)
AUDIT_DIR="$HOME/repo-audits/${REPO_NAME}-${TIMESTAMP}"

mkdir -p "$AUDIT_DIR"
cd "$AUDIT_DIR"

echo "🔍 Auditing: $REPO_URL"
echo "📁 Output: $AUDIT_DIR"

# Clone
echo "⏳ Cloning repository..."
git clone --depth 1 "$REPO_URL" repo 2>/dev/null

if [ ! -d "repo" ]; then
    echo "❌ Failed to clone repository"
    exit 1
fi

cd repo

echo "📋 Creating inventory..."
find . -type f \( \
    -name "*.js" -o -name "*.ts" -o -name "*.jsx" -o -name "*.tsx" -o \
    -name "*.py" -o -name "*.go" -o -name "*.rs" -o -name "*.java" -o \
    -name "*.c" -o -name "*.cpp" -o -name "*.h" -o \
    -name "*.json" -o -name "*.yaml" -o -name "*.yml" -o \
    -name "*.toml" -o -name "*.lock" \
\) | grep -v node_modules | grep -v ".git/" > "$AUDIT_DIR/file-inventory.txt"

echo "🔍 Scanning for suspicious patterns..."

# Network patterns
grep -rE "(fetch|axios|request|http|socket|net)\.(post|get|send|write|connect)" \
    --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" \
    . 2>/dev/null | grep -v node_modules | head -50 > "$AUDIT_DIR/suspicious-network.txt" || true

# Dynamic execution
grep -rE "(\beval\s*\(|\bFunction\s*\(|\bsetTimeout\s*\(|\bsetInterval\s*\()" \
    --include="*.js" --include="*.ts" --include="*.jsx" --include="*.tsx" \
    . 2>/dev/null | grep -v node_modules | head -50 > "$AUDIT_DIR/suspicious-dynamic.txt" || true

# Obfuscation
grep -rE "(\\\\x[0-9a-f]{2}|\\\\u[0-9a-f]{4}|fromCharCode|\\\\[0-9]{1,3}|atob\s*\(|btoa\s*\()" \
    --include="*.js" --include="*.ts" \
    . 2>/dev/null | grep -v node_modules | head -50 > "$AUDIT_DIR/suspicious-obfuscation.txt" || true

# Shell execution
grep -rE "(child_process|exec\s*\(|execSync|spawn|execFile)" \
    --include="*.js" --include="*.ts" --include="*.py" \
    . 2>/dev/null | grep -v node_modules | head -30 > "$AUDIT_DIR/shell-execution.txt" || true

# Crypto patterns
grep -riE "(bitcoin|ethereum|monero|crypto\.Currency|mining|wallet|blockchain|coin)" \
    --include="*.js" --include="*.ts" --include="*.py" --include="*.md" \
    . 2>/dev/null | grep -v node_modules | head -20 > "$AUDIT_DIR/crypto-patterns.txt" || true

# Environment access
grep -rE "(process\.env|env\[|getenv|os\.environ)" \
    --include="*.js" --include="*.ts" --include="*.py" \
    . 2>/dev/null | grep -v node_modules | head -30 > "$AUDIT_DIR/env-access.txt" || true

echo "📊 Dependency analysis..."

# Package.json
if [ -f "package.json" ]; then
    cat package.json > "$AUDIT_DIR/package.json"
    npm audit --json 2>/dev/null > "$AUDIT_DIR/npm-audit.json" || true
fi

# Python
if [ -f "requirements.txt" ]; then
    cat requirements.txt > "$AUDIT_DIR/requirements.txt"
fi
if [ -f "pyproject.toml" ]; then
    cat pyproject.toml > "$AUDIT_DIR/pyproject.toml"
fi

# Rust
if [ -f "Cargo.toml" ]; then
    cat Cargo.toml > "$AUDIT_DIR/Cargo.toml"
fi

# Go
if [ -f "go.mod" ]; then
    cat go.mod > "$AUDIT_DIR/go.mod"
fi

# License
echo "📄 License check..."
LICENSE_FILE=$(find . -maxdepth 2 -iname "license*" -o -iname "copying*" | head -1)
if [ -n "$LICENSE_FILE" ]; then
    cat "$LICENSE_FILE" > "$AUDIT_DIR/LICENSE-content.txt"
fi

echo "✅ Audit complete! Results in: $AUDIT_DIR"
echo ""
echo "Next: Run security analysis on the findings"
