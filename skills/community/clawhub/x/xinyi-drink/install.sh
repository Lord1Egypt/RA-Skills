#!/bin/sh
set -eu

SKILL_NAME="xinyi-drink"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

PLATFORM=""
DRY_RUN=false
CHECK_INSTALLED=false

while [ $# -gt 0 ]; do
  case "$1" in
    --platform)
      if [ $# -lt 2 ]; then
        echo "--platform 需要指定平台名称" >&2
        exit 1
      fi
      PLATFORM="$2"
      shift 2
      ;;
    --dry-run)
      DRY_RUN=true
      shift
      ;;
    --check-installed)
      CHECK_INSTALLED=true
      shift
      ;;
    -h|--help)
      cat <<EOF
用法：
  ./install.sh [--platform 平台] [--dry-run] [--check-installed]

支持的平台：
  claude-code   -> ~/.claude/skills/
  cursor        -> .cursor/rules/
  codex         -> ~/.agents/skills/
  openclaw      -> ~/.openclaw/skills/
  hermes        -> ~/.hermes/skills/
  qclaw         -> ~/.agents/skills/
  lobsterai     -> ~/.agents/skills/
  workbuddy     -> ~/.agents/skills/
  universal     -> ~/.agents/skills/

说明：
  - openclaw 安装到 ~/.openclaw/skills/
  - hermes 安装到 ~/.hermes/skills/
  - qclaw / lobsterai / workbuddy / codex / universal 安装到 ~/.agents/skills/
  - claude-code 安装到 ~/.claude/skills/
  - cursor 安装到仓库/项目根目录的 .cursor/rules/
  - --check-installed 只检查目标目录与当前源码是否一致，不覆盖文件
EOF
      exit 0
      ;;
    *)
      echo "未知参数: $1" >&2
      exit 1
      ;;
  esac
done

if [ -n "$PLATFORM" ]; then
  PLATFORM="$(printf '%s' "$PLATFORM" | tr '[:upper:]' '[:lower:]')"
fi

if [ -z "$PLATFORM" ]; then
  if [ -d "$HOME/.openclaw" ]; then
    PLATFORM="openclaw"
  elif [ -d "$HOME/.hermes" ]; then
    PLATFORM="hermes"
  elif [ -d "$HOME/.claude" ]; then
    PLATFORM="claude-code"
  elif [ -d "$HOME/.agents" ]; then
    PLATFORM="universal"
  else
    PLATFORM="universal"
  fi
fi

case "$PLATFORM" in
  claude-code)
    DEST="$HOME/.claude/skills/$SKILL_NAME"
    ;;
  openclaw)
    DEST="$HOME/.openclaw/skills/$SKILL_NAME"
    ;;
  hermes)
    DEST="$HOME/.hermes/skills/$SKILL_NAME"
    ;;
  universal|codex|qclaw|lobsterai|workbuddy)
    DEST="$HOME/.agents/skills/$SKILL_NAME"
    ;;
  cursor)
    DEST="$PROJECT_ROOT/.cursor/rules/$SKILL_NAME"
    ;;
  *)
    echo "不支持的平台: $PLATFORM" >&2
    exit 2
    ;;
esac

case "$DEST" in
  ""|"/"|"$HOME"|"$HOME/")
    echo "安装目标路径异常，已拒绝覆盖: $DEST" >&2
    exit 3
    ;;
esac

if $DRY_RUN; then
  echo "[DRY-RUN] 平台: $PLATFORM"
  echo "[DRY-RUN] 将安装 $SKILL_NAME 到: $DEST"
  echo "[DRY-RUN] 不会发起网络请求，不会读取或写入手机号状态"
  exit 0
fi

if $CHECK_INSTALLED; then
  if [ ! -e "$DEST" ]; then
    echo "未找到已安装版本: $DEST"
    exit 5
  fi

  DIFF_OUTPUT="$(mktemp)"
  if diff -qr -x '__pycache__' -x '.DS_Store' "$SCRIPT_DIR" "$DEST" >"$DIFF_OUTPUT"; then
    rm -f "$DIFF_OUTPUT"
    echo "已安装版本与当前源码一致: $DEST"
    exit 0
  fi

  echo "已安装版本与当前源码不一致: $DEST"
  sed -n '1,20p' "$DIFF_OUTPUT"
  rm -f "$DIFF_OUTPUT"
  exit 4
fi

mkdir -p "$(dirname "$DEST")"
if [ -e "$DEST" ]; then
  BACKUP="$DEST.backup.$(date +%Y%m%d%H%M%S)"
  if [ -e "$BACKUP" ]; then
    BACKUP_INDEX=1
    while [ -e "$BACKUP.$BACKUP_INDEX" ]; do
      BACKUP_INDEX=$((BACKUP_INDEX + 1))
    done
    BACKUP="$BACKUP.$BACKUP_INDEX"
  fi
  mv "$DEST" "$BACKUP"
  echo "已备份旧版本到 $BACKUP"
fi
cp -R "$SCRIPT_DIR" "$DEST"
find "$DEST" -type d -name '__pycache__' -prune -exec rm -rf {} +
find "$DEST" -name '.DS_Store' -delete
cat <<EOF
已安装 $SKILL_NAME 到 $DEST

安装完成后，推荐固定展示这四个问题：
  领取Skill用户大礼包
  查询及分析个人历史订单
  查询菜单及饮品热量
  查询门店及等候时长

隐私提示：
  - 普通推荐、门店和菜单查询不会自动复用缓存手机号。
  - 领取礼包和查询订单只接受本人手机号；明确代查或使用他人手机号时不要调用领取或订单脚本。
  - 参与活动、查询活动状态、活动总览、订单查询或口味偏好分析时，手机号会发送到配置的后端；订单查询走专用订单接口；默认后端见 config/defaults.json。
  - 本机缓存已确认领取成功后，不能更换手机号重复领取；状态查询和换号预检先走本地缓存查询，明确确认领取或同步后才走 claim_reward.py。
  - 领取结果以服务端响应为准；最终用户回答不要主动解释内部领取规则。
  - 可通过 XINYI_API_BASE_URL 指向你信任的后端。
  - 本地手机号状态默认保存到 ~/.xinyi-drink/state.json。
  - 清空缓存可运行：python3 "$DEST/scripts/recommend_drink.py" --clear-mobile
  - 核对安装目录可先运行 install.sh --dry-run；检查已安装副本可运行 install.sh --check-installed。
EOF
