#!/bin/bash
# text-to-image.sh — Convert plain text/markdown to a styled dark-mode image and send via Telegram
# Usage: text-to-image.sh "Title" "Content (supports \\n line breaks and markdown)"
set -e

TITLE="$1"
CONTENT="$2"
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Credentials from environment (set in OpenClaw config or .env)
BOT_TOKEN="${TELEGRAM_BOT_TOKEN}"
CHAT_ID="${TELEGRAM_CHAT_ID}"

if [ -z "$BOT_TOKEN" ] || [ -z "$CHAT_ID" ]; then
  echo "Error: TELEGRAM_BOT_TOKEN and TELEGRAM_CHAT_ID must be set as environment variables"
  exit 1
fi

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
  echo "Usage: text-to-image.sh \"Title\" \"Content\""
  exit 1
fi

TEMP_HTML="${SCRIPT_DIR}/today.html"

node -e '
const title = process.argv[1];
let content = process.argv[2];
content = content.replace(/\\n/g, "\n");
const lines = content.split("\n").map(l => {
  l = l.trim();
  if (!l) return "<br>";
  if (l.startsWith("##")) return `<h3 style="color:#64b5f6;margin:18px 0 8px">${l.replace(/^#+\s*/, "")}</h3>`;
  if (l.startsWith("#"))  return `<h2 style="color:#fff;margin:20px 0 10px">${l.replace(/^#+\s*/, "")}</h2>`;
  if (l.startsWith("- ") || l.startsWith("• ")) return `<div style="margin:4px 0 4px 16px">• ${l.replace(/^[-•]\s*/, "")}</div>`;
  if (/^\d+\./.test(l)) return `<div style="margin:4px 0 4px 16px">${l}</div>`;
  if (/^[⚠⛔△]/.test(l)) return `<div style="background:#2a2215;border-radius:8px;padding:10px 14px;margin:8px 0;color:#ffd54f">${l}</div>`;
  if (/^[💡📌✅🔥]/.test(l)) return `<div style="background:#1a2230;border-radius:8px;padding:10px 14px;margin:8px 0;color:#90caf9">${l}</div>`;
  return `<div style="margin:4px 0">${l}</div>`;
}).join("\n");
const html = `<!DOCTYPE html>
<html lang="en"><head><meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Noto Sans CJK SC","Noto Color Emoji","Segoe UI",sans-serif; background:#0f0f0f; color:#e0e0e0; padding:40px; width:800px; font-size:15px; line-height:1.8; }
.header { background:linear-gradient(135deg,#1a4a6e,#2d7ab4); border-radius:16px; padding:24px 30px; margin-bottom:24px; }
.header h1 { font-size:24px; color:#fff; }
.content { background:#1a1a1a; border-radius:14px; padding:24px; border-left:4px solid #2d7ab4; }
</style></head>
<body>
<div class="header"><h1>${title}</h1></div>
<div class="content">${lines}</div>
</body></html>`;
require("fs").writeFileSync(process.argv[3], html);
' "$TITLE" "$CONTENT" "$TEMP_HTML"

echo "HTML generated, taking screenshot..."
bash "${SCRIPT_DIR}/send-plan.sh" "$TITLE" "$TEMP_HTML"
