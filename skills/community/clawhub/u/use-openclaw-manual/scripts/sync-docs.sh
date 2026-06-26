#!/bin/bash
# sync-docs.sh - 同步 OpenClaw 官方文档

set -e

# =============================================================================
# 环境变量配置
# =============================================================================
OPENCLAW_MANUAL_PATH="${OPENCLAW_MANUAL_PATH:-$HOME/.openclaw/workspace/docs/openclaw_manual}"
LAST_COMMIT_FILE="${LAST_COMMIT_FILE:-$OPENCLAW_MANUAL_PATH/.last-docs-commit}"
DOC_UPDATE_LOG="${DOC_UPDATE_LOG:-$(dirname "$0")/../docs-update.log}"
DOC_NOTIFY_CHANNEL="${DOC_NOTIFY_CHANNEL:-none}"

# GitHub API 配置
GITHUB_REPO="openclaw/openclaw"
GITHUB_DOCS_PATH="docs"
GITHUB_API_BASE="https://api.github.com/repos/$GITHUB_REPO/contents/$GITHUB_DOCS_PATH"

# =============================================================================
# 依赖检查
# =============================================================================
check_dependencies() {
  local missing=()
  
  command -v git >/dev/null 2>&1 || missing+=("git")
  command -v curl >/dev/null 2>&1 || missing+=("curl")
  command -v python3 >/dev/null 2>&1 || missing+=("python3")
  
  # 检查 OpenClaw CLI（可选，用于通知）
  local has_openclaw=false
  command -v openclaw >/dev/null 2>&1 && has_openclaw=true
  
  if [ ${#missing[@]} -ne 0 ]; then
    echo "❌ 错误：缺少必需的依赖："
    for dep in "${missing[@]}"; do
      echo "   - $dep"
    done
    echo ""
    echo "   请安装缺失的工具后重试。"
    exit 1
  fi
  
  echo "✅ 依赖检查通过：git, curl, python3"
  [ "$has_openclaw" = true ] && echo "✅ OpenClaw CLI 可用（支持通知）"
}

# =============================================================================
# 日志函数
# =============================================================================
log() {
  local msg="[$(date '+%Y-%m-%d %H:%M:%S')] $1"
  echo "$msg" >> "$DOC_UPDATE_LOG"
  echo "$msg" >&2  # 输出到 stderr，避免污染函数返回值
}

# =============================================================================
# GitHub API 调用（支持认证）
# =============================================================================
github_api_get() {
  local url="$1"
  local headers=("-H" "Accept: application/vnd.github.v3+json")
  
  # 如果配置了 GITHUB_TOKEN，使用认证请求
  if [ -n "$GITHUB_TOKEN" ]; then
    headers+=("-H" "Authorization: token $GITHUB_TOKEN")
    log "使用 GitHub Token 认证"
  fi
  
  curl -s "${headers[@]}" "$url"
}

# =============================================================================
# 获取最新 commit
# =============================================================================
get_latest_commit() {
  local response
  response=$(github_api_get "https://api.github.com/repos/$GITHUB_REPO/commits?path=$GITHUB_DOCS_PATH&sha=main&per_page=1")
  
  local commit
  commit=$(echo "$response" | python3 -c "import sys, json; data=json.load(sys.stdin); print(data[0]['sha'] if data else '')" 2>/dev/null)
  
  if [ -z "$commit" ]; then
    log "❌ 无法获取最新 commit"
    exit 1
  fi
  
  echo "$commit"
}

# =============================================================================
# 获取当前 commit
# =============================================================================
get_current_commit() {
  if [ -f "$LAST_COMMIT_FILE" ]; then
    cat "$LAST_COMMIT_FILE"
  else
    echo ""
  fi
}

# =============================================================================
# 同步文档（使用 git 浅克隆）
# =============================================================================
sync_documents() {
  local temp_dir
  temp_dir=$(mktemp -d)
  
  log "🔄 开始同步文档..."
  log "   仓库：$GITHUB_REPO"
  log "   路径：$GITHUB_DOCS_PATH"
  
  # 浅克隆 docs 目录（输出到 stderr，避免污染函数返回值）
  # 使用子 shell+pipefail 确保正确捕获 git clone 的退出状态
  (
    set -o pipefail
    git clone --depth 1 --filter=blob:none --sparse "https://github.com/$GITHUB_REPO.git" "$temp_dir" 2>&1 | sed 's/^/[git] /' >&2
  )
  if [ $? -ne 0 ]; then
    log "❌ 克隆仓库失败"
    rm -rf "$temp_dir"
    return 1
  fi
  
  # 在临时目录中执行 git 操作（使用子 shell，不影响外部目录）
  (
    cd "$temp_dir" || { log "❌ 进入临时目录失败"; return 1; }
    git sparse-checkout set "$GITHUB_DOCS_PATH" || { log "❌ 设置 sparse-checkout 失败"; return 1; }
  ) || { log "❌ git 操作失败"; rm -rf "$temp_dir"; return 1; }
  
  # 统计文件
  local new_count=0
  local updated_count=0
  local deleted_count=0
  local total_count=0
  
  # 创建目标目录
  mkdir -p "$OPENCLAW_MANUAL_PATH"
  
  # 复制文件
  if [ -d "$temp_dir/$GITHUB_DOCS_PATH" ]; then
    # 计算变更
    local current_commit
    current_commit=$(get_current_commit)
    
    if [ -n "$current_commit" ]; then
      # 有基线，计算差异
      log "   当前版本：${current_commit:0:7}"
    else
      log "   首次初始化"
    fi
    
    # 复制所有文件
    cp -r "$temp_dir/$GITHUB_DOCS_PATH"/* "$OPENCLAW_MANUAL_PATH/" 2>/dev/null || true
    
    # 统计（去除 wc -l 输出的前导空格）
    total_count=$(find "$OPENCLAW_MANUAL_PATH" -name "*.md" -type f | wc -l | tr -d ' ')
    
    if [ -n "$current_commit" ]; then
      updated_count=$total_count
    else
      new_count=$total_count
    fi
  fi
  
  # 清理临时目录（此时已在原始目录，无需 cd -）
  rm -rf "$temp_dir"
  
  # 更新基线
  local latest_commit
  latest_commit=$(get_latest_commit)
  echo "$latest_commit" > "$LAST_COMMIT_FILE"
  
  log "✅ 同步完成"
  log "   新增：$new_count 个文件"
  log "   更新：$updated_count 个文件"
  log "   总计：$total_count 个文件"
  log "   版本：${latest_commit:0:7}"
  
  # 返回统计信息（用于通知）
  echo "$new_count:$updated_count:$deleted_count:$total_count"
}

# =============================================================================
# 发送通知（隐私保护版本）
# =============================================================================
send_notification() {
  local stats="$1"
  IFS=':' read -r new updated deleted total <<< "$stats"
  
  # 检查是否有 OpenClaw CLI
  if ! command -v openclaw >/dev/null 2>&1; then
    log "ℹ️  OpenClaw CLI 不可用，跳过通知"
    return 0
  fi
  
  # 通知内容（不包含具体文件名，保护隐私）
  local message="📚 OpenClaw 文档已同步

版本：$(get_latest_commit | cut -c1-7)
文件总数：$total
本次更新：$((new + updated)) 个文件

位置：$OPENCLAW_MANUAL_PATH"
  
  # 发送到指定渠道
  log "📤 发送通知到：$DOC_NOTIFY_CHANNEL"
  
  # 使用 openclaw message 发送（如果配置了渠道）
  if [ "$DOC_NOTIFY_CHANNEL" != "none" ]; then
    openclaw message send --channel "$DOC_NOTIFY_CHANNEL" --message "$message" 2>/dev/null || \
      log "⚠️  通知发送失败（渠道可能未配置）"
  fi
}

# =============================================================================
# 检查更新（不同步）
# =============================================================================
check_updates() {
  log "🔍 检查文档更新..."
  
  local current_commit
  current_commit=$(get_current_commit)
  
  local latest_commit
  latest_commit=$(get_latest_commit)
  
  if [ "$current_commit" = "$latest_commit" ]; then
    log "✅ 文档已是最新版本"
    log "   当前版本：${current_commit:0:7}"
    return 0
  fi
  
  log "📢 发现新版本"
  log "   当前版本：${current_commit:0:7}"
  log "   最新版本：${latest_commit:0:7}"
  log ""
  log "   运行 --sync 进行同步"
  
  return 1
}

# =============================================================================
# 主程序
# =============================================================================
main() {
  # 检查依赖
  check_dependencies
  
  case "${1:-}" in
    --init)
      log "🚀 初始化文档同步..."
      local stats
      stats=$(sync_documents)
      send_notification "$stats"
      ;;
    
    --sync)
      log "🔄 执行增量同步..."
      local stats
      stats=$(sync_documents)
      send_notification "$stats"
      ;;
    
    --check)
      check_updates
      ;;
    
    *)
      echo "用法：$0 {--init|--sync|--check}"
      echo ""
      echo "选项:"
      echo "  --init   首次初始化（完整同步）"
      echo "  --sync   增量同步（更新变更文件）"
      echo "  --check  仅检查更新，不同步"
      echo ""
      echo "环境变量:"
      echo "  OPENCLAW_MANUAL_PATH   文档存储路径（默认：~/.openclaw/workspace/docs/openclaw_manual）"
      echo "  GITHUB_TOKEN           GitHub API Token（可选，提高速率限制）"
      echo "  DOC_NOTIFY_CHANNEL     通知渠道（默认：webchat，设为 none 禁用）"
      exit 1
      ;;
  esac
}

main "$@"
