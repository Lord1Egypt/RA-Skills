#!/usr/bin/env bash
# yt2podcast: 建 job + 起后台 worker
#
# 用法:
#   new-job.sh <youtube_url> [选项]
#
# 选项:
#   --title <标题>          中文播客名(给 agent 用);不给就用 YouTube 原标题
#   --description <简介>    中文简介;不给就用 NotebookLM 源摘要兜底
#   --session-key <key>     完成后唤醒哪个会话,例如 agent:main:openclaw-weixin:direct:xxx
#   --podcast <id>          小宇宙节目 id(必填,或设 YT2PODCAST_PODCAST_ID)
#   --publish               上传后调用平台"发布"接口。需同时设置 YT2PODCAST_ALLOW_PUBLISH=1,
#                           否则直接报错退出——公开不可撤销,必须显式授权
#   --hold-upload           生成完先停下等确认(默认是一条龙:直接上传)
#   --draft                 显式指定草稿(默认行为)
#   --retry                 已有 job 是 failed 时,重置并重跑
#
# 说明:本脚本只负责建 job 文件,**不启动 worker**。建完用:
#   python3 scripts/worker.py <job_id>
# 由调用方(agent/宿主)以后台任务方式托管;这样 worker 生命周期不会超出宿主,
# 也不会出现"脱离管理的孤儿进程"。
#
# 输出:一行 JSON,便于 agent 解析。
#
# 环境变量:
#   YT2PODCAST_ROOT       根目录,默认 ~/.openclaw/workspace/yt2podcast
#   YT2PODCAST_PODCAST_ID 小宇宙节目 id(等价的 --podcast 默认值)
#   YT2PODCAST_PROXY      访问 Google 用的 HTTP 代理(worker 侧也会自动读系统代理)
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
WORKER="$SCRIPT_DIR/worker.py"
ROOT="${YT2PODCAST_ROOT:-$HOME/.openclaw/workspace/yt2podcast}"
JOBS_DIR="$ROOT/jobs"
DEFAULT_PODCAST_ID="${YT2PODCAST_PODCAST_ID:-}"

URL=""
TITLE=""
DESCRIPTION=""
SESSION_KEY=""
PODCAST_ID="$DEFAULT_PODCAST_ID"
DRAFT=1
AUTO_UPLOAD=1
HOLD_UPLOAD=0
RETRY=0
START=0

usage() {
  sed -n '2,22p' "${BASH_SOURCE[0]}" | sed 's/^# \{0,1\}//'
}

die() {
  printf '{"ok":false,"error":%s}\n' "$(python3 -c 'import json,sys; print(json.dumps(sys.argv[1], ensure_ascii=False))' "$1")" >&2
  exit 1
}

while [ $# -gt 0 ]; do
  case "$1" in
    --title) TITLE="${2:-}"; shift 2 ;;
    --description) DESCRIPTION="${2:-}"; shift 2 ;;
    --session-key) SESSION_KEY="${2:-}"; shift 2 ;;
    --podcast) PODCAST_ID="${2:-}"; shift 2 ;;
    --publish)
      if [ "${YT2PODCAST_ALLOW_PUBLISH:-}" != "1" ]; then
        die "公开发布需要显式授权:设置 YT2PODCAST_ALLOW_PUBLISH=1 后再加 --publish(公开不可撤销)"
      fi
      DRAFT=0; shift ;;
    --draft) DRAFT=1; shift ;;
    --hold-upload) HOLD_UPLOAD=1; shift ;;
    --auto-upload) HOLD_UPLOAD=0; shift ;;   # 兼容旧参数,现在是默认行为
    --retry) RETRY=1; shift ;;
    --no-start) shift ;;   # 兼容旧参数,现在是默认行为
    --start|--wait) die "本脚本不再启动 worker;请用: python3 ${WORKER} <job_id>(由宿主后台托管)" ;;
    --timeout) shift 2 ;;   # 兼容旧参数,已无意义
    -h|--help) usage; exit 0 ;;
    --*) die "unknown option: $1" ;;
    *) if [ -z "$URL" ]; then URL="$1"; shift; else die "unexpected argument: $1"; fi ;;
  esac
done

[ -n "$URL" ] || { usage >&2; die "missing youtube url"; }
[ -f "$WORKER" ] || die "worker not found: $WORKER"

# ---------- 前置条件(毫秒级,不启动浏览器):缺东西就别建 job --------
require_ready() {
  local missing=() fix=""
  local b
  for b in opencli ffmpeg ffprobe python3; do
    command -v "$b" >/dev/null 2>&1 || missing+=("命令缺失: $b")
  done
  local clis="${OPENCLI_HOME:-$HOME/.opencli}/clis"
  local rel
  for rel in notebooklm/download-audio.js xiaoyuzhou/upload.js xiaoyuzhou/upload-status.js; do
    [ -f "$clis/$rel" ] || missing+=("adapter 未安装: $rel")
  done
  [ -n "${PODCAST_ID:-}" ] || missing+=("没有小宇宙节目 id")

  if [ "${#missing[@]}" -gt 0 ]; then
    fix="bash $SCRIPT_DIR/setup.sh"
    python3 - "$fix" "${missing[@]}" <<'PY'
import json, sys
fix = sys.argv[1]
print(json.dumps({
    "ok": False,
    "error": "前置条件未满足,已拒绝建 job(避免白跑一趟、白耗生成配额)",
    "missing": sys.argv[2:],
    "fix": fix,
    # agent 可自主执行的安全修复动作(幂等、只写本机 opencli 目录、不改用户配置)
    "repair": {
        "safe": True,
        "cmd": fix,
        "then": "重新执行同一条 new-job.sh 命令",
        "note": "安装自带 adapter 并做环境自检;不会安装全局包、不会登录账号",
    },
}, ensure_ascii=False))
PY
    exit 4
  fi
}

# ---------------------------------------------------------------- 提取 video_id
extract_video_id() {
  local url="$1"
  local id=""
  case "$url" in
    *youtu.be/*)      id="${url#*youtu.be/}" ;;
    *watch?v=*)       id="${url#*watch?v=}" ;;
    */shorts/*)       id="${url#*/shorts/}" ;;
    */embed/*)        id="${url#*/embed/}" ;;
    */live/*)         id="${url#*/live/}" ;;
    *v=*)             id="${url#*v=}" ;;
    *)                id="$url" ;;
  esac
  # 去掉多余的查询串/片段
  id="${id%%[&?#]*}"
  id="${id%%/*}"
  printf '%s' "$id"
}

require_ready

VIDEO_ID="$(extract_video_id "$URL")"
if ! printf '%s' "$VIDEO_ID" | grep -Eq '^[A-Za-z0-9_-]{11}$'; then
  die "cannot parse YouTube video id from: $URL"
fi

JOB_ID="$VIDEO_ID"
JOB_DIR="$JOBS_DIR/$JOB_ID"
JOB_FILE="$JOBS_DIR/$JOB_ID.json"
mkdir -p "$JOB_DIR"

# ---------------------------------------------------------------- 幂等
existing_stage=""
if [ -f "$JOB_FILE" ]; then
  existing_stage="$(python3 - "$JOB_FILE" <<'PY'
import json, sys
try:
    with open(sys.argv[1], "r", encoding="utf-8") as handle:
        print(json.load(handle).get("stage") or "pending")
except Exception:
    print("pending")
PY
)"
fi

if [ -n "$existing_stage" ] && [ "$existing_stage" != "failed" ]; then
  # 已存在且非 failed → 直接输出已有状态,不再起 worker
  python3 - "$JOB_FILE" "$existing_stage" "$JOB_ID" <<'PY'
import json, sys
path, stage, job_id = sys.argv[1], sys.argv[2], sys.argv[3]
with open(path, "r", encoding="utf-8") as handle:
    job = json.load(handle)
print(json.dumps({
    "ok": True,
    "existing": True,
    "job_id": job.get("job_id"),
    "stage": stage,
    "job_file": path,
    "job_dir": path.rsplit("/", 1)[0] + "/" + job_id,
    "episode_url": job.get("episode_url"),
    "error": job.get("error"),
}, ensure_ascii=False))
PY
  exit 0
fi

if [ "$existing_stage" = "failed" ] && [ "$RETRY" -ne 1 ]; then
  # failed 的 job 只有显式 --retry 才重跑
  python3 - "$JOB_FILE" <<'PY'
import json, sys
with open(sys.argv[1], "r", encoding="utf-8") as handle:
    job = json.load(handle)
print(json.dumps({
    "ok": False,
    "existing": True,
    "stage": "failed",
    "job_id": job.get("job_id"),
    "job_file": sys.argv[1],
    "error": job.get("error"),
    "hint": "上次跑失败了;确认原因后用 --retry 重跑(会复用已有 notebook,不再消耗生成配额)",
}, ensure_ascii=False))
PY
  exit 3
fi

# ---------------------------------------------------------------- 串行约束检查
if [ "$START" -eq 1 ] && [ -f "$JOBS_DIR/.worker.lock" ]; then
  LOCK_PID="$(cat "$JOBS_DIR/.worker.lock" 2>/dev/null || echo "")"
  if [ -n "$LOCK_PID" ] && kill -0 "$LOCK_PID" 2>/dev/null; then
    die "another worker is running (pid=$LOCK_PID); wait for it to finish"
  fi
fi

# ---------------------------------------------------------------- 写 job 文件
YOUTUBE_URL="$URL" JOB_ID="$JOB_ID" JOB_FILE="$JOB_FILE" JOB_DIR="$JOB_DIR" \
TITLE="$TITLE" DESCRIPTION="$DESCRIPTION" SESSION_KEY="$SESSION_KEY" \
PODCAST_ID="$PODCAST_ID" AUTO_UPLOAD="$AUTO_UPLOAD" HOLD_UPLOAD="$HOLD_UPLOAD" DRAFT="$DRAFT" RETRY="$RETRY" \
python3 - <<'PY'
import json, os, time

def now():
    return time.strftime("%Y-%m-%dT%H:%M:%S%z")

path = os.environ["JOB_FILE"]
job_id = os.environ["JOB_ID"]
job = {}
if os.path.exists(path):
    try:
        with open(path, "r", encoding="utf-8") as handle:
            job = json.load(handle)
    except Exception:
        job = {}

retry = os.environ.get("RETRY") == "1"
job.update({
    "job_id": job_id,
    "video_id": job_id,
    "youtube_url": os.environ["YOUTUBE_URL"],
    "stage": job.get("stage") if (retry and job.get("stage") not in (None, "failed")) else "pending",
    "title": os.environ.get("TITLE") or job.get("title") or "",
    "description": os.environ.get("DESCRIPTION") or job.get("description") or "",
    "session_key": os.environ.get("SESSION_KEY") or job.get("session_key") or "",
    "podcast_id": os.environ.get("PODCAST_ID") or job.get("podcast_id"),
    "draft": os.environ.get("DRAFT") == "1",
    "auto_upload": os.environ.get("AUTO_UPLOAD") == "1",
    "hold_upload": os.environ.get("HOLD_UPLOAD") == "1",
    "notebook_id": job.get("notebook_id"),
    "source_id": job.get("source_id"),
    "stages_done": job.get("stages_done") or [],
    "history": job.get("history") or [],
    "created_at": job.get("created_at") or now(),
    "updated_at": now(),
})
if job["stage"] == "pending":
    job.pop("error", None)
    job.pop("failed_stage", None)

tmp = path + ".tmp"
with open(tmp, "w", encoding="utf-8") as handle:
    json.dump(job, handle, ensure_ascii=False, indent=2)
    handle.write("\n")
os.replace(tmp, path)
print(json.dumps({"job_id": job_id, "job_file": path, "stage": job["stage"]}, ensure_ascii=False))
PY

# 不启动 worker:只把"下一步命令"告诉调用方
NEXT_STEP="python3 $WORKER $JOB_ID"

python3 - "$JOB_FILE" "$JOB_ID" "$NEXT_STEP" <<'PY'
import json, sys
path, job_id, next_step = sys.argv[1], sys.argv[2], sys.argv[3]
try:
    with open(path, "r", encoding="utf-8") as handle:
        job = json.load(handle)
except Exception:
    job = {}
print(json.dumps({
    "ok": True,
    "job_id": job_id,
    "stage": job.get("stage"),
    "started": False,
    "next_step": next_step,
    "job_file": path,
    "job_dir": path.rsplit("/", 1)[0] + "/" + job_id,
    "log": path.rsplit("/", 1)[0] + "/" + job_id + "/worker.log",
    "episode_url": job.get("episode_url"),
    "error": job.get("error"),
}, ensure_ascii=False))
PY
