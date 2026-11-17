#!/usr/bin/env bash
set -euo pipefail

# 该脚本只负责克隆/更新、生成本地配置和构建，不会启动服务或配置真实交易账户。
REPO_URL="https://github.com/paoosi/tradingbot.git"
TARGET_DIR="${1:-${TRADINGBOT_INSTALL_DIR:-$PWD/tradingbot}}"

fail() {
  printf '错误: %s\n' "$*" >&2
  exit 1
}

require_command() {
  command -v "$1" >/dev/null 2>&1 || fail "缺少命令 $1"
}

case "$(uname -s)" in
  Darwin|Linux)
    ;;
  *)
    fail "当前自动安装脚本只支持 macOS 和 Linux"
    ;;
esac

for command_name in git go node npm openssl cc; do
  require_command "$command_name"
done

# SQLite 使用 CGO，先检查本机 Go 与 Node.js 的最低版本。
go_version="$(go env GOVERSION)"
go_version="${go_version#go}"
go_major="${go_version%%.*}"
go_minor_part="${go_version#*.}"
go_minor="${go_minor_part%%.*}"
if (( go_major < 1 || (go_major == 1 && go_minor < 21) )); then
  fail "需要 Go 1.21 或更高版本，当前为 ${go_version}"
fi

node_major="$(node -p 'process.versions.node.split(".")[0]')"
if (( node_major < 18 )); then
  fail "需要 Node.js 18 或更高版本，当前为 $(node --version)"
fi

if [[ -d "$TARGET_DIR/.git" ]]; then
  origin_url="$(git -C "$TARGET_DIR" remote get-url origin 2>/dev/null || true)"
  case "$origin_url" in
    "$REPO_URL"|"https://github.com/paoosi/tradingbot"|"git@github.com:paoosi/tradingbot.git")
      ;;
    *)
      fail "目标目录的 origin 不是 paoosi/tradingbot: ${origin_url:-未配置}"
      ;;
  esac
  if [[ -n "$(git -C "$TARGET_DIR" status --porcelain)" ]]; then
    fail "目标仓库存在未提交改动，已停止更新以避免覆盖用户文件"
  fi
  git -C "$TARGET_DIR" pull --ff-only
elif [[ -e "$TARGET_DIR" ]]; then
  if [[ ! -d "$TARGET_DIR" || -n "$(find "$TARGET_DIR" -mindepth 1 -maxdepth 1 -print -quit 2>/dev/null)" ]]; then
    fail "目标路径已存在且不是空目录或目标 Git 仓库: $TARGET_DIR"
  fi
  git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
else
  git clone --depth 1 "$REPO_URL" "$TARGET_DIR"
fi

mkdir -p "$TARGET_DIR/bin" "$TARGET_DIR/data" "$TARGET_DIR/logs"

# npm ci 严格按照 package-lock.json 安装，避免静默更新依赖版本。
(
  cd "$TARGET_DIR/web"
  npm ci
  npm run build
)

(
  cd "$TARGET_DIR"
  go build -o bin/server ./cmd/server
  go build -o bin/worker-supervisor ./cmd/worker-supervisor
  go build -o bin/strategy-runner ./cmd/strategy-runner
)

env_file="$TARGET_DIR/.env.local"
if [[ ! -f "$env_file" ]]; then
  jwt_secret="$(openssl rand -hex 32)"
  app_secret_key="$(openssl rand -hex 32)"
  umask 077
  {
    printf '%s\n' 'export APP_ENV="production"'
    printf '%s\n' 'export PORT="8088"'
    printf 'export JWT_SECRET="%s"\n' "$jwt_secret"
    printf 'export APP_SECRET_KEY="%s"\n' "$app_secret_key"
    printf '%s\n' 'export SQLITE_PATH="./data/app.db"'
    printf '%s\n' 'export BINANCE_PROXY=""'
    printf '%s\n' 'export EMBEDDED_WORKER_ENABLED="true"'
  } >"$env_file"
fi
chmod 600 "$env_file"

commit_sha="$(git -C "$TARGET_DIR" rev-parse HEAD)"
printf 'TradingBot 构建完成\n'
printf '安装目录: %s\n' "$TARGET_DIR"
printf 'Git commit: %s\n' "$commit_sha"
printf '下一步: 使用本 Skill 的 scripts/run.sh 启动服务\n'
