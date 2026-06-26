#!/usr/bin/env bash
# 知乎自动发布：在网页端直接发布（打开写文章页或使用已打开的编辑器页，填入标题和正文，点击发布）
# Usage:
#   bash publish_article.sh "文章标题" /path/to/body.md
#   cat body.md | bash publish_article.sh "文章标题" -
#
# 推荐（Browser Relay，耗时更短、不易超时）：
#   用户先在 Chrome 打开知乎写文章页并挂上 OpenClaw 扩展（Relay ON），再执行：
#   ZHIHU_ALREADY_ON_EDITOR=1 bash publish_article.sh "文章标题" /path/to/body.md
# 使用前请确保已在浏览器中登录知乎。

set -e
TITLE="${1:-}"
BODY_SRC="${2:-}"

CLI="openclaw browser"
ZHIHU_BASE="${ZHIHU_BASE:-https://www.zhihu.com}"
# 已在写文章/编辑器页时设为 1，跳过打开与点击「写文章」，直接填表+点击发布（参考 Browser Relay 用法）
SKIP_NAV="${ZHIHU_ALREADY_ON_EDITOR:-0}"

if [ -z "$TITLE" ]; then
  echo "用法: $0 \"文章标题\" <正文文件路径|->"
  exit 1
fi

# 读取正文
if [ -z "$BODY_SRC" ] || [ "$BODY_SRC" = "-" ]; then
  BODY=$(cat)
else
  [ ! -f "$BODY_SRC" ] && echo "正文文件不存在: $BODY_SRC" && exit 1
  BODY=$(cat "$BODY_SRC")
fi

echo "============================================"
echo "  知乎自动发布（网页端）"
echo "============================================"
echo "标题: $TITLE"
echo "正文长度: $(echo -n "$BODY" | wc -c) 字符"
echo ""

if [ "$SKIP_NAV" != "1" ]; then
  # 打开知乎创作中心（用户需已登录）
  echo "=== 打开知乎 ==="
  $CLI open "${ZHIHU_BASE}/creator" 2>/dev/null || $CLI open "${ZHIHU_BASE}" 2>/dev/null
  sleep 5

  SNAP=$($CLI snapshot 2>/dev/null)

  # 尝试点击「写文章」入口（多种可能文案）
  WRITE_REF=$(echo "$SNAP" | grep -oE '(写文章|写 文 章|发布文章|创作).*ref=e[0-9]+' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  [ -z "$WRITE_REF" ] && WRITE_REF=$(echo "$SNAP" | grep -E '写文章|写 文 章' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  [ -z "$WRITE_REF" ] && WRITE_REF=$(echo "$SNAP" | grep -i 'write\|文章' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')

  if [ -n "$WRITE_REF" ]; then
    echo "  点击写文章入口 ref=$WRITE_REF"
    $CLI click "$WRITE_REF" 2>/dev/null
    sleep 4
  fi
else
  echo "=== 使用当前页（已打开写文章页 / Browser Relay）==="
  sleep 1
fi

# 查找标题输入框（placeholder 常含「标题」或 input/textarea）
SNAP=$($CLI snapshot 2>/dev/null)
TITLE_REF=$(echo "$SNAP" | grep -E 'textbox|input|标题|placeholder.*标题' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
[ -z "$TITLE_REF" ] && TITLE_REF=$(echo "$SNAP" | grep -B0 -A0 '标题' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')

if [ -n "$TITLE_REF" ]; then
  echo "  填入标题 ref=$TITLE_REF"
  $CLI type "$TITLE_REF" "$TITLE" 2>/dev/null
  sleep 1
fi

# 查找正文编辑区（知乎多为 contenteditable 或 textarea）
BODY_REF=$(echo "$SNAP" | grep -E 'textbox|contenteditable|正文|编辑' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
[ -z "$BODY_REF" ] && BODY_REF=$(echo "$SNAP" | grep -E 'textarea|paragraph|富文本' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
# 若正文区在第二屏，再 snapshot 一次
[ -z "$BODY_REF" ] && SNAP=$($CLI snapshot 2>/dev/null) && BODY_REF=$(echo "$SNAP" | grep -E 'ref=e[0-9]+' | head -5 | tail -1 | grep -oE 'ref=e[0-9]+' | sed 's/ref=//')

if [ -n "$BODY_REF" ]; then
  echo "  填入正文 ref=$BODY_REF"
  # 正文较长时用 type 可能超时，只取前 8000 字符避免异常
  BODY_SHORT=$(echo "$BODY" | head -c 8000)
  $CLI type "$BODY_REF" "$BODY_SHORT" 2>/dev/null
  sleep 1
fi

# 发布按钮可能在页面下方，先滚动再查找
echo "=== 查找发布按钮 ==="
$CLI press "PageDown" 2>/dev/null || true
sleep 0.5
$CLI press "End" 2>/dev/null || true
sleep 0.5
SNAP=$($CLI snapshot 2>/dev/null)

PUBLISH_REF=$(echo "$SNAP" | grep -E '发布|发表|提交|Publish' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
[ -z "$PUBLISH_REF" ] && PUBLISH_REF=$(echo "$SNAP" | grep -i 'button.*发布\|发布.*button' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
[ -z "$PUBLISH_REF" ] && PUBLISH_REF=$(echo "$SNAP" | grep -B1 -E '发布|发表|提交' | grep -oE 'ref=e[0-9]+' | tail -1 | sed 's/ref=//')
[ -z "$PUBLISH_REF" ] && PUBLISH_REF=$(echo "$SNAP" | grep -E '发布文章|立即发布|确认发布' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
[ -z "$PUBLISH_REF" ] && PUBLISH_REF=$(echo "$SNAP" | grep -i 'cursor:pointer.*发布\|发布.*cursor:pointer' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')

if [ -n "$PUBLISH_REF" ]; then
  echo "  点击发布 ref=$PUBLISH_REF"
  $CLI click "$PUBLISH_REF" 2>/dev/null
  sleep 2
  echo ""
  echo "=== 完成 ==="
  echo "已点击发布。请在浏览器中确认是否成功（如弹窗、二次确认等）。"
else
  echo "  未找到发布按钮，尝试快捷键 Ctrl+Enter / Cmd+Enter"
  $CLI press "Control+Enter" 2>/dev/null || $CLI press "Meta+Enter" 2>/dev/null
  sleep 2
  SNAP2=$($CLI snapshot 2>/dev/null)
  PUBLISH_REF=$(echo "$SNAP2" | grep -E '发布|发表|提交' | grep -oE 'ref=e[0-9]+' | head -1 | sed 's/ref=//')
  if [ -n "$PUBLISH_REF" ]; then
    echo "  点击发布 ref=$PUBLISH_REF"
    $CLI click "$PUBLISH_REF" 2>/dev/null
    echo "=== 完成 ==="
  else
    echo "  仍未找到发布按钮。标题与正文应已填入，请在此页面手动点击「发布」或「发表」完成发布。"
  fi
fi
