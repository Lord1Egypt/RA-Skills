#!/usr/bin/env bash
# injector.sh — 把 inject.css/inject.js 注入目标 HTML，启动本地 server，输出 *.annotated.html 并打开浏览器
#
# 用法:
#   ./injector.sh <input.html>           # 注入并打开
#   ./injector.sh <input.html> --no-open # 注入但不打开浏览器（CI/测试用）

set -euo pipefail

# ---------- 配置 ----------
RL_PORT="${RL_PORT:-7893}"
RL_HOME="${RL_HOME:-$HOME/.claude/redline}"
PIDFILE="$RL_HOME/server.pid"
LOGFILE="$RL_HOME/server.log"

# ---------- 参数解析 ----------
if [[ $# -lt 1 ]]; then
  echo "用法: $0 <html-file> [--no-open]" >&2
  exit 1
fi

INPUT="$1"
OPEN_BROWSER=1
[[ "${2:-}" == "--no-open" ]] && OPEN_BROWSER=0

if [[ ! -f "$INPUT" ]]; then
  echo "错误: 文件不存在: $INPUT" >&2
  exit 1
fi

# ---------- 路径解析 ----------
SOURCE="${BASH_SOURCE[0]}"
while [[ -h "$SOURCE" ]]; do
  DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"
  SOURCE="$(readlink "$SOURCE")"
  [[ $SOURCE != /* ]] && SOURCE="$DIR/$SOURCE"
done
SCRIPT_DIR="$(cd -P "$(dirname "$SOURCE")" && pwd)"

CSS_FILE="$SCRIPT_DIR/inject.css"
JS_FILE="$SCRIPT_DIR/inject.js"
SERVER_PY="$SCRIPT_DIR/server.py"

for f in "$CSS_FILE" "$JS_FILE" "$SERVER_PY"; do
  if [[ ! -f "$f" ]]; then
    echo "错误: 缺失资源文件: $f" >&2
    exit 1
  fi
done

# ---------- 启动/复用 server ----------
mkdir -p "$RL_HOME"

server_alive() {
  [[ -f "$PIDFILE" ]] || return 1
  local pid
  pid=$(cat "$PIDFILE" 2>/dev/null) || return 1
  [[ -n "$pid" ]] && kill -0 "$pid" 2>/dev/null
}

if server_alive; then
  echo "✓ server 已在运行 (pid=$(cat "$PIDFILE"), port=$RL_PORT)"
else
  rm -f "$PIDFILE"
  nohup python3 "$SERVER_PY" "$RL_PORT" > "$LOGFILE" 2>&1 &
  SERVER_PID=$!
  echo "$SERVER_PID" > "$PIDFILE"
  # 给 server 一点时间起来；最多等 1 秒
  for _ in 1 2 3 4 5 6 7 8 9 10; do
    if curl -fs "http://127.0.0.1:$RL_PORT/ping" >/dev/null 2>&1; then
      break
    fi
    sleep 0.1
  done
  if curl -fs "http://127.0.0.1:$RL_PORT/ping" >/dev/null 2>&1; then
    echo "✓ server 已启动 (pid=$SERVER_PID, port=$RL_PORT)"
  else
    echo "⚠ server 启动可能失败，详见 $LOGFILE" >&2
  fi
fi

# ---------- 输出路径 & inbox 路径 ----------
INPUT_ABS="$(cd "$(dirname "$INPUT")" && pwd)/$(basename "$INPUT")"
INPUT_DIR="$(dirname "$INPUT_ABS")"
INPUT_BASE="$(basename "$INPUT_ABS")"

if [[ "$INPUT_BASE" == *.annotated.html ]]; then
  OUTPUT="$INPUT_ABS"
  ORIGINAL_NAME="${INPUT_BASE%.annotated.html}.html"
elif [[ "$INPUT_BASE" == *.html ]]; then
  OUTPUT="$INPUT_DIR/${INPUT_BASE%.html}.annotated.html"
  ORIGINAL_NAME="$INPUT_BASE"
else
  OUTPUT="$INPUT_DIR/${INPUT_BASE}.annotated.html"
  ORIGINAL_NAME="$INPUT_BASE"
fi

# inbox 落在用户调用 injector.sh 时的 cwd（不是 HTML 所在目录）
# 这样 hook 在 cwd 检查时能匹配到
INBOX_PATH="${RL_INBOX:-$PWD/.redline-inbox.json}"

# ---------- 构造注入块 ----------
# 1) 配置块（端口、inbox 路径、源文件名）
# 2) <style> + <script>（来自 inject.css / inject.js）
CONFIG_JSON=$(python3 -c "
import json, sys
print(json.dumps({
    'port': int('$RL_PORT'),
    'inbox': '$INBOX_PATH',
    'file': '$ORIGINAL_NAME',
}, ensure_ascii=False))
")

# ---------- 注入 ----------
awk \
  -v css_file="$CSS_FILE" \
  -v js_file="$JS_FILE" \
  -v config="$CONFIG_JSON" '
function read_file(path,    line, content) {
    content = ""
    while ((getline line < path) > 0) {
        content = content line "\n"
    }
    close(path)
    return content
}
BEGIN {
    css = read_file(css_file)
    js  = read_file(js_file)
    injection = "<!-- redline: injected -->\n" \
                "<style data-rl-ui=\"1\">\n" css "</style>\n" \
                "<script data-rl-ui=\"1\">window.__RL_CONFIG__ = " config ";</script>\n" \
                "<script data-rl-ui=\"1\">\n" js "</script>\n" \
                "<!-- /redline -->\n"
    injected = 0
}
{
    if (!injected && match($0, /<\/body>/)) {
        before = substr($0, 1, RSTART - 1)
        after  = substr($0, RSTART)
        if (before != "") print before
        printf "%s", injection
        print after
        injected = 1
        next
    }
    print
}
END {
    if (!injected) {
        printf "%s", injection
    }
}
' "$INPUT_ABS" > "$OUTPUT"

echo "✓ 已生成: $OUTPUT"
echo "  inbox 路径: $INBOX_PATH"

# ---------- 打开浏览器 ----------
if [[ $OPEN_BROWSER -eq 1 ]]; then
  if command -v open >/dev/null 2>&1; then
    open "$OUTPUT"
  elif command -v xdg-open >/dev/null 2>&1; then
    xdg-open "$OUTPUT"
  else
    echo "提示: 未找到 open/xdg-open，请手动在浏览器打开: $OUTPUT"
  fi
fi

cat <<EOF

下一步:
  1. 在浏览器里点右上角 "✏️ 标注模式"
  2. 点击页面元素 → 写评论 → 保存
  3. 点 "📤 提交反馈" — 直接 POST 到 server，无需复制
  4. 回 Claude Code 随便说一句话，hook 会自动注入反馈触发 apply
EOF
