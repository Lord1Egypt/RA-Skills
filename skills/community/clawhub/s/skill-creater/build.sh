#!/bin/bash
# Build script for Skill Craftsmen
# Packages the skill for Clawhub upload

set -e

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR/.."

SKILL_NAME="skill-craftsmen"
VERSION="1.0.0"
OUTPUT_DIR="./dist"

echo "🔨 Building $SKILL_NAME v$VERSION..."

# Create output directory
mkdir -p "$OUTPUT_DIR"

# Package the skill
python3 scripts/package_skill.py . "$OUTPUT_DIR" "$VERSION"

echo ""
echo "✅ Build complete!"
echo "📦 Output: $OUTPUT_DIR/${SKILL_NAME}-v${VERSION}.zip"
