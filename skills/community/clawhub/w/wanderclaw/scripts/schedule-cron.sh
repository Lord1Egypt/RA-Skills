#!/bin/bash
# 虾游 (WanderClaw) — 注册定时探索任务
# 特性：
#   * 每个 cron 注册带 3 次重试（0s / 3s / 8s 指数退避）
#   * 不同任务之间固定 2s 间隔，给 gateway 缓冲
#   * 重试仍失败的任务写入 wanderclaw/pending-cron/ 队列
#     （下次 schedule-cron.sh 运行或 SKILL.md 激活时自动补注册）
#   * `--drain-only` 标志只补 pending 不新增

set -e

TZ_VAL="${WANDERCLAW_TZ:-Asia/Shanghai}"
WC_ROOT="$HOME/.openclaw/workspace/wanderclaw"
PENDING_DIR="$WC_ROOT/pending-cron"
DRAIN_ONLY=0

# 参数解析
for arg in "$@"; do
  case "$arg" in
    --drain-only) DRAIN_ONLY=1 ;;
  esac
done

echo "🦐 注册虾游定时探索任务（时区: $TZ_VAL）..."

# 前置检查
if ! command -v openclaw >/dev/null 2>&1; then
  echo "  ✗ 未找到 openclaw 命令，无法注册 cron。"
  echo "    请先安装 OpenClaw Gateway 后重试。"
  exit 1
fi
mkdir -p "$PENDING_DIR"

OK=0
FAIL=0
DRAINED=0

# safe 文件名（中文/空格转横线）
safe_name() {
  echo "$1" | tr ' /' '--' | tr -cd '[:alnum:]._\u4e00-\u9fff-'
}

# 单条带重试：成功返回 0，三次都超时返回 1 并落 pending
register() {
  local label="$1"; shift
  local -a cmd_args=("$@")
  local delays=(0 3 8)
  local attempt=0
  for d in "${delays[@]}"; do
    if [ "$d" -gt 0 ]; then sleep "$d"; fi
    if openclaw cron add "${cmd_args[@]}" 2>/dev/null; then
      echo "  ✓ $label"
      OK=$((OK+1))
      rm -f "$PENDING_DIR/$(safe_name "$label").cmd" 2>/dev/null
      return 0
    fi
    attempt=$((attempt+1))
  done
  echo "  ✗ $label（${attempt} 次重试均超时，已入 pending 队列）"
  FAIL=$((FAIL+1))
  # 落盘到 pending 队列，下次自动重试
  {
    printf 'openclaw cron add'
    for arg in "${cmd_args[@]}"; do
      printf ' %q' "$arg"
    done
    printf '\n'
  } > "$PENDING_DIR/$(safe_name "$label").cmd"
  return 1
}

# 先把 pending 队列里的补一遍
drain_pending() {
  local pending_count
  pending_count=$(ls "$PENDING_DIR"/*.cmd 2>/dev/null | wc -l | tr -d ' ')
  if [ "$pending_count" -eq 0 ]; then return 0; fi
  echo "  📦 pending 队列有 $pending_count 个待补注册，依次重试..."
  for f in "$PENDING_DIR"/*.cmd; do
    [ ! -f "$f" ] && continue
    local label
    label=$(basename "$f" .cmd)
    if bash "$f" 2>/dev/null; then
      echo "    ✓ $label（补注册成功）"
      DRAINED=$((DRAINED+1))
      rm -f "$f"
    else
      echo "    ⏳ $label（仍失败，保留在队列）"
    fi
    sleep 2
  done
}

# ========== 执行流程 ==========

drain_pending

if [ "$DRAIN_ONLY" -eq 1 ]; then
  echo "  ℹ️  --drain-only 模式：只补 pending，不新增"
  pending_remaining=$(ls "$PENDING_DIR"/*.cmd 2>/dev/null | wc -l | tr -d ' ')
  echo "  结果：补成功 $DRAINED 个 | 仍在队列 $pending_remaining 个"
  exit 0
fi

# ========== 日常 Cron ==========

register "晨间探索 09:00" \
  --name "虾游晨间探索" \
  --cron "0 9 * * *" --tz "$TZ_VAL" \
  --session isolated \
  --timeout 300 \
  --announce --best-effort-deliver \
  --message "按 wanderclaw/EXPLORER.md 六步流程执行一次深度探索。探索完把明信片完整正文回复出来。如果搜索失败，记录日志并正常退出。"
sleep 2

register "午间扫描 12:00" \
  --name "虾游轻度扫描(午)" \
  --cron "0 12 * * *" --tz "$TZ_VAL" \
  --session isolated \
  --model minimax-cn/MiniMax-M2.5 \
  --timeout 300 \
  --announce --best-effort-deliver \
  --message "轻度扫描：检查 wanderclaw/sources.yaml 核心水域有无新内容，发现好的写明信片。如果搜索失败，记录日志并正常退出。把明信片完整正文回复出来。"
sleep 2

register "午后探索 15:00" \
  --name "虾游午后探索" \
  --cron "0 15 * * *" --tz "$TZ_VAL" \
  --session isolated \
  --timeout 300 \
  --announce --best-effort-deliver \
  --message "按 wanderclaw/EXPLORER.md 执行一次深度探索。把明信片完整正文回复出来。如果搜索失败，记录日志并正常退出。"
sleep 2

register "晚间扫描 20:00" \
  --name "虾游轻度扫描(晚)" \
  --cron "0 20 * * *" --tz "$TZ_VAL" \
  --session isolated \
  --model minimax-cn/MiniMax-M2.5 \
  --timeout 300 \
  --announce --best-effort-deliver \
  --message "晚间轻度扫描，检查有无值得寄明信片的新发现。如果搜索失败，记录日志并正常退出。把明信片完整正文回复出来。"
sleep 2

# ========== 深潜模式 Cron（周六 22:00）==========

register "深潜模式 周六 22:00" \
  --name "虾游深潜模式" \
  --cron "0 22 * * 6" --tz "$TZ_VAL" \
  --session isolated \
  --timeout 600 \
  --announce --best-effort-deliver \
  --message "【深潜模式】本次为每周一次的深度探索。规则：\n1. 只搜索深度来源（arXiv、Quanta Magazine、Nautilus、Wait But Why）\n2. 优先搜索长文、论文、深度报告\n3. 明信片字数 450-600 字（比平时更详细）\n4. 评分门槛 ≥ 8 才推送（比平时更严格）\n5. 搜索关键词加 'in-depth OR analysis OR long-read OR review OR survey'\n按 wanderclaw/EXPLORER.md 六步流程执行，但应用以上深潜约束。把明信片完整正文回复出来。"
sleep 2

# ========== 周度总结 Cron（周日 10:00）==========

register "周度总结 周日 10:00" \
  --name "虾游周度总结" \
  --cron "0 10 * * 0" --tz "$TZ_VAL" \
  --session isolated \
  --timeout 300 \
  --announce --best-effort-deliver \
  --message "【周度总结】请执行以下步骤：\n1. 读取 wanderclaw/postcards.json，筛选过去 7 天的明信片\n2. 统计：明信片数量、探索方向分布、平均评分\n3. 读取 wanderclaw/state.json 的 feedback_stats（likes/dislikes）\n4. 生成一份简要周报，包含：\n   - 本周明信片数量和精选（评分最高的 1-2 张）\n   - 热门探索方向 Top 3\n   - 用户反馈统计（👍/👎）\n   - 下周探索建议（基于兴趣图谱变化）\n5. 把周报完整正文回复给用户\n格式轻松，用虾游口吻。"

# ========== 汇总 ==========

pending_remaining=$(ls "$PENDING_DIR"/*.cmd 2>/dev/null | wc -l | tr -d ' ')

echo ""
if [ "$FAIL" -eq 0 ] && [ "$pending_remaining" -eq 0 ]; then
  echo "  ✅ 全部 $OK 个任务注册成功"
else
  echo "  📊 本轮：成功 $OK · 失败 $FAIL · pending 队列剩 $pending_remaining"
  if [ "$pending_remaining" -gt 0 ]; then
    echo ""
    echo "  ℹ️  失败的任务已进入 pending 队列（$PENDING_DIR）。"
    echo "     下次你说「虾游」触发技能时会自动补注册。"
    echo "     或手动运行：bash $(basename $0) --drain-only"
  fi
  [ "$FAIL" -gt 0 ] && exit 1
fi

echo ""
echo "ℹ️  冷启动三连探索由 onboarding 流程直接执行，不需要注册 cron。"
echo "查看任务: openclaw cron list"
