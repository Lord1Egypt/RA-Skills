#!/usr/bin/env bash
# memory.sh — 记忆系统（单脚本，无硬编码用户名）
set -euo pipefail
VERSION="3.3"

# ── 配置 ──
SESSIONS_DIR="${SESSIONS_DIR:-/root/.openclaw/agents/main/sessions}"
LOCK_TTL=600
SUMMARY_MAX_LEN=2000

# ── 帮助 ──
show_help() {
  cat <<'HELP'
用法: memory.sh <命令> [参数]

命令:
  sync [--user <name>]        同步对话摘要到 Redis
  get <用户名> [天数]          查记忆（默认为最近 3 天）
  set <用户名> <日期> <摘要>   手动写入摘要
  heartbeat                   系统心跳 + 监控（供 cron 调用）
  ping                        检查 Redis 连通性
  stats                       系统状态

环境变量:
  MEMORY_USERS    逗号分隔的用户列表（用于 sync/heartbeat）
  SESSIONS_DIR    transcript 目录（默认 .../agents/main/sessions）

用户列表来源（优先级）:
  1. sync --user 参数
  2. $MEMORY_USERS 环境变量
  3. /etc/memory-users.conf 文件
HELP
  exit 0
}

json_esc() { python3 -c 'import json,sys; print(json.dumps(sys.stdin.read().rstrip("\n")))' <<< "$1"; }

get_users() {
  local single="$1"  # --user 值，可能为空
  if [ -n "$single" ]; then echo "$single"; return; fi
  if [ -n "${MEMORY_USERS:-}" ]; then echo "$MEMORY_USERS" | tr ',' '\n'; return; fi
  if [ -f /etc/memory-users.conf ]; then cat /etc/memory-users.conf; return; fi
  echo ""
}

[ $# -lt 1 ] && show_help
ACTION="$1"; shift || true

# ── ping ──
if [ "$ACTION" = "ping" ]; then
  redis-cli PING >/dev/null 2>&1 && echo "✅ Redis OK" || { echo "❌ Redis 未运行"; exit 1; }
  exit 0
fi
if [ "$ACTION" = "help" ]; then show_help; fi

# ═══════════════════════════════════════════
# sync
# ═══════════════════════════════════════════
if [ "$ACTION" = "sync" ]; then
  SINGLE_USER=""
  while [ $# -gt 0 ]; do
    case "$1" in --user) SINGLE_USER="$2"; shift 2 ;; *) shift ;; esac
  done

  USERS=$(get_users "$SINGLE_USER")
  [ -z "$USERS" ] && { echo '{"status":"error","reason":"No users configured"}'; exit 0; }

  echo '['; FIRST=true
  while IFS= read -r raw_user; do
    u="$(echo "$raw_user" | xargs)"
    [ -z "$u" ] && continue
    $FIRST || echo ','; FIRST=false

    # 防并发锁（一个 subshell = 一个用户，trap 自动释放）
    (
      LOCK_KEY="cron_lock:sync:${u}"
      if ! redis-cli SET "$LOCK_KEY" "$$" NX EX "$LOCK_TTL" >/dev/null 2>&1; then
        escaped_u=$(json_esc "$u")
        echo "{\"status\":\"skip\",\"username\":${escaped_u},\"reason\":\"locked\"}"
        exit 0
      fi
      trap 'redis-cli DEL "$LOCK_KEY" >/dev/null 2>&1 || true' EXIT

      # 找最新 transcript（按时间排序，跳过 trajectory 和 cron session）
      BEST=""
      while IFS= read -r -d '' f; do
        case "$f" in *.trajectory*) continue ;; esac
        # 至少 2 条用户消息
        c=$(grep -c '"role":"user"' "$f" 2>/dev/null || echo 0); c="${c:-0}"
        [ "$c" -ge 2 ] || continue
        # 过滤 cron session：第一条 user 消息含 memory.sh sync 特征（语言无关）
        FIRST_USER=$(grep -m1 '"role":"user"' "$f" 2>/dev/null | python3 -c "
import json,sys
try:
    m=json.loads(sys.stdin.readline().strip())
    msg=m.get('message',{}).get('content','')
    if isinstance(msg,list):
        for c in msg:
            if c.get('type')=='text': print(c['text'][:200]); break
    elif isinstance(msg,str): print(msg[:200])
except: pass
" 2>/dev/null)
        case "$FIRST_USER" in *memory.sh*sync*) continue ;; esac
        BEST="$f"; break
      done < <(ls -t "$SESSIONS_DIR"/*.jsonl 2>/dev/null | grep -Fv ".trajectory" | head -20 | tr '\n' '\0')

      # 使用 transcript 文件修改日期作为日期，避免跨夜写入错误日期
      if [ -n "$BEST" ]; then
        FILE_TS=$(stat -c %Y "$BEST" 2>/dev/null || echo 0)
        TODAY=$(date -d "@$FILE_TS" +%Y-%m-%d 2>/dev/null || date +%Y-%m-%d)
      else
        TODAY=$(date +%Y-%m-%d)
      fi

      # 提取对话（Python）
      DIALOG=""
      if [ -n "$BEST" ]; then
        DIALOG=$(python3 -c "
import json, sys
try:
    with open(sys.argv[1]) as f:
        lines = f.readlines()
except:
    sys.exit(0)
out = []
for line in lines[-200:]:
    try:
        m = json.loads(line.strip())
        if m.get('type') != 'message': continue
        msg = m.get('message', {})
        role = msg.get('role', '')
        content = msg.get('content', '')
        if isinstance(content, list):
            for c in content:
                if c.get('type') == 'text' and c.get('text','').strip():
                    out.append(f'{role}: {c[\"text\"][:300]}')
        elif isinstance(content, str) and len(content) < 500 and content.strip():
            out.append(f'{role}: {content[:300]}')
    except:
        pass
for l in out:
    print(l)
" "$BEST" 2>/dev/null) || true
      fi

      EXISTING=$(redis-cli HGET "memory:${u}" "$TODAY" 2>/dev/null || echo "")
      EU=$(json_esc "$u")
      EF=$(json_esc "${BEST:-}")
      ED=$(json_esc "$DIALOG")
      EE=$(json_esc "$EXISTING")
      cat << JSONEOF
{
  "status": "ok",
  "username": $EU,
  "date": "$TODAY",
  "file": $EF,
  "dialog_lines": $ED,
  "existing_summary": $EE,
  "existing_len": ${#EXISTING},
  "summary_max_len": $SUMMARY_MAX_LEN
}
JSONEOF
    )
  done <<< "$USERS"
  echo ']'
  exit 0
fi

# ═══════════════════════════════════════════
# tag
# ═══════════════════════════════════════════
if [ "$ACTION" = "tag" ]; then
  USER="${1:-}"; DATE="${2:-}"; shift 2 2>/dev/null || true
  TAGS="$*"
  [ -z "$USER" ] && { echo "❌ 缺用户名"; exit 1; }
  [ -z "$DATE" ] && { echo "❌ 缺日期"; exit 1; }
  [ -z "$TAGS" ] && { echo "❌ 缺标签"; exit 1; }
  
  # 删除该日期旧标签及倒排索引
  for t in $(redis-cli SMEMBERS "tags:${USER}:${DATE}" 2>/dev/null || true); do
    redis-cli SREM "tagidx:${t}" "${DATE}" >/dev/null 2>&1 || true
  done
  redis-cli DEL "tags:${USER}:${DATE}" >/dev/null 2>&1 || true
  
  # 写入新标签 + 倒排索引
  for t in $TAGS; do
    [ -z "$t" ] && continue
    redis-cli SADD "tags:${USER}:${DATE}" "$t" >/dev/null 2>&1 || true
    redis-cli SADD "tagidx:${t}" "${DATE}" >/dev/null 2>&1 || true
    redis-cli EXPIRE "tagidx:${t}" 604800 >/dev/null 2>&1 || true
  done
  redis-cli EXPIRE "tags:${USER}:${DATE}" 604800 >/dev/null 2>&1 || true
  echo "✅ ${USER} ${DATE} 标签已记录"
  exit 0
fi

# ═══════════════════════════════════════════
# search
# ═══════════════════════════════════════════
if [ "$ACTION" = "search" ]; then
  QUERY="$*"
  [ -z "$QUERY" ] && { echo "❌ 用法: memory.sh search <关键词>"; echo "   示例: memory.sh search 论文架构"; exit 1; }
  echo "Q: $QUERY"
  # 列出所有标签供语义匹配
  echo "---TAGS---"
  redis-cli KEYS "tagidx:*" 2>/dev/null | sed 's/tagidx://' | sort -u | paste -sd ' ' || echo "（暂无标签）"
  exit 0
fi

# ═══════════════════════════════════════════
# heartbeat
# ═══════════════════════════════════════════
if [ "$ACTION" = "heartbeat" ]; then
  NOW="$(date '+%Y-%m-%d %H:%M')"
  TODAY="$(date '+%Y-%m-%d')"
  redis-cli HSET "cron:health" "$NOW" "ok" >/dev/null 2>&1 || true
  redis-cli EXPIRE "cron:health" 604800 >/dev/null 2>&1 || true
  USERS=$(get_users "")
  while IFS= read -r raw_user; do
    u="$(echo "$raw_user" | xargs)"; [ -z "$u" ] && continue
    ts=$(redis-cli HGET "memory:${u}" "$TODAY" 2>/dev/null || echo "")
    ys=$(date -d 'yesterday' '+%Y-%m-%d' 2>/dev/null)
    ys_val=$(redis-cli HGET "memory:${u}" "$ys" 2>/dev/null || echo "")
    wf="/tmp/memory_warning_${u}.flag"
    if [ -n "$ts" ]; then rm -f "$wf"
    elif [ -n "$ys_val" ]; then echo "[$NOW] ⚠️ $u: 今日暂无"
    else
      act=$(redis-cli GET "activity:${u}:last_seen" 2>/dev/null || echo "")
      [ -n "$act" ] && { echo "[$NOW] 🚨 $u: 活跃但摘要丢失 ($act)"; echo "$NOW|$u|miss|$act" > "$wf"; }
    fi
  done <<< "$USERS"
  exit 0
fi

# ═══════════════════════════════════════════
# stats / get / set
# ═══════════════════════════════════════════
USER="${1:-}"

if [ "$ACTION" = "stats" ]; then
  echo "📊 状态"; echo "========"
  for key in $(redis-cli KEYS "memory:*" 2>/dev/null); do
    u="${key#memory:}"; c=$(redis-cli HLEN "$key" 2>/dev/null || echo 0)
    t=$(( $(redis-cli TTL "$key" 2>/dev/null || echo 0) / 86400 ))
    ch=0; for d in $(redis-cli HKEYS "$key" 2>/dev/null); do
      v=$(redis-cli HGET "$key" "$d" 2>/dev/null || echo ""); ch=$((ch+${#v})); done
    echo "  $u: ${c}天 / ${t}天后 / ${ch}字符"
  done
  hb=$(redis-cli HLEN "cron:health" 2>/dev/null || echo 0)
  echo "  心跳: ${hb}条"
  exit 0
fi

[ -z "$USER" ] && { echo "❌ 缺少用户名" >&2; exit 1; }

if [ "$ACTION" = "get" ]; then
  DAYS="${2:-3}"
  if echo "$DAYS" | grep -qxE '^[0-9]+$' 2>/dev/null; then
    [ "$DAYS" -gt 30 ] && DAYS=30
    for d in $(seq 0 "$DAYS"); do
      day=$(date -d "-$d days" +%Y-%m-%d 2>/dev/null)
      val=$(redis-cli HGET "memory:$USER" "$day" 2>/dev/null)
      [ -n "$val" ] && echo "[$day] $val"
    done
  elif echo "$DAYS" | grep -qxE '^[0-9]{4}-[0-9]{2}-[0-9]{2}$' 2>/dev/null; then
    val=$(redis-cli HGET "memory:$USER" "$DAYS" 2>/dev/null)
    echo "${val:-（无记录）}"
  else
    for d in $(seq 0 3); do
      day=$(date -d "-$d days" +%Y-%m-%d 2>/dev/null)
      val=$(redis-cli HGET "memory:$USER" "$day" 2>/dev/null)
      [ -n "$val" ] && echo "[$day] $val"
    done
  fi
  exit 0
fi

if [ "$ACTION" = "set" ]; then
  DATE="${2:-}"; SUMMARY="${*:3}"
  [ -z "$DATE" ] && { echo "❌ 缺日期" >&2; exit 1; }
  [ -z "$SUMMARY" ] && { echo "❌ 缺内容" >&2; exit 1; }
  redis-cli EVAL "
    redis.call('HSET', 'memory:$USER', ARGV[1], ARGV[2])
    redis.call('EXPIRE', 'memory:$USER', 604800)
    redis.call('SET', 'activity:${USER}:last_seen', ARGV[3], 'EX', 43200)
    return 'OK'
  " 0 "$DATE" "$SUMMARY" "$(date '+%Y-%m-%d %H:%M')" >/dev/null
  echo "✅ 已记录"
  exit 0
fi

echo "❌ 未知操作: $ACTION" >&2
echo "可用: sync get set heartbeat ping stats help" >&2
exit 1
