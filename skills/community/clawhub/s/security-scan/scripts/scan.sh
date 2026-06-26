#!/bin/bash
# Lightweight security scan for a target directory.

set -u

TARGET_DIR=${1:-}

if [ -z "$TARGET_DIR" ]; then
    echo "Usage: $0 <target_directory>"
    exit 1
fi

if [ ! -d "$TARGET_DIR" ]; then
    echo "Error: target directory does not exist: $TARGET_DIR"
    exit 1
fi

echo "Starting Security Scan for: $TARGET_DIR"
echo "======================================"

echo "[1/3] Scanning for dangerous function calls (eval, exec, system, spawn)..."
DANGEROUS_CALLS=$(grep -rEn '\beval\s*\(|\bexec\s*\(|\bsystem\s*\(|\bspawn\s*\(' \
    "$TARGET_DIR" \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude=SKILL.md 2>/dev/null || true)

if [ -n "$DANGEROUS_CALLS" ]; then
    echo "WARNING: Potential dangerous function calls found:"
    echo "$DANGEROUS_CALLS"
else
    echo "OK: No dangerous function calls detected."
fi

echo ""
echo "[2/3] Checking for hardcoded secrets/credentials (API keys, passwords)..."
SECRETS=$(grep -rEn 'AIza[0-9A-Za-z_-]{35}|sk-[0-9A-Za-z]{32,}|gsk_[0-9A-Za-z]{16,}|nvapi-[0-9A-Za-z-]{16,}' \
    "$TARGET_DIR" \
    --exclude-dir=.git \
    --exclude-dir=node_modules \
    --exclude=SKILL.md 2>/dev/null || true)

if [ -n "$SECRETS" ]; then
    echo "WARNING: Potential hardcoded secrets found:"
    echo "$SECRETS"
else
    echo "OK: No obvious hardcoded secrets detected."
fi

echo ""
echo "[3/3] Analyzing file permissions..."
WORLD_WRITABLE=$(find "$TARGET_DIR" -type f -perm -0002 2>/dev/null || true)

if [ -n "$WORLD_WRITABLE" ]; then
    echo "WARNING: World-writable files found:"
    echo "$WORLD_WRITABLE"
else
    echo "OK: No world-writable files detected."
fi

echo "======================================"
echo "Security Scan Complete."
