#!/usr/bin/env bash
set -euo pipefail

SAGE_HOME="${SAGE_HOME:-$HOME/.sage}"
GROWTH_DIR="$SAGE_HOME/growth"

if [ ! -d "$SAGE_HOME" ]; then
  echo "[MISSING] $SAGE_HOME does not exist. Run init_sage.sh first." >&2
  exit 1
fi

mkdir -p "$GROWTH_DIR"

create_file() {
  local file="$1"
  local title="$2"
  if [ ! -f "$GROWTH_DIR/$file" ]; then
    printf "# %s\n\n- 待填写\n" "$title" > "$GROWTH_DIR/$file"
  fi
}

create_file "channels.md" "平台与渠道策略"
create_file "content-pillars.md" "内容支柱与栏目"
create_file "audience.md" "受众画像与关系分层"
create_file "experiments.md" "增长实验"
create_file "metrics.md" "增长指标与复盘"
create_file "monetization.md" "变现路径"

echo "[OK] Ensured growth extension at $GROWTH_DIR"

