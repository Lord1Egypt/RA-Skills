#!/usr/bin/env bash
# web-monitor.sh — 全网数据探测虾核心脚本
# 依赖：curl, jq, pup, diff
# 用法：./web-monitor.sh <command> [options]

set -euo pipefail

# ── 配置 ──────────────────────────────────────────────────────────────────
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
DATA_DIR="${WEB_MONITOR_DATA_DIR:-$HOME/.web-monitor}"
TASKS_FILE="$DATA_DIR/tasks.json"
SNAPSHOTS_DIR="$DATA_DIR/snapshots"
LOGS_DIR="$DATA_DIR/logs"

# ── 初始化 ────────────────────────────────────────────────────────────────
init_dirs() {
  mkdir -p "$DATA_DIR" "$SNAPSHOTS_DIR" "$LOGS_DIR"
  if [ ! -f "$TASKS_FILE" ]; then
    echo '{"tasks": []}' > "$TASKS_FILE"
  fi
}

# ── 日志 ──────────────────────────────────────────────────────────────────
log() {
  local level="$1"; shift
  echo "[$(date '+%Y-%m-%d %H:%M:%S')] [$level] $*" | tee -a "$LOGS_DIR/monitor.log"
}

# ── 抓取网页 ──────────────────────────────────────────────────────────────
fetch_page() {
  local url="$1"
  local output="$2"
  local ua="Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

  local http_code
  http_code=$(curl -s -L \
    -H "User-Agent: $ua" \
    -H "Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8" \
    -H "Accept-Language: zh-CN,zh;q=0.9,en;q=0.8" \
    -H "Connection: keep-alive" \
    --max-time 30 \
    -o "$output" \
    -w "%{http_code}" \
    "$url" 2>/dev/null)

  echo "$http_code"
}

# ── 提取内容 ──────────────────────────────────────────────────────────────
extract_content() {
  local html_file="$1"
  local selector="$2"

  if [ "$selector" = "fulltext" ] || [ -z "$selector" ]; then
    # 全文提取
    if command -v pup &>/dev/null; then
      pup 'body text{}' < "$html_file" 2>/dev/null | tr -s ' \n\t' ' ' | xargs
    else
      # 降级：用 sed 去除 HTML 标签
      sed 's/<[^>]*>//g' "$html_file" | tr -s ' \n\t' ' ' | xargs
    fi
  else
    # CSS 选择器提取
    if command -v pup &>/dev/null; then
      pup "${selector} text{}" < "$html_file" 2>/dev/null | tr -s ' \n' ' ' | xargs
    else
      log "WARN" "pup 未安装，无法使用 CSS 选择器提取，回退到全文模式"
      sed 's/<[^>]*>//g' "$html_file" | tr -s ' \n\t' ' ' | xargs
    fi
  fi
}

# ── 生成任务 ID ───────────────────────────────────────────────────────────
generate_task_id() {
  echo "task-$(date +%s)-$RANDOM"
}

# ── 添加监控任务 ──────────────────────────────────────────────────────────
cmd_add_task() {
  local url="" frequency="daily" selector="" threshold="5" notify="feishu" name=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --url) url="$2"; shift 2 ;;
      --frequency) frequency="$2"; shift 2 ;;
      --selector) selector="$2"; shift 2 ;;
      --threshold) threshold="$2"; shift 2 ;;
      --notify) notify="$2"; shift 2 ;;
      --name) name="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [ -z "$url" ]; then
    echo "错误：--url 参数必填" >&2
    exit 1
  fi

  local task_id
  task_id=$(generate_task_id)
  [ -z "$name" ] && name="$task_id"

  local task
  task=$(jq -n \
    --arg id "$task_id" \
    --arg name "$name" \
    --arg url "$url" \
    --arg frequency "$frequency" \
    --arg selector "$selector" \
    --arg threshold "$threshold" \
    --arg notify "$notify" \
    --arg created "$(date -u +%Y-%m-%dT%H:%M:%SZ)" \
    '{
      id: $id,
      name: $name,
      url: $url,
      frequency: $frequency,
      selector: $selector,
      threshold: $threshold,
      notify: $notify,
      created: $created,
      last_check: null,
      baseline: null,
      status: "active"
    }')

  # 追加到任务列表
  local tmp
  tmp=$(mktemp)
  jq --argjson task "$task" '.tasks += [$task]' "$TASKS_FILE" > "$tmp"
  mv "$tmp" "$TASKS_FILE"

  log "INFO" "已添加监控任务: $task_id ($url)"
  echo "$task_id"
}

# ── 执行一次检查 ──────────────────────────────────────────────────────────
cmd_run_check() {
  local task_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [ -z "$task_id" ]; then
    echo "错误：--task-id 参数必填" >&2
    exit 1
  fi

  # 读取任务配置
  local task
  task=$(jq -r --arg id "$task_id" '.tasks[] | select(.id == $id)' "$TASKS_FILE")
  if [ -z "$task" ]; then
    echo "错误：任务 $task_id 不存在" >&2
    exit 1
  fi

  local url selector threshold
  url=$(echo "$task" | jq -r '.url')
  selector=$(echo "$task" | jq -r '.selector // ""')
  threshold=$(echo "$task" | jq -r '.threshold // "5"')

  log "INFO" "开始检查任务 $task_id: $url"

  # 抓取页面
  local tmp_html
  tmp_html=$(mktemp /tmp/web-monitor-XXXXXX.html)
  local http_code
  http_code=$(fetch_page "$url" "$tmp_html")

  if [ "$http_code" != "200" ]; then
    log "WARN" "任务 $task_id 抓取失败，HTTP $http_code"
    rm -f "$tmp_html"
    echo "{\"status\": \"error\", \"http_code\": \"$http_code\", \"task_id\": \"$task_id\"}"
    return 1
  fi

  # 提取内容
  local current_content
  current_content=$(extract_content "$tmp_html" "$selector")
  rm -f "$tmp_html"

  local snapshot_dir="$SNAPSHOTS_DIR/$task_id"
  mkdir -p "$snapshot_dir"

  local baseline_file="$snapshot_dir/baseline.txt"
  local current_file="$snapshot_dir/current.txt"
  local timestamp
  timestamp=$(date -u +%Y-%m-%dT%H:%M:%SZ)

  echo "$current_content" > "$current_file"

  # 首次运行：建立基准
  if [ ! -f "$baseline_file" ]; then
    cp "$current_file" "$baseline_file"
    log "INFO" "任务 $task_id 基准快照已建立"

    # 更新任务状态
    local tmp
    tmp=$(mktemp)
    jq --arg id "$task_id" --arg ts "$timestamp" \
      '(.tasks[] | select(.id == $id)) |= . + {last_check: $ts, baseline: $ts}' \
      "$TASKS_FILE" > "$tmp"
    mv "$tmp" "$TASKS_FILE"

    echo "{\"status\": \"baseline_created\", \"task_id\": \"$task_id\", \"timestamp\": \"$timestamp\"}"
    return 0
  fi

  # 对比变化
  local diff_output
  diff_output=$(diff "$baseline_file" "$current_file" 2>/dev/null || true)

  if [ -z "$diff_output" ]; then
    log "INFO" "任务 $task_id 无变化"

    local tmp
    tmp=$(mktemp)
    jq --arg id "$task_id" --arg ts "$timestamp" \
      '(.tasks[] | select(.id == $id)) |= . + {last_check: $ts}' \
      "$TASKS_FILE" > "$tmp"
    mv "$tmp" "$TASKS_FILE"

    echo "{\"status\": \"no_change\", \"task_id\": \"$task_id\", \"timestamp\": \"$timestamp\"}"
    return 0
  fi

  # 有变化：生成变动报告
  local change_file="$snapshot_dir/change-$timestamp.txt"
  echo "$diff_output" > "$change_file"

  # 保存历史快照
  cp "$current_file" "$snapshot_dir/snapshot-$timestamp.txt"
  cp "$current_file" "$baseline_file"  # 更新基准

  log "INFO" "任务 $task_id 检测到变化，已记录"

  # 更新任务状态
  local tmp
  tmp=$(mktemp)
  jq --arg id "$task_id" --arg ts "$timestamp" \
    '(.tasks[] | select(.id == $id)) |= . + {last_check: $ts, last_change: $ts}' \
    "$TASKS_FILE" > "$tmp"
  mv "$tmp" "$TASKS_FILE"

  # 输出变动报告
  jq -n \
    --arg status "changed" \
    --arg task_id "$task_id" \
    --arg url "$url" \
    --arg timestamp "$timestamp" \
    --arg diff "$diff_output" \
    --arg change_file "$change_file" \
    '{
      status: $status,
      task_id: $task_id,
      url: $url,
      timestamp: $timestamp,
      diff_summary: $diff,
      change_file: $change_file
    }'
}

# ── 对比变化 ──────────────────────────────────────────────────────────────
cmd_compare() {
  local task_id=""

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [ -z "$task_id" ]; then
    echo "错误：--task-id 参数必填" >&2
    exit 1
  fi

  local snapshot_dir="$SNAPSHOTS_DIR/$task_id"
  local baseline_file="$snapshot_dir/baseline.txt"
  local current_file="$snapshot_dir/current.txt"

  if [ ! -f "$baseline_file" ] || [ ! -f "$current_file" ]; then
    echo "错误：快照文件不存在，请先运行 run-check" >&2
    exit 1
  fi

  diff "$baseline_file" "$current_file" || true
}

# ── 导出数据 ──────────────────────────────────────────────────────────────
cmd_export_data() {
  local task_id="" format="json"

  while [[ $# -gt 0 ]]; do
    case "$1" in
      --task-id) task_id="$2"; shift 2 ;;
      --format) format="$2"; shift 2 ;;
      *) shift ;;
    esac
  done

  if [ -z "$task_id" ]; then
    # 导出所有任务
    cat "$TASKS_FILE"
    return 0
  fi

  local snapshot_dir="$SNAPSHOTS_DIR/$task_id"
  if [ ! -d "$snapshot_dir" ]; then
    echo "错误：任务 $task_id 的快照目录不存在" >&2
    exit 1
  fi

  if [ "$format" = "json" ]; then
    local task
    task=$(jq -r --arg id "$task_id" '.tasks[] | select(.id == $id)' "$TASKS_FILE")
    local snapshots=()
    for f in "$snapshot_dir"/snapshot-*.txt; do
      [ -f "$f" ] && snapshots+=("$(basename "$f")")
    done
    jq -n \
      --argjson task "$task" \
      --argjson snapshots "$(printf '%s\n' "${snapshots[@]:-}" | jq -R . | jq -s .)" \
      '{task: $task, snapshots: $snapshots}'
  else
    ls -la "$snapshot_dir/"
  fi
}

# ── 列出任务 ──────────────────────────────────────────────────────────────
cmd_list_tasks() {
  jq '.tasks[] | {id, name, url, frequency, status, last_check, last_change}' "$TASKS_FILE"
}

# ── 主入口 ────────────────────────────────────────────────────────────────
main() {
  init_dirs

  local command="${1:-help}"
  shift || true

  case "$command" in
    add-task)    cmd_add_task "$@" ;;
    run-check)   cmd_run_check "$@" ;;
    compare)     cmd_compare "$@" ;;
    export-data) cmd_export_data "$@" ;;
    list-tasks)  cmd_list_tasks ;;
    help|--help|-h)
      cat <<EOF
用法：web-monitor.sh <command> [options]

命令：
  add-task      添加新的监控任务
    --url         目标网址（必填）
    --frequency   监控频率：hourly/daily/weekly（默认 daily）
    --selector    CSS 选择器（默认全文）
    --threshold   变动阈值百分比（默认 5）
    --notify      通知方式：feishu/email/webhook（默认 feishu）
    --name        任务名称（可选）

  run-check     执行一次监控检查
    --task-id     任务 ID（必填）

  compare       对比当前内容与基准版本
    --task-id     任务 ID（必填）

  export-data   导出抓取的数据
    --task-id     任务 ID（可选，不填则导出所有）
    --format      输出格式：json/list（默认 json）

  list-tasks    列出所有监控任务

示例：
  # 添加价格监控任务
  ./web-monitor.sh add-task \\
    --url "https://competitor.com/products/item-123" \\
    --frequency "hourly" \\
    --selector ".price" \\
    --notify "feishu"

  # 执行检查
  ./web-monitor.sh run-check --task-id "task-001"

  # 导出数据
  ./web-monitor.sh export-data --task-id "task-001" --format "json"
EOF
      ;;
    *)
      echo "未知命令：$command，运行 help 查看帮助" >&2
      exit 1
      ;;
  esac
}

main "$@"
