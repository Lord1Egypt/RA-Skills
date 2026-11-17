#!/bin/bash
# Usage: text-to-image.sh "标题" "内容文本"
# Converts plain text to a styled dark-mode image and sends as Telegram album
set -e

TITLE="$1"
CONTENT="$2"
# Credentials are handled by send-album.mjs (skill-root .credentials dotfile);
# this script never touches them.
DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

if [ -z "$TITLE" ] || [ -z "$CONTENT" ]; then
  echo "Usage: text-to-image.sh \"标题\" \"内容文本\""
  exit 1
fi

# Generate HTML from text content
node -e '
// Plan text is treated as untrusted: every character that reaches the HTML is
// escaped, so the rendered page is inert text + fixed styling (no markup,
// no scripts). The renderer (screenshot.mjs) also disables JavaScript and
// blocks all network requests.
const esc = s => String(s)
  .replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;")
  .replace(/"/g, "&quot;").replace(/\x27/g, "&#39;");
const title = esc(process.argv[1]);
let content = process.argv[2];
// Handle literal \n from exec tool
content = content.replace(/\\n/g, "\n");
const lines = content.split("\n").map(raw => {
  const l = raw.trim();
  if (!l) return "<br>";
  if (l.startsWith("##")) return `<h3 style="color:#64b5f6;margin:18px 0 8px">${esc(l.replace(/^#+\s*/, ""))}</h3>`;
  if (l.startsWith("#")) return `<h2 style="color:#fff;margin:20px 0 10px">${esc(l.replace(/^#+\s*/, ""))}</h2>`;
  if (l.startsWith("- ") || l.startsWith("• ")) return `<div style="margin:4px 0 4px 16px">• ${esc(l.replace(/^[-•]\s*/, ""))}</div>`;
  if (/^\d+\./.test(l)) return `<div style="margin:4px 0 4px 16px">${esc(l)}</div>`;
  if (/^[⚠⛔△]/.test(l)) return `<div style="background:#2a2215;border-radius:8px;padding:10px 14px;margin:8px 0;color:#ffd54f">${esc(l)}</div>`;
  if (/^[💡📌✅🔥]/.test(l)) return `<div style="background:#1a2230;border-radius:8px;padding:10px 14px;margin:8px 0;color:#90caf9">${esc(l)}</div>`;
  return `<div style="margin:4px 0">${esc(l)}</div>`;
}).join("\n");

const html = `<!DOCTYPE html>
<html lang="zh"><head><meta charset="UTF-8">
<style>
* { margin:0; padding:0; box-sizing:border-box; }
body { font-family:"Noto Sans CJK SC","Noto Color Emoji",sans-serif; background:#0f0f0f; color:#e0e0e0; padding:40px; width:800px; font-size:15px; line-height:1.8; }
.header { background:linear-gradient(135deg,#1a4a6e,#2d7ab4); border-radius:16px; padding:24px 30px; margin-bottom:24px; }
.header h1 { font-size:24px; color:#fff; }
.content { background:#1a1a1a; border-radius:14px; padding:24px; border-left:4px solid #2d7ab4; }
</style></head>
<body>
<div class="header"><h1>${title}</h1></div>
<div class="content">${lines}</div>
</body></html>`;
require("fs").writeFileSync(process.argv[3], html);
' "$TITLE" "$CONTENT" "${DIR}/today.html"

echo "HTML generated, taking screenshot..."
bash "${DIR}/send-plan.sh" "$TITLE" "${DIR}/today.html"
