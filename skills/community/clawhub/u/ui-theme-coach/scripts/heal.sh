#!/bin/bash
# 升级自愈脚本：检测 Control UI 主题注入是否丢失，丢失则从快照恢复；支持卸载
#
# 用法：
#   heal.sh [theme]           自愈模式：目标主题缺失则注入；同主题跳过；检测到装了别的主题则报出
#   heal.sh [theme] --force   强制模式：先验目标快照（缺失/契约违反直接报错退出，不动现有主题），
#                             再卸载当前已注入的主题、注入目标主题
#   heal.sh uninstall [theme] 卸载模式：移除主题注入块（theme 省略 = 卸载当前检测到的主题）
#
# 环境变量（可选覆盖，解决「安装路径不固定」问题）：
#   OPENCLAW_INDEX          index.html 完整路径（默认自动探测 OpenClaw 安装路径）
#   OPENCLAW_UPSTREAM       当前 dist 上游版本（默认从 openclaw package.json 读；测试/特殊环境可用）
#   THEME_SNAPSHOTS_ROOT    快照根目录（默认 ~/.openclaw/workspace/theme-coach/snapshot）
#
# 快照契约：快照目录必须含 theme-vars.html（含 <style data-theme-id=...> 块）和
# injector.html（含 <script data-theme-id=...> 块），指纹 = data-theme-id + data-theme-version；
# 注入块还应带 data-upstream-version（注入时的 dist 上游版本）。重注入前与当前 dist 比对，
# 主版本跳大先警告再注入（DOM/CSS 钩子可能已变，注入后需人工验证）。
# 版本判定示例：2026.7.1-2 → 主版本 2026；1.2.0 → 1；非数字开头 → 跳过比对。

set -euo pipefail

usage() {
  cat <<'EOF'
用法：
  heal.sh [theme]           自愈模式：目标主题缺失则注入；同主题跳过；检测到装了别的主题则报出
  heal.sh [theme] --force   强制模式：先卸载当前已注入的主题，再注入目标主题
  heal.sh uninstall [theme] 卸载模式：移除主题注入块（theme 省略 = 卸载当前检测到的主题）
EOF
  exit 1
}

# ---------- 1. 动态探测 index.html 路径（不硬编码安装路径） ----------
detect_index() {
  if [ -n "${OPENCLAW_INDEX:-}" ]; then
    if [ ! -f "$OPENCLAW_INDEX" ]; then
      echo "[heal] ERROR: OPENCLAW_INDEX 指定的文件不存在: $OPENCLAW_INDEX" >&2
      exit 1
    fi
    echo "$OPENCLAW_INDEX"
    return
  fi

  local candidates=() bin real root
  # a) 从 openclaw 命令位置反推（覆盖 npx/pnpm/yarn 全局安装的软链场景）
  if bin="$(command -v openclaw 2>/dev/null || true)" && [ -n "$bin" ]; then
    real="$(readlink -f "$bin" 2>/dev/null || echo "$bin")"
    candidates+=("$(dirname "$real")/dist/control-ui/index.html")
  fi
  # b) npm 全局根目录（不同 npm 配置下 root -g 会变）
  if command -v npm >/dev/null 2>&1; then
    root="$(npm root -g 2>/dev/null || true)"
    [ -n "$root" ] && candidates+=("$root/openclaw/dist/control-ui/index.html")
  fi
  # c) 兜底：常见固定位置
  candidates+=("$HOME/.openclaw/workspace/dist/control-ui/index.html" "/usr/lib/node_modules/openclaw/dist/control-ui/index.html")

  local c
  for c in "${candidates[@]}"; do
    if [ -f "$c" ]; then
      echo "$c"
      return
    fi
  done

  echo "[heal] ERROR: 找不到 dist/control-ui/index.html，已尝试：" >&2
  for c in "${candidates[@]}"; do echo "[heal]   - $c" >&2; done
  echo "[heal]        请用 OPENCLAW_INDEX=/path/to/index.html 显式指定。" >&2
  exit 1
}

# ---------- 2. 指纹识别：index.html 里当前装的是哪个主题 ----------
# 契约：注入块携带 data-theme-id="<主题名>"（新版）+ data-theme-version="<版本>"。
# 兼容旧注入格式：id="<主题名>-theme"。
detect_current_theme() {
  local index="$1" m
  m="$(grep -o 'data-theme-id="[^"]*"' "$index" 2>/dev/null | head -1 || true)"
  if [ -n "$m" ]; then
    m="${m#data-theme-id=\"}"; m="${m%\"}"
    echo "$m"; return
  fi
  m="$(grep -o 'id="[^"]*-theme"' "$index" 2>/dev/null | head -1 || true)"
  if [ -n "$m" ]; then
    m="${m#id=\"}"; m="${m%-theme\"}"
    echo "$m"; return
  fi
  echo ""
}

detect_current_version() {
  local index="$1" m
  m="$(grep -o 'data-theme-version="[^"]*"' "$index" 2>/dev/null | head -1 || true)"
  [ -z "$m" ] && { echo ""; return; }
  m="${m#data-theme-version=\"}"; m="${m%\"}"
  echo "$m"
}

# ---------- 2b. 上游 dist 版本探测（重注入前比对用） ----------
detect_upstream_version() {
  local index="$1" root p ver bin real
  if [ -n "${OPENCLAW_UPSTREAM:-}" ]; then
    echo "$OPENCLAW_UPSTREAM"; return
  fi
  # index.html 位于 <openclaw root>/dist/control-ui/ → package.json 在 <openclaw root>/
  root="$(dirname "$(dirname "$(dirname "$index")")")"
  local candidates=("$root/package.json")
  if bin="$(command -v openclaw 2>/dev/null || true)" && [ -n "$bin" ]; then
    real="$(readlink -f "$bin" 2>/dev/null || echo "$bin")"
    candidates+=("$(dirname "$real")/package.json")
  fi
  for p in "${candidates[@]}"; do
    [ -f "$p" ] || continue
    ver="$(python3 -c 'import json,sys;print(json.load(open(sys.argv[1],encoding="utf-8")).get("version",""))' "$p" 2>/dev/null || true)"
    [ -n "$ver" ] && { echo "$ver"; return; }
  done
  echo ""
}

detect_recorded_upstream() {
  local f="$1" m
  m="$(grep -o 'data-upstream-version="[^"]*"' "$f" 2>/dev/null | head -1 || true)"
  [ -z "$m" ] && { echo ""; return; }
  m="${m#data-upstream-version=\"}"; m="${m%\"}"
  echo "$m"
}

version_major() {
  # "2026.7.1-2" → 2026；"1.2.0" → 1；非数字开头 → ""
  echo "${1%%[!0-9]*}"
}

# ---------- 5. 上游版本比对（重注入前：主版本跳大先警告再注入） ----------
check_upstream_version() {
  local index="$1" snap_tv="$2" upstream recorded maj_c maj_r
  upstream="$(detect_upstream_version "$index")"
  recorded="$(detect_recorded_upstream "$snap_tv")"
  if [ -z "$recorded" ]; then
    echo "[heal] INFO: snapshot has no data-upstream-version (old snapshot); skipping upstream version check."
    return
  fi
  if [ -z "$upstream" ]; then
    echo "[heal] INFO: cannot detect current dist upstream version; skipping version check."
    return
  fi
  echo "[heal] upstream dist version: snapshot recorded=$recorded, current=$upstream"
  maj_c="$(version_major "$upstream")"
  maj_r="$(version_major "$recorded")"
  if [ -n "$maj_c" ] && [ -n "$maj_r" ]; then
    if [ "$maj_c" != "$maj_r" ]; then
      echo "[heal] WARN: upstream dist MAJOR version changed ($recorded -> $upstream)."
      echo "[heal]       DOM/CSS hooks may have changed; re-injecting anyway, then verify visually."
      echo "[heal]       If the theme looks broken, re-create the snapshot against the new dist."
    else
      echo "[heal] INFO: same major version ($maj_c), DOM hooks likely intact."
    fi
  else
    echo "[heal] INFO: version format unrecognized, skipping major-jump check."
  fi
}

backup_index() {
  local index="$1" bak
  bak="${index}.bak-heal-$(date +%s)"
  cp "$index" "$bak"
  echo "[heal] Backed up: $bak"
}

# ---------- 3a. 快照契约先验（卸载/备份之前跑：目录在 + 契约文件全 + 指纹匹配） ----------
validate_snapshot() {
  local snapdir="$1" theme="$2" tv inj snap_theme missing=""
  if [ ! -d "$snapdir" ]; then
    echo "[heal] ERROR: No snapshot found for theme '$theme' at $snapdir" >&2
    echo "[heal]       Create it first (theme-vars.html + injector.html, see SKILL.md 3.2), or pick another theme." >&2
    exit 1
  fi
  tv="$snapdir/theme-vars.html"
  inj="$snapdir/injector.html"
  [ -f "$tv" ]  || missing="$tv"
  [ -f "$inj" ] || missing="$missing${missing:+ }$inj"
  if [ -n "$missing" ]; then
    echo "[heal] ERROR: snapshot incomplete: missing $missing" >&2
    exit 1
  fi
  # 契约：theme-vars.html 与 injector.html 必须声明与目标主题一致的指纹，防止拿错主题灌错
  for f in "$tv" "$inj"; do
    snap_theme="$(grep -o 'data-theme-id="[^"]*"' "$f" 2>/dev/null | head -1 || true)"
    snap_theme="${snap_theme#data-theme-id=\"}"; snap_theme="${snap_theme%\"}"
    if [ "$snap_theme" != "$theme" ]; then
      echo "[heal] ERROR: snapshot contract violation: $(basename "$f") declares theme='${snap_theme:-<none>}', expected '$theme'." >&2
      exit 1
    fi
  done
  echo "[heal] OK: snapshot for '$theme' validated (directory + theme-vars.html + injector.html + fingerprint match)."
}

# ---------- 3. 卸载：移除携带该主题指纹的注入块 ----------
uninstall_theme() {
  local index="$1" theme="$2"
  if [ -z "$theme" ]; then
    theme="$(detect_current_theme "$index")"
    if [ -z "$theme" ]; then
      echo "[heal] Nothing to uninstall: no injected theme found (no theme fingerprint in index.html)."
      exit 0
    fi
  fi
  if [ "$(detect_current_theme "$index")" != "$theme" ]; then
    echo "[heal] ERROR: theme '$theme' not found in index.html (current: '$(detect_current_theme "$index")')."
    exit 1
  fi

  backup_index "$index"
  python3 - "$index" "$theme" <<'PY'
import pathlib, re, sys
index, theme = sys.argv[1], sys.argv[2]
html = pathlib.Path(index).read_text()
pat_style = re.compile(r'<style\b[^>]*data-theme-id="%s"[^>]*>.*?</style>\n?' % re.escape(theme), re.S)
pat_script = re.compile(r'<script\b[^>]*data-theme-id="%s"[^>]*>.*?</script>\n?' % re.escape(theme), re.S)
removed = len(pat_style.findall(html)) + len(pat_script.findall(html))
new = pat_style.sub('', html)
new = pat_script.sub('', new)
pathlib.Path(index).write_text(new)
print('[heal] Uninstalled theme "%s": removed %d injection block(s).' % (theme, removed))
PY
  [ "${3:-}" = "quiet" ] || echo "[heal] Done. Ctrl+Shift+R to see the original UI."
}

# ---------- 4. 注入：从快照恢复到 index.html ----------
inject_theme() {
  local index="$1" theme="$2" snapdir="$3"
  local tv inj
  tv="$snapdir/theme-vars.html"
  inj="$snapdir/injector.html"
  for f in "$tv" "$inj"; do
    if [ ! -f "$f" ]; then
      echo "[heal] ERROR: snapshot incomplete: missing $f" >&2
      exit 1
    fi
  done

  # 快照契约自检：theme-vars 必须声明与目标主题一致的指纹，防止拿错主题灌错
  local snap_theme
  snap_theme="$(grep -o 'data-theme-id="[^"]*"' "$tv" 2>/dev/null | head -1 || true)"
  snap_theme="${snap_theme#data-theme-id=\"}"; snap_theme="${snap_theme%\"}"
  if [ "$snap_theme" != "$theme" ]; then
    echo "[heal] ERROR: snapshot contract violation: theme-vars.html declares theme='${snap_theme:-<none>}', expected '$theme'." >&2
    exit 1
  fi

  python3 - "$index" "$tv" "$inj" <<'PY'
import pathlib, sys
index, tv, inj = sys.argv[1], sys.argv[2], sys.argv[3]
html = pathlib.Path(index).read_text()
tv_text = pathlib.Path(tv).read_text()   # 快照文件以 \n 结尾，直接拼
inj_text = pathlib.Path(inj).read_text()
html = html.replace('</head>', tv_text + '</head>')
html = html.replace('</body>', inj_text + '</body>')
pathlib.Path(index).write_text(html)
print('[heal] Re-injection complete')
PY
}

# ---------- 主流程 ----------
if [ "${1:-}" = "-h" ] || [ "${1:-}" = "--help" ]; then
  usage
fi

MODE="heal"
THEME=""
if [ "${1:-}" = "uninstall" ]; then
  MODE="uninstall"
  shift
  THEME="${1:-}"
else
  THEME="${1:-mc}"
fi

FORCE=0
if [ "$MODE" = "heal" ] && [ "${2:-}" = "--force" ]; then
  FORCE=1
fi

INDEX="$(detect_index)"
echo "[heal] index.html: $INDEX"
SNAPSHOTS_ROOT="${THEME_SNAPSHOTS_ROOT:-$HOME/.openclaw/workspace/theme-coach/snapshot}"
SNAPDIR="$SNAPSHOTS_ROOT/$THEME"

if [ "$MODE" = "uninstall" ]; then
  uninstall_theme "$INDEX" "$THEME"
  exit 0
fi

CURRENT="$(detect_current_theme "$INDEX")"
if [ -n "$CURRENT" ]; then
  if [ "$CURRENT" = "$THEME" ]; then
    echo "[heal] Theme '$THEME' is present (version $(detect_current_version "$INDEX")), skipping."
    exit 0
  fi
  if [ "$FORCE" = "0" ]; then
    echo "[heal] WARN: a different theme '$CURRENT' is currently installed."
    echo "[heal]       Run '$0 uninstall $CURRENT' first, or re-run with --force to replace it with '$THEME'."
    exit 1
  fi
  echo "[heal] Replacing installed theme '$CURRENT' with '$THEME' (--force)..."
fi

# 先验目标快照（存在 + 契约完整 + 指纹匹配）：--force 场景下必须在卸载旧主题
# 之前跑——目标快照缺失直接报错退出（exit 非 0），现有主题原样不动。
# 契约检查同时挪到 backup_index 之前，契约违反不再白备份一次。
validate_snapshot "$SNAPDIR" "$THEME"

check_upstream_version "$INDEX" "$SNAPDIR/theme-vars.html"

if [ -n "$CURRENT" ]; then
  uninstall_theme "$INDEX" "$CURRENT" quiet
fi

if [ -n "$CURRENT" ]; then
  echo "[heal] Injecting theme '$THEME' from snapshot..."
else
  echo "[heal] Theme '$THEME' missing! Re-injecting from snapshot..."
fi

backup_index "$INDEX"
inject_theme "$INDEX" "$THEME" "$SNAPDIR"

echo "[heal] Done! Theme '$THEME' has been restored."
echo "[heal] Remember to Ctrl+Shift+R to see changes."
