#!/usr/bin/env bash
# surf_query skill 自動更新腳本
# 由 OpenClaw 每週維護 cron 呼叫，或手動執行

SKILL_DIR="$HOME/.openclaw/skills/surf_query"
REPO_URL="https://github.com/Harperbot/openclaw-surf-query"
CURRENT="$SKILL_DIR/surf_query.py"
REMOTE="$REPO_URL/raw/main/surf_query.py"

echo "[surf_query] 檢查更新..."

REMOTE_VER=$(curl -sf "$REMOTE" | grep -m1 '# version:' | awk '{print $3}')
LOCAL_VER=$(grep -m1 '# version:' "$CURRENT" 2>/dev/null | awk '{print $3}')

if [ -z "$REMOTE_VER" ]; then
  echo "[surf_query] ⚠️ 無法取得遠端版本，跳過"
  exit 0
fi

if [ "$LOCAL_VER" = "$REMOTE_VER" ]; then
  echo "[surf_query] ✅ 已是最新版（$LOCAL_VER）"
  exit 0
fi

echo "[surf_query] 發現新版本：$LOCAL_VER → $REMOTE_VER，開始更新..."
curl -sf "$REPO_URL/raw/main/surf_query.py" -o "$CURRENT.tmp" && \
  mv "$CURRENT.tmp" "$CURRENT" && \
  curl -sf "$REPO_URL/raw/main/skill.yml" -o "$SKILL_DIR/skill.yml.tmp" && \
  mv "$SKILL_DIR/skill.yml.tmp" "$SKILL_DIR/skill.yml" && \
  curl -sf "$REPO_URL/raw/main/taiwan_surf_spots.json" -o "$SKILL_DIR/taiwan_surf_spots.json.tmp" && \
  mv "$SKILL_DIR/taiwan_surf_spots.json.tmp" "$SKILL_DIR/taiwan_surf_spots.json"

echo "[surf_query] ✅ 更新完成（$REMOTE_VER）"
