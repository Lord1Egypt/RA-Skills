#!/bin/bash
# dependency-scan.sh - Deep dependency vulnerability scan

REPO_PATH="$1"
if [ -z "$REPO_PATH" ] || [ ! -d "$REPO_PATH" ]; then
    echo "Usage: $0 <repo-path>"
    exit 1
fi

cd "$REPO_PATH"
OUTPUT_DIR="${2:-./security-scan}"
mkdir -p "$OUTPUT_DIR"

echo "🔍 Scanning dependencies in: $REPO_PATH"

# JavaScript/Node.js
if [ -f "package.json" ]; then
    echo "📦 Node.js project detected"
    
    # NPM audit
    if command -v npm >/dev/null; then
        echo "  Running npm audit..."
        npm audit --json > "$OUTPUT_DIR/npm-audit.json" 2>/dev/null || true
        npm audit --audit-level=moderate 2>&1 | tee "$OUTPUT_DIR/npm-audit-summary.txt" || true
    fi
    
    # Yarn audit
    if [ -f "yarn.lock" ] && command -v yarn >/dev/null; then
        echo "  Running yarn audit..."
        yarn audit --json > "$OUTPUT_DIR/yarn-audit.json" 2>/dev/null || true
    fi
    
    # PNPM audit
    if [ -f "pnpm-lock.yaml" ] && command -v pnpm >/dev/null; then
        echo "  Running pnpm audit..."
        pnpm audit --json > "$OUTPUT_DIR/pnpm-audit.json" 2>/dev/null || true
    fi
    
    # Snyk if available
    if command -v snyk >/dev/null; then
        echo "  Running Snyk test..."
        snyk test --json > "$OUTPUT_DIR/snyk-test.json" 2>/dev/null || true
    fi
fi

# Python
if [ -f "requirements.txt" ] || [ -f "pyproject.toml" ]; then
    echo "🐍 Python project detected"
    
    # Safety check
    if command -v safety >/dev/null; then
        echo "  Running safety check..."
        safety check --json > "$OUTPUT_DIR/safety-report.json" 2>/dev/null || true
    fi
    
    # pip-audit
    if command -v pip-audit >/dev/null; then
        echo "  Running pip-audit..."
        pip-audit --format=json > "$OUTPUT_DIR/pip-audit.json" 2>/dev/null || true
    fi
    
    # Bandit for security issues in code
    if command -v bandit >/dev/null; then
        echo "  Running bandit..."
        bandit -r . -f json -o "$OUTPUT_DIR/bandit-report.json" 2>/dev/null || true
    fi
fi

# Rust
if [ -f "Cargo.toml" ]; then
    echo "🦀 Rust project detected"
    
    # cargo-audit
    if command -v cargo-audit >/dev/null; then
        echo "  Running cargo audit..."
        cargo audit --json > "$OUTPUT_DIR/cargo-audit.json" 2>/dev/null || true
    fi
fi

# Go
if [ -f "go.mod" ]; then
    echo "🐹 Go project detected"
    
    # govulncheck
    if command -v govulncheck >/dev/null; then
        echo "  Running govulncheck..."
        govulncheck -json ./... > "$OUTPUT_DIR/govulncheck.json" 2>/dev/null || true
    fi
    
    # nancy
    if command -v nancy >/dev/null; then
        echo "  Running nancy..."
        go list -json -m all | nancy sleuth --output=json > "$OUTPUT_DIR/nancy-report.json" 2>/dev/null || true
    fi
fi

# Generate summary
echo "📊 Generating summary..."
cat > "$OUTPUT_DIR/scan-summary.txt" << EOF
Dependency Scan Summary
=======================
Repository: $REPO_PATH
Scanned: $(date)

Results by Tool:
EOF

for file in "$OUTPUT_DIR"/*.json; do
    if [ -f "$file" ] && [ -s "$file" ]; then
        basename "$file" >> "$OUTPUT_DIR/scan-summary.txt"
        wc -l "$file" | awk '{print "  Lines: " $1}' >> "$OUTPUT_DIR/scan-summary.txt"
    fi
done

echo "✅ Scan complete. Results in: $OUTPUT_DIR"
