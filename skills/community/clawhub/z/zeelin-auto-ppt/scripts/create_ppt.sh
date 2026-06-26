#!/bin/bash
# create_ppt.sh — Automate NotebookLM to create a presentation from text content
# Usage: bash create_ppt.sh "content text" ["output filename"]
#
# This script handles the full NotebookLM automation flow:
#   1. Open NotebookLM
#   2. Create new notebook
#   3. Paste source text
#   4. Generate presentation (Audio Overview -> Slides)
#   5. Download PDF to ~/Desktop/

set -e

CONTENT="$1"
OUTPUT_NAME="${2:-PPT_$(date +%Y%m%d_%H%M).pdf}"
OUTPUT_PATH="$HOME/Desktop/$OUTPUT_NAME"
CLI="openclaw browser"

if [ -z "$CONTENT" ]; then
  echo "ERROR: No content provided"
  echo "Usage: bash create_ppt.sh \"content text\" [\"output_filename.pdf\"]"
  exit 1
fi

wait_and_snap() {
  local wait_sec="${1:-3}"
  sleep "$wait_sec"
  $CLI snapshot 2>/dev/null
}

find_ref() {
  local snap="$1"
  local pattern="$2"
  echo "$snap" | grep -i "$pattern" | grep -oE 'ref=e[0-9]+' | tail -1 | sed 's/ref=//'
}

find_button_ref() {
  local snap="$1"
  local pattern="$2"
  echo "$snap" | grep -i "button.*$pattern" | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//'
}

click_ref() {
  local ref="$1"
  local label="$2"
  if [ -z "$ref" ]; then
    echo "ERROR: Could not find element: $label"
    return 1
  fi
  echo "  Clicking: $label ($ref)"
  $CLI click "$ref" 2>/dev/null
}

echo "============================================"
echo "  NotebookLM PPT Generator"
echo "============================================"
echo "Output: $OUTPUT_PATH"
echo ""

echo "=== Step 1/7: Opening NotebookLM ==="
$CLI open "https://notebooklm.google.com/" 2>/dev/null
SNAP=$(wait_and_snap 5)

if echo "$SNAP" | grep -qi "sign.in\|登录\|login"; then
  echo "WARNING: NotebookLM requires login. Please sign in manually, then re-run this script."
  exit 1
fi
echo "  NotebookLM loaded"

echo ""
echo "=== Step 2/7: Creating new notebook ==="
REF=$(find_button_ref "$SNAP" "新建笔记本\|[Nn]ew notebook")
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "新建\|[Cc]reate.*new")
fi
click_ref "$REF" "New notebook button"
SNAP=$(wait_and_snap 6)
echo "  New notebook created"

echo ""
echo "=== Step 3/7: Finding 'Copied text' option ==="
# After creating a notebook, NotebookLM auto-opens a source dialog.
# Look for "复制的文字" directly — do NOT click "添加来源" again.
REF=$(find_button_ref "$SNAP" "复制的文字\|[Cc]opied text\|[Pp]aste text")
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "content_paste\|粘贴")
fi

# If dialog didn't auto-open, then click "添加来源"
if [ -z "$REF" ]; then
  echo "  Dialog not auto-opened, clicking Add source..."
  ADD_REF=$(find_button_ref "$SNAP" "添加来源\|[Aa]dd source")
  if [ -z "$ADD_REF" ]; then
    ADD_REF=$(find_button_ref "$SNAP" "add\|添加")
  fi
  if [ -n "$ADD_REF" ]; then
    click_ref "$ADD_REF" "Add source"
    SNAP=$(wait_and_snap 4)
    REF=$(find_button_ref "$SNAP" "复制的文字\|[Cc]opied text\|[Pp]aste text")
    if [ -z "$REF" ]; then
      REF=$(find_button_ref "$SNAP" "content_paste\|粘贴")
    fi
  fi
fi

click_ref "$REF" "Copied text option"
SNAP=$(wait_and_snap 3)
echo "  Text source dialog opened"

echo ""
echo "=== Step 4/7: Pasting content ==="
REF=$(find_ref "$SNAP" 'textbox.*粘贴\|textbox.*[Pp]aste\|textbox.*在此处')
if [ -z "$REF" ]; then
  REF=$(find_ref "$SNAP" 'textbox.*active\|textbox.*placeholder')
fi
if [ -z "$REF" ]; then
  REF=$(find_ref "$SNAP" "textbox\|textarea")
fi
if [ -z "$REF" ]; then
  echo "ERROR: Could not find text input area"
  echo "SNAPSHOT:"
  echo "$SNAP" | head -30
  exit 1
fi
echo "  Found text input: $REF"
echo "  Typing content (${#CONTENT} chars)..."
$CLI type "$REF" "$CONTENT" 2>/dev/null
SNAP=$(wait_and_snap 2)

REF=$(find_button_ref "$SNAP" "插入\|[Ii]nsert\|[Ss]ubmit")
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "确[定认]\|[Aa]dd")
fi
click_ref "$REF" "Insert button"
SNAP=$(wait_and_snap 5)
echo "  Content inserted"

echo ""
echo "=== Step 5/7: Generating presentation ==="
REF=$(find_button_ref "$SNAP" "演示文稿\|[Pp]resentation")
if [ -z "$REF" ]; then
  SNAP=$(wait_and_snap 5)
  REF=$(find_button_ref "$SNAP" "演示文稿\|[Pp]resentation\|[Ss]lides")
fi
click_ref "$REF" "Generate presentation"
echo "  Generating slides... (this may take 30-60 seconds)"

READY=false
for i in $(seq 1 30); do
  sleep 10
  SNAP=$($CLI snapshot 2>/dev/null)
  # Check if generation is done: look for a presentation entry with timestamp, or "已准备就绪"
  if echo "$SNAP" | grep -qi "已准备就绪\|幻灯片.*已准备"; then
    READY=true
    echo "  Presentation ready! (detected: 已准备就绪)"
    break
  fi
  if echo "$SNAP" | grep -qi "button.*个来源.*前"; then
    READY=true
    echo "  Presentation ready! (detected: entry with timestamp)"
    break
  fi
  # Check if still generating
  if echo "$SNAP" | grep -qi "正在生成\|generating"; then
    echo "  Still generating... ($((i*10))s elapsed)"
  else
    echo "  Waiting... ($((i*10))s elapsed)"
  fi
done

if [ "$READY" = false ]; then
  echo "WARNING: Timed out after 300s. Taking final snapshot..."
  SNAP=$($CLI snapshot 2>/dev/null)
fi

echo ""
echo "=== Step 6/7: Opening presentation ==="
# Find the generated presentation entry in the Studio panel
# Pattern 1: button with "个来源" and timestamp (e.g., "1 个来源 · 2 分钟前")
REF=$(echo "$SNAP" | grep -i 'button.*个来源.*前\|button.*source.*ago' | grep -v "disabled\|正在生成\|generating" | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
# Pattern 2: button with "个来源" (without timestamp)
if [ -z "$REF" ]; then
  REF=$(echo "$SNAP" | grep -i 'button.*个来源\|button.*source' | grep -v "disabled\|正在生成\|generating" | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi
# Pattern 3: generic with cursor=pointer near Studio output area
if [ -z "$REF" ]; then
  REF=$(echo "$SNAP" | grep -i 'generic.*cursor=pointer.*个来源\|generic.*cursor=pointer.*source' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi
# Pattern 4: any clickable element mentioning "个来源"
if [ -z "$REF" ]; then
  REF=$(find_ref "$SNAP" "cursor=pointer.*个来源")
fi

if [ -z "$REF" ]; then
  echo "WARNING: Could not find presentation entry. Trying to snap again..."
  sleep 10
  SNAP=$($CLI snapshot 2>/dev/null)
  REF=$(echo "$SNAP" | grep -i 'button.*个来源' | grep -v "disabled\|正在生成" | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
fi

click_ref "$REF" "Open presentation"
SNAP=$(wait_and_snap 5)
echo "  Presentation opened"

echo ""
echo "=== Step 7/7: Downloading PDF ==="
REF=$(find_button_ref "$SNAP" "更多选项\|more_horiz")
if [ -z "$REF" ]; then
  REF=$(find_button_ref "$SNAP" "[Mm]ore.*option\|更多")
fi
click_ref "$REF" "More options menu"
SNAP=$(wait_and_snap 3)

REF=$(echo "$SNAP" | grep -i 'menuitem.*PDF' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
if [ -z "$REF" ]; then
  REF=$(find_ref "$SNAP" "下载 PDF\|[Dd]ownload.*PDF\|PDF.*文档")
fi

if [ -z "$REF" ]; then
  echo "ERROR: Could not find PDF download option"
  echo "SNAPSHOT of menu:"
  echo "$SNAP" | grep -i "menu\|PDF\|下载\|download" | head -10
  echo "  Please download manually from the open presentation"
  exit 1
fi

echo "  Downloading PDF to $OUTPUT_PATH ..."
$CLI download "$REF" "$OUTPUT_PATH" --timeout-ms 30000 2>/dev/null
sleep 3

if [ -f "$OUTPUT_PATH" ]; then
  SIZE=$(du -h "$OUTPUT_PATH" | cut -f1)
  echo ""
  echo "============================================"
  echo "  SUCCESS!"
  echo "  File: $OUTPUT_PATH"
  echo "  Size: $SIZE"
  echo "============================================"
else
  echo ""
  echo "WARNING: PDF file not found at $OUTPUT_PATH"
  echo "  The download may still be in progress."
  echo "  Check ~/Desktop/ for the file."
fi
