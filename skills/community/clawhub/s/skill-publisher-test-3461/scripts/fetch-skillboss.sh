#!/bin/bash
# Fetch skill from SkillBoss.co
# Usage: ./fetch-skillboss.sh <skillboss-url> <output-dir>

set -e

SKILL_URL="$1"

# 修正 URL：确保使用 www.skillboss.co
SKILL_URL=$(echo "$SKILL_URL" | sed 's|https://skillboss.co|https://www.skillboss.co|g')
OUTPUT_DIR="$2"

if [ -z "$SKILL_URL" ] || [ -z "$OUTPUT_DIR" ]; then
  echo "Usage: $0 <skillboss-url> <output-dir>"
  exit 1
fi

mkdir -p "$OUTPUT_DIR"

echo "Fetching skill from: $SKILL_URL"

# Extract skill slug from URL
SKILL_SLUG=$(echo "$SKILL_URL" | sed 's|https://www.skillboss.co/skills/||' | sed 's|https://skillboss.co/skills/||' | sed 's|/||g')

echo "Skill slug: $SKILL_SLUG"

# Fetch skill page HTML
HTML=$(curl -s "$SKILL_URL")

# Extract skill metadata (simplified - in real implementation would parse properly)
SKILL_NAME=$(echo "$HTML" | grep -oP '<h1[^>]*>\K[^<]+' | head -1 || echo "$SKILL_SLUG")
SKILL_DESC=$(echo "$HTML" | grep -oP '<meta name="description" content="\K[^"]+' || echo "OpenClaw skill")

# Try to find download link
DOWNLOAD_URL=$(echo "$HTML" | grep -oP 'href="(/downloads/[^"]+\.zip)"' | head -1 || echo "")

if [ -z "$DOWNLOAD_URL" ]; then
  # Try alternative pattern
  DOWNLOAD_URL=$(echo "$HTML" | grep -oP 'download[^"]*"\s*:\s*"\K[^"]+' | head -1 || echo "")
fi

echo "Skill name: $SKILL_NAME"
echo "Description: $SKILL_DESC"

if [ -n "$DOWNLOAD_URL" ]; then
  # Convert relative URL to absolute if needed
  if [[ "$DOWNLOAD_URL" == /* ]]; then
    DOWNLOAD_URL="https://www.skillboss.co${DOWNLOAD_URL}"
  fi
  
  echo "Downloading: $DOWNLOAD_URL"
  
  ZIP_FILE="$OUTPUT_DIR/${SKILL_SLUG}.zip"
  curl -L -o "$ZIP_FILE" "$DOWNLOAD_URL"
  
  if [ -f "$ZIP_FILE" ]; then
    echo "✅ Downloaded to: $ZIP_FILE"
    
    # Extract ZIP
    EXTRACT_DIR="$OUTPUT_DIR/$SKILL_SLUG"
    unzip -qo "$ZIP_FILE" -d "$EXTRACT_DIR"
    echo "✅ Extracted to: $EXTRACT_DIR"
    
    # Output metadata as JSON
    cat > "$OUTPUT_DIR/${SKILL_SLUG}.json" << EOF
{
  "slug": "$SKILL_SLUG",
  "name": "$SKILL_NAME",
  "description": "$SKILL_DESC",
  "source_url": "$SKILL_URL",
  "download_url": "$DOWNLOAD_URL",
  "local_path": "$EXTRACT_DIR"
}
EOF
    
    echo "✅ Metadata saved to: $OUTPUT_DIR/${SKILL_SLUG}.json"
    exit 0
  else
    echo "❌ Download failed"
    exit 1
  fi
else
  echo "❌ No download link found"
  echo "⚠️  Skill might not be publicly available for download"
  echo "💡 Try using ZIP file upload instead"
  exit 1
fi
