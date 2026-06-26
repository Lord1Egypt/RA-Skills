#!/bin/bash
# WSB Digest - Discord Push Script
# 自动抓取 WSB 热股数据并推送到 Discord
# 
# 安装后需要修改:
# 1. TARGET_CHANNEL_ID - Discord 频道 ID
# 2. OPENCLAW_BIN - OpenClaw 可执行文件路径
# 3. SKILL_DIR - 本 skill 的安装路径

set -euo pipefail

# ============================================
# 配置区域 (安装后必须修改!)
# ============================================

# Discord 频道 ID（必须修改为你的频道 ID!）
# 获取方法: Discord 设置 → 高级 → 开启开发者模式 → 右键频道 → 复制频道 ID
TARGET_CHANNEL_ID="你的频道ID"

# OpenClaw 可执行文件路径（根据你的安装方式调整）
OPENCLAW_BIN="/root/.local/share/pnpm/openclaw"

# Skill 安装目录
SKILL_DIR="/root/.openclaw/workspace/skills/wsb-digest"

# ============================================
# 日志和临时文件配置
# ============================================

LOG_FILE=/tmp/wsb-digest.log
RAW_FILE=/tmp/wsb-raw.out
JSON_FILE=/tmp/wsb-latest.json
CHUNK_DIR=/tmp/wsb-digest-chunks

# 确保 PATH 包含 node
export PATH="/usr/bin:/usr/local/bin:$PATH"
export HOME=/root

# ============================================
# 主程序
# ============================================

echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Starting WSB Digest..." >> "$LOG_FILE"

# 1) 抓取数据
if ! node "${SKILL_DIR}/scripts/apewisdom-wsb.js" > "$RAW_FILE" 2>> "$LOG_FILE"; then
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] ❌ Generator failed" >> "$LOG_FILE"
  exit 1
fi

# 2) 提取 JSON
awk 'found{print} /^\{/{found=1; print}' "$RAW_FILE" > "$JSON_FILE"

# 3) 分片处理 (Discord 2000 字符限制)
rm -rf "$CHUNK_DIR"
mkdir -p "$CHUNK_DIR"

if ! node - <<'NODE' "$JSON_FILE" "$CHUNK_DIR" 2>> "$LOG_FILE"
const fs = require('fs');
const jsonPath = process.argv[2];
const outDir = process.argv[3];

const payload = JSON.parse(fs.readFileSync(jsonPath, 'utf8'));
let text = String(payload.digest_markdown || '').trim();
if (!text) {
  text = 'WSB Digest 生成成功，但 digest_markdown 为空。';
}

const MAX = 1800;

function splitLongLine(line, max) {
  const chunks = [];
  let i = 0;
  while (i < line.length) {
    chunks.push(line.slice(i, i + max));
    i += max;
  }
  return chunks;
}

function splitForDiscord(input, max) {
  const lines = input.split('\n');
  const chunks = [];
  let cur = '';

  for (let line of lines) {
    if (line.length > max) {
      const parts = splitLongLine(line, max);
      for (const p of parts) {
        if (cur) {
          chunks.push(cur);
          cur = '';
        }
        chunks.push(p);
      }
      continue;
    }

    const next = cur ? `${cur}\n${line}` : line;
    if (next.length > max) {
      if (cur) chunks.push(cur);
      cur = line;
    } else {
      cur = next;
    }
  }

  if (cur) chunks.push(cur);
  return chunks.filter(Boolean);
}

const chunks = splitForDiscord(text, MAX);
if (!chunks.length) chunks.push('WSB Digest 为空。');

chunks.forEach((c, idx) => {
  const p = `${outDir}/chunk-${String(idx + 1).padStart(3, '0')}.txt`;
  fs.writeFileSync(p, c, 'utf8');
});

fs.writeFileSync(`${outDir}/count.txt`, String(chunks.length), 'utf8');
NODE
then
  echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] ❌ Invalid JSON payload or split failed" >> "$LOG_FILE"
  exit 1
fi

CHUNK_COUNT=$(cat "$CHUNK_DIR/count.txt")
echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] Prepared $CHUNK_COUNT message chunk(s)" >> "$LOG_FILE"

# 4) 发送到 Discord
idx=0
for f in "$CHUNK_DIR"/chunk-*.txt; do
  idx=$((idx + 1))
  part_msg=$(cat "$f")

  if [ "$CHUNK_COUNT" -gt 1 ]; then
    part_msg="📊 WSB Digest（$idx/$CHUNK_COUNT）\n\n$part_msg"
  fi

  if "$OPENCLAW_BIN" message send --channel discord --target "$TARGET_CHANNEL_ID" --message "$part_msg" >> "$LOG_FILE" 2>&1; then
    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] ✅ Sent chunk $idx/$CHUNK_COUNT" >> "$LOG_FILE"
  else
    echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] ❌ Failed at chunk $idx/$CHUNK_COUNT" >> "$LOG_FILE"
    exit 1
  fi
done

echo "[$(date '+%Y-%m-%d %H:%M:%S %Z')] ✅ Digest sent completely ($CHUNK_COUNT chunk(s))" >> "$LOG_FILE"
