#!/bin/bash
# ============================================================
# 小红书笔记自动发布（图文 + 视频，自动判断类型）
#
# 本脚本只做三件事：解析/校验参数 → 写参数文件 → 调用浏览器流程层。
# 浏览器流程在 publish_note.mjs，可用 `node --check` 单独校验。
#
# 退出码（与 SKILL.md「退出码与失败处理」一致）：
#   0   成功
#   10  参数错误（类型/数量/文件不存在）—— 无副作用，改参数重跑
#   11  依赖缺失（ego-browser / python3）
#   20  登录态失效 —— 在 ego-lite 手动登录后重跑
#   21  未进入上传页
#   30  素材上传/转码失败
#   40  填表失败（标题/正文/编辑器）
#   50  话题未挂载
#   60  封面设置失败
#   70  提交按钮不可用
#   80  提交后状态不确定（去笔记管理确认，不要立即重发）
#   90  内部未预期异常
# ============================================================

set -euo pipefail

# 只在 PATH 里确实找不到 ego-browser 时才追加，否则会静默顶掉调用方自选的版本，
# 让后面的 command -v 检查失去意义（审计时用桩替换 ego-browser 就被这行顶掉过）。
command -v ego-browser >/dev/null 2>&1 || export PATH="$HOME/.local/bin:$PATH"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
MJS="$SCRIPT_DIR/publish_note.mjs"
PARAMS_FILE="/tmp/xhs_publish_params.json"
RUN_ID="$(date +%Y%m%d-%H%M%S)-$$"
LOG_FILE="/tmp/xhs-publish-${RUN_ID}.log"

# ---- 参数（支持 env 传入或直接改本文件）----
MEDIA_DIR="${MEDIA_DIR:-${IMAGE_DIR:-}}"
MEDIA_FILES="${MEDIA_FILES:-${IMAGES:-}}"
TITLE="${TITLE:-}"
BODY="${BODY:-}"
TOPICS="${TOPICS:-}"
MODE="${MODE:-publish}"
MEDIA_TYPE="${MEDIA_TYPE:-auto}"
COVER_IMAGE="${COVER_IMAGE:-}"
KEEP_ON_FAIL="${KEEP_ON_FAIL:-1}"

die() {  # die <exit_code> <code> <message> <hint...>
  local code="$1" ecode="$2" msg="$3"
  shift 3
  echo "" >&2
  echo "=== FAILED ===" >&2
  echo "step     : precheck" >&2
  echo "code     : $ecode" >&2
  echo "exit     : $code" >&2
  echo "message  : $msg" >&2
  echo "what_now :" >&2
  local i=1
  for h in "$@"; do echo "  $i. $h" >&2; i=$((i + 1)); done
  echo "=== END FAILED ===" >&2
  exit "$code"
}

# ---- 依赖检查 ----
command -v ego-browser >/dev/null 2>&1 || die 11 E_DEP_EGO_BROWSER "ego-browser 未安装或不在 PATH" \
  "安装 ego-lite：sh ~/.workbuddy/skills/ego-browser/scripts/install.sh" \
  "装完确认 ego-browser --version 能输出版本号"

command -v python3 >/dev/null 2>&1 || die 11 E_DEP_PYTHON "找不到 python3" \
  "安装 Python 3.8+（macOS 自带，Linux: apt install python3）"

[ -f "$MJS" ] || die 11 E_DEP_MJS "同目录下缺少 publish_note.mjs" \
  "脚本被拆成 publish_note.sh + publish_note.mjs 两个文件，必须保持在同一目录" \
  "重新拷贝整个 scripts/ 目录，不要只拷 .sh"

# ---- 参数校验 ----
[ -n "$MEDIA_DIR" ] && [ -n "$MEDIA_FILES" ] && [ -n "$TITLE" ] && [ -n "$BODY" ] \
  || die 10 E_PARAM_MISSING "缺少必填参数 MEDIA_DIR / MEDIA_FILES / TITLE / BODY" \
    "最少需要：MEDIA_DIR（绝对路径）、MEDIA_FILES（文件名，逗号分隔）、TITLE、BODY"

case "$MODE" in
  publish|draft|stage) ;;
  *) die 10 E_PARAM_MODE "MODE 取值非法：$MODE" "只能是 publish / draft / stage" ;;
esac

case "$MEDIA_TYPE" in
  auto|image|video) ;;
  *) die 10 E_PARAM_MEDIA_TYPE "MEDIA_TYPE 取值非法：$MEDIA_TYPE" "只能是 auto / image / video" ;;
esac

case "$TITLE" in
  *"'"*) die 10 E_PARAM_TITLE_QUOTE "TITLE 含单引号，会破坏注入到 JS 的字符串" \
    "把单引号换成「」或直接去掉" ;;
esac

case "$BODY" in
  *'`'*) die 10 E_PARAM_BODY_BACKTICK "BODY 含反引号，会破坏 JS 模板字符串" "去掉反引号，或改用「」" ;;
  *'${'*) die 10 E_PARAM_BODY_DOLLAR "BODY 含 \${，会被当作模板变量" "把 \$ 去掉或改成全角" ;;
esac

case "$TOPICS" in
  *'#'*) echo "WARN: TOPICS 不需要带 #，脚本会自动补；本次会忽略多余的 #" >&2 ;;
esac

[ -d "$MEDIA_DIR" ] || die 10 E_PARAM_DIR_NOT_FOUND "素材目录不存在：$MEDIA_DIR" \
  "MEDIA_DIR 必须是绝对路径且目录真实存在"

# ---- 判断类型 + 生成参数文件 ----
RESOLVED_TYPE=$(python3 - "$MEDIA_DIR" "$MEDIA_FILES" "$TITLE" "$BODY" "$TOPICS" "$MODE" "$MEDIA_TYPE" "$COVER_IMAGE" "$KEEP_ON_FAIL" "$RUN_ID" "$LOG_FILE" "$PARAMS_FILE" <<'PYEOF'
import json, os, sys

(media_dir, files_str, title, body, topics_str,
 mode, forced_type, cover_image, keep_on_fail, run_id, log_file, path) = sys.argv[1:13]

VIDEO_EXT = {'.mp4', '.mov', '.flv', '.f4v', '.mkv', '.rm', '.rmvb', '.m4v', '.mpg', '.mpeg', '.ts'}
IMAGE_EXT = {'.png', '.jpg', '.jpeg', '.webp', '.heic', '.bmp'}

files = [s.strip() for s in files_str.split(',') if s.strip()]
forced_type = (forced_type or 'auto').strip().lower()
exts = [os.path.splitext(f)[1].lower() for f in files]

if forced_type in ('image', 'video'):
    media_type = forced_type
elif exts and all(e in VIDEO_EXT for e in exts):
    media_type = 'video'
elif exts and all(e in IMAGE_EXT for e in exts):
    media_type = 'image'
else:
    media_type = 'unknown'

err = None
missing = [f for f in files if not os.path.isfile(os.path.join(media_dir, f))]

if media_type == 'unknown':
    err = 'E_MEDIA_TYPE_UNKNOWN: 无法从扩展名判断类型。视频支持 %s，图片支持 %s；也可显式设置 MEDIA_TYPE' % (
        '/'.join(sorted(VIDEO_EXT)), '/'.join(sorted(IMAGE_EXT)))
elif missing:
    err = 'E_MEDIA_FILE_MISSING: 文件不存在 -> %s' % ', '.join(missing)
elif media_type == 'video' and len(files) != 1:
    err = 'E_MEDIA_VIDEO_COUNT: 视频笔记一次只能发 1 个文件，当前 %d 个' % len(files)
elif media_type == 'image' and len(files) > 18:
    err = 'E_MEDIA_IMAGE_COUNT: 图文笔记最多 18 张，当前 %d 张' % len(files)

cover = (cover_image or '').strip()
# 图文笔记没有封面概念，先置空再校验。原来的顺序把文件检查放在前面，
# 「图文 + 一个不存在的 COVER_IMAGE」会直接 E_COVER_NOT_FOUND / exit 10，
# 而文档承诺的是「图文模式忽略该参数」。
if cover and media_type != 'video':
    cover = ''
if cover and not err:
    if not os.path.isfile(cover):
        err = 'E_COVER_NOT_FOUND: COVER_IMAGE 文件不存在 -> %s' % cover
    elif os.path.splitext(cover)[1].lower() not in IMAGE_EXT:
        err = 'E_COVER_NOT_IMAGE: COVER_IMAGE 必须是图片（%s），当前 %s' % (
            '/'.join(sorted(IMAGE_EXT)), cover)

params = {
    "runId": run_id,
    "logFile": log_file,
    "mediaDir": media_dir,
    "files": files,
    "mediaType": media_type,
    "title": title,
    "body": body,
    "topics": [t.strip().lstrip('#') for t in topics_str.split(',') if t.strip()],
    "mode": mode,
    "coverImage": cover,
    "keepOnFail": str(keep_on_fail).strip() not in ('0', 'false', 'no'),
    "error": err,
}
with open(path, 'w', encoding='utf-8') as f:
    json.dump(params, f, ensure_ascii=False)

print(media_type)
if err:
    print(err, file=sys.stderr)
PYEOF
)

[ -f "$PARAMS_FILE" ] || die 10 E_PARAM_WRITE "参数文件生成失败：$PARAMS_FILE" \
  "检查 /tmp 是否可写、python3 是否正常"

if [ "$RESOLVED_TYPE" = "unknown" ]; then
  die 10 E_MEDIA_TYPE_UNKNOWN "无法判断素材类型" \
    "视频支持 mp4/mov/flv/mkv 等；图片支持 png/jpg/webp 等" \
    "也可显式指定 MEDIA_TYPE=image 或 MEDIA_TYPE=video"
fi

# python 侧其它校验（文件缺失/数量/封面）也在这里兜住
PARAM_ERR=$(python3 -c "
import json
d = json.load(open('$PARAMS_FILE', encoding='utf-8'))
print(d.get('error') or '')
" 2>/dev/null || true)
if [ -n "$PARAM_ERR" ]; then
  MSG="${PARAM_ERR#*: }"
  CODE="${PARAM_ERR%%:*}"
  die 10 "$CODE" "$MSG" "修正后重跑；本次没有启动浏览器，不产生任何副作用"
fi

IFS=',' read -ra FILE_ARRAY <<< "$MEDIA_FILES"

# ---- 开跑 ----
{
  echo "run      : $RUN_ID"
  echo "start    : $(date '+%Y-%m-%d %H:%M:%S')"
  echo "type     : $RESOLVED_TYPE"
  echo "files    : $MEDIA_FILES"
  echo "title    : $TITLE"
  echo "topics   : $TOPICS"
  echo "mode     : $MODE"
  echo "cover    : ${COVER_IMAGE:-（默认第一帧）}"
  echo "params   : $PARAMS_FILE"
  echo "---"
} > "$LOG_FILE"

echo "=========================================="
echo "小红书笔记自动发布"
if [ "$RESOLVED_TYPE" = "video" ]; then
  echo "  类型: video（视频笔记）"
else
  echo "  类型: image（图文笔记）"
fi
echo "  素材目录: $MEDIA_DIR"
echo "  文件数量: ${#FILE_ARRAY[@]}"
echo "  标题: $TITLE"
[ -n "$TOPICS" ] && echo "  话题: $TOPICS"
if [ "$RESOLVED_TYPE" = "video" ]; then
  echo "  封面: ${COVER_IMAGE:-默认（视频第一帧）}"
elif [ -n "$COVER_IMAGE" ]; then
  echo "  封面: 忽略（COVER_IMAGE 仅对视频笔记生效）"
fi
echo "  模式: $MODE"
echo "  日志: $LOG_FILE"
echo "=========================================="
echo ""

# ---- 调用浏览器流程层 ----
# 开启 set -e 后，浏览器非零退出会直接终止脚本、跳过下面的汇总，
# 所以用 `|| EXIT_CODE=$?` 显式接住，既保留 -e 的快速失败，也保留失败汇报。
EXIT_CODE=0
ego-browser nodejs < "$MJS" || EXIT_CODE=$?

echo ""
echo "=========================================="
if [ "$EXIT_CODE" -eq 0 ]; then
  echo "结果: 成功（exit 0）"
else
  echo "结果: 失败（exit ${EXIT_CODE}），按上面 what_now 处理"
fi
echo "日志: $LOG_FILE"
echo "=========================================="

exit "$EXIT_CODE"
