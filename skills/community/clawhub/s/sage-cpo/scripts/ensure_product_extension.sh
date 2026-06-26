#!/usr/bin/env bash
set -euo pipefail

SAGE_HOME="${SAGE_HOME:-$HOME/.sage}"
PRODUCT_DIR="$SAGE_HOME/product"

if [ ! -d "$SAGE_HOME" ]; then
  echo "[MISSING] $SAGE_HOME does not exist. Run init_sage.sh first." >&2
  exit 1
fi

mkdir -p "$PRODUCT_DIR"

create_file() {
  local file="$1"
  local title="$2"
  if [ ! -f "$PRODUCT_DIR/$file" ]; then
    printf "# %s\n\n- 待填写\n" "$title" > "$PRODUCT_DIR/$file"
  fi
}

create_file "users.md" "用户与 JTBD"
create_file "feedback.md" "用户反馈与需求信号"
create_file "roadmap.md" "产品路线图"
create_file "experiments.md" "产品实验"
create_file "metrics.md" "产品指标与 PMF 信号"
create_file "packaging.md" "服务产品化与套餐"
create_file "open-questions.md" "产品待确认问题"

echo "[OK] Ensured product extension at $PRODUCT_DIR"

