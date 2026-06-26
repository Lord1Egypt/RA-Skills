#!/bin/bash
# extract-features.sh - Extract features for clean reimplementation

REPO_PATH="$1"
if [ -z "$REPO_PATH" ] || [ ! -d "$REPO_PATH" ]; then
    echo "Usage: $0 <repo-path> [output-dir]"
    exit 1
fi

OUTPUT_DIR="${2:-./feature-extraction}"
mkdir -p "$OUTPUT_DIR"

cd "$REPO_PATH"

echo "🔍 Extracting features from: $REPO_PATH"

# README
echo "📖 README analysis..."
if [ -f "README.md" ]; then
    cat README.md > "$OUTPUT_DIR/README-original.md"
fi

# Package metadata
echo "📦 Package metadata..."
if [ -f "package.json" ]; then
    cat package.json | jq '{name, description, version, main, exports, dependencies, peerDependencies}' 2>/dev/null > "$OUTPUT_DIR/package-metadata.json" || cat package.json > "$OUTPUT_DIR/package-metadata.json"
fi

# Entry points
echo "🚪 Entry points..."
find . -maxdepth 2 -name "index.*" -o -name "main.*" -o -name "app.*" | grep -v node_modules > "$OUTPUT_DIR/entry-points.txt"

# Public API exports
echo "📤 Public API exports..."
grep -r "^export" --include="*.ts" --include="*.js" . | grep -v node_modules | head -100 > "$OUTPUT_DIR/exports-raw.txt"

# Type definitions
echo "📝 Type definitions..."
find . -name "*.d.ts" -o -name "types.ts" -o -name "interfaces.ts" | grep -v node_modules | head -20 > "$OUTPUT_DIR/type-files.txt"

# Key classes and interfaces
echo "🏗️  Classes and interfaces..."
grep -r "^(export )?(class|interface|type|enum)" --include="*.ts" . | grep -v node_modules | head -50 > "$OUTPUT_DIR/classes-interfaces.txt"

# Main functions
echo "⚙️  Core functions..."
grep -r "^(export )?function\|^(export )?async function" --include="*.ts" --include="*.js" . | grep -v node_modules | head -50 > "$OUTPUT_DIR/functions.txt"

# Configuration files
echo "⚙️  Configuration..."
find . -maxdepth 2 -name "*.config.*" -o -name ".*rc*" | grep -v node_modules > "$OUTPUT_DIR/config-files.txt"

# Test coverage
echo "🧪 Test structure..."
find . -type d -name "*test*" -o -name "*spec*" | grep -v node_modules | head -20 > "$OUTPUT_DIR/test-directories.txt"
find . -name "*.test.*" -o -name "*.spec.*" | grep -v node_modules | wc -l > "$OUTPUT_DIR/test-file-count.txt"

# Documentation
echo "📚 Documentation..."
find . -name "*.md" | grep -v node_modules | head -20 > "$OUTPUT_DIR/markdown-files.txt"

# Generate feature summary
echo "📝 Generating feature summary..."
cat > "$OUTPUT_DIR/feature-summary.md" << 'EOF'
# Feature Extraction Summary

## Overview
This document summarizes the features extracted for clean reimplementation.

## Core Functionality
EOF

# Extract description from README or package.json
if [ -f "README.md" ]; then
    head -50 README.md | grep -E "^# |^## " | head -5 >> "$OUTPUT_DIR/feature-summary.md"
fi

cat >> "$OUTPUT_DIR/feature-summary.md" << 'EOF'

## Public API
See: exports-raw.txt, classes-interfaces.txt, functions.txt

## Architecture
- Entry points: See entry-points.txt
- Type definitions: See type-files.txt
- Configuration: See config-files.txt

## Testing
- Test files: See test-directories.txt

## Reimplementation Notes
1. Preserve core functionality only
2. Update dependencies to latest secure versions
3. Add comprehensive input validation
4. Implement proper error handling
5. Add security tests
EOF

echo "✅ Feature extraction complete: $OUTPUT_DIR"
