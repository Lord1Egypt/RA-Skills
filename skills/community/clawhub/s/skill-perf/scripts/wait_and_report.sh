#!/bin/bash
# wait_and_report.sh — 轮询等待两个 subagent 完成，从 .jsonl 读精确 totalTokens，生成报告
#
# 用法：
#   bash wait_and_report.sh <CALIB_KEY> <TEST_KEY> <SKILL_NAME>
#
# 参数：
#   CALIB_KEY   - 标定 subagent 的 childSessionKey（sessions_spawn 立即返回）
#   TEST_KEY    - 测试 subagent 的 childSessionKey（sessions_spawn 立即返回）
#   SKILL_NAME  - 被测 skill 名称（用于报告显示）

# 不使用 set -e，改为显式错误处理，防止静默退出

CALIB_KEY="$1"
TEST_KEY="$2"
SKILL_NAME="${3:-unknown}"

if [[ -z "$CALIB_KEY" || -z "$TEST_KEY" ]]; then
  echo "用法: bash wait_and_report.sh <CALIB_KEY> <TEST_KEY> <SKILL_NAME>"
  exit 1
fi

SESS_DIR="$HOME/.openclaw/agents/main/sessions"
SESS_FILE="$SESS_DIR/sessions.json"
SNAPSHOT_PY="$HOME/.openclaw/skills/skill-perf/scripts/snapshot.py"

echo "[skill-perf] 开始轮询..."
echo "[skill-perf] calib=$CALIB_KEY"
echo "[skill-perf] test=$TEST_KEY"

# 启动时立刻读取 sessionId（session 还活着时），供后续 .deleted 降级使用
_get_session_id() {
  local key="$1"
  python3 - <<PYEOF2
import json
from pathlib import Path
d = json.loads(Path('$SESS_FILE').read_text()) if Path('$SESS_FILE').exists() else {}
entry = d.get('$key') or next((v for k,v in d.items() if k.startswith('$key') or '$key'.startswith(k[:len('$key')])), {})
print(entry.get('sessionId', '') if isinstance(entry, dict) else '')
PYEOF2
}
CALIB_SID_INIT=$(_get_session_id "$CALIB_KEY" 2>/dev/null)
TEST_SID_INIT=$(_get_session_id "$TEST_KEY" 2>/dev/null)
echo "[skill-perf] calib_sid=$CALIB_SID_INIT  test_sid=$TEST_SID_INIT"

# 从 sessions.json 找 sessionId → .jsonl，读 usage.totalTokens
# 输出格式：TOKENS:xxx SESSION_ID:yyy
read_tokens_from_jsonl() {
  local session_key="$1"
  local fallback_sid="$2"   # 启动时记录的 sessionId，用于 .deleted 精确匹配
  python3 - <<PYEOF
import json
from pathlib import Path

sess_file = Path('$SESS_FILE')
sess_dir  = Path('$SESS_DIR')
key = '$session_key'

if not sess_file.exists():
    print('')
    exit()

d = json.loads(sess_file.read_text())

# 精确匹配，失败时尝试前缀模糊匹配（防止 agent 传入截断的 key）
entry = d.get(key)
if not entry and len(key) >= 20:
    for k in d:
        if k.startswith(key) or key.startswith(k[:len(key)]):
            if isinstance(d[k], dict):
                entry = d[k]
                import sys
                print(f'[debug] prefix match: {key!r} -> {k!r}', file=sys.stderr)
                break
if not entry:
    entry = {}

import sys

sid = entry.get('sessionId', '')
t_sess = entry.get('totalTokens', 0)
is_fresh = entry.get('totalTokensFresh', False)

def extract_text(content):
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return '\n'.join(c.get('text', '') for c in content if isinstance(c, dict) and c.get('type') == 'text')
    return ''

def scan_jsonl(path):
    """扫描 .jsonl，同时收集最大 totalTokens 和检测 ANNOUNCE_SKIP。
    返回 (t_at_announce, t_max, found_announce)
    - t_at_announce: ANNOUNCE_SKIP 出现时的 totalTokens（skill-perf 设计约定的结束信号）
    - t_max: 文件中所有 totalTokens 的最大值
    - found_announce: 是否找到 ANNOUNCE_SKIP
    """
    best_total = 0
    t_at_announce = 0
    found_announce = False
    for line in path.read_text(errors='replace').splitlines():
        try:
            obj = json.loads(line)
            msg = obj.get('message', {})
            t = msg.get('usage', {}).get('totalTokens', 0)
            if t:
                best_total = t
            if msg.get('role') == 'assistant':
                if 'ANNOUNCE_SKIP' in extract_text(msg.get('content', '')):
                    found_announce = True
                    t_at_announce = best_total
        except:
            pass
    return (t_at_announce, best_total, found_announce)

# ── 调试模式：ANNOUNCE_SKIP 和 totalTokensFresh 两个信号并行输出，供对比验证 ──
if sid:
    jsonl = sess_dir / f'{sid}.jsonl'
    if jsonl.exists():
        t_at_ann, t_max, found_ann = scan_jsonl(jsonl)

        # 信号1: ANNOUNCE_SKIP（skill-perf 自定义约定，LLM 主动输出）
        sig_announce = t_at_ann if found_ann else 0
        # 信号2: totalTokensFresh（sessions.json 字段，OpenClaw 框架写入）
        sig_fresh = t_sess if is_fresh else 0

        # 两个信号都打印，方便对比
        print(f'[DEBUG:ANNOUNCE_SKIP] found={found_ann} t={sig_announce}', file=sys.stderr)
        print(f'[DEBUG:totalTokensFresh] fresh={is_fresh} t={sig_fresh}', file=sys.stderr)
        if sig_announce and sig_fresh:
            if sig_announce == sig_fresh:
                print(f'[DEBUG] ✅ AGREE: both={sig_announce}', file=sys.stderr)
            else:
                print(f'[DEBUG] ⚠️ DIFFER: announce={sig_announce} fresh={sig_fresh}', file=sys.stderr)
        elif sig_announce and not sig_fresh:
            print(f'[DEBUG] ANNOUNCE_SKIP ready, totalTokensFresh not yet', file=sys.stderr)
        elif sig_fresh and not sig_announce:
            print(f'[DEBUG] totalTokensFresh ready, ANNOUNCE_SKIP not found', file=sys.stderr)

        # 以 ANNOUNCE_SKIP 为主信号（skill-perf 自己设计的约定，语义最明确）
        if sig_announce:
            print(f'TOKENS:{sig_announce} SESSION_ID:{sid}')
            exit()
        # totalTokensFresh 作为备用
        if sig_fresh:
            print(f'TOKENS:{sig_fresh} SESSION_ID:{sid}')
            exit()
        if t_sess:
            print(f'[DEBUG] both pending, t_sess={t_sess} (mid-run)', file=sys.stderr)
    else:
        if t_sess:
            print(f'[DEBUG] no .jsonl yet, t_sess={t_sess}', file=sys.stderr)

# 降级：session 已被清除，从 .deleted 文件恢复
fsid = '$fallback_sid'
if fsid:
    deleted_files = sorted(sess_dir.glob(f'{fsid}.jsonl.deleted.*'))
    if deleted_files:
        df = deleted_files[-1]
        t_at_ann, t_max, found_ann = scan_jsonl(df)
        if found_ann and t_at_ann:
            print(f'[DEBUG] ANNOUNCE_SKIP in .deleted: {df.name}', file=sys.stderr)
            print(f'TOKENS:{t_at_ann} SESSION_ID:{fsid}')
            exit()
        if t_max:
            print(f'[DEBUG] .deleted fallback (no ANNOUNCE_SKIP, abnormal exit): t={t_max}', file=sys.stderr)
            print(f'TOKENS:{t_max} SESSION_ID:{fsid}')
            exit()

print('')
PYEOF
}

calib_t=""
calib_sid=""
test_t=""
test_sid=""
tick=0
MAX_TICKS=75   # 最多等 75 × 8s = 600s（10分钟）

while true; do
  tick=$((tick + 1))

  if [[ -z "$calib_t" ]]; then
    val=$(read_tokens_from_jsonl "$CALIB_KEY" "$CALIB_SID_INIT" 2>/dev/null)
    if [[ -n "$val" && "$val" != "0" ]]; then
      calib_t=$(echo "$val" | grep -o 'TOKENS:[0-9]*' | sed 's/TOKENS://')
      calib_sid=$(echo "$val" | grep -o 'SESSION_ID:[^ ]*' | sed 's/SESSION_ID://')
    fi
  fi

  if [[ -z "$test_t" ]]; then
    val=$(read_tokens_from_jsonl "$TEST_KEY" "$TEST_SID_INIT" 2>/dev/null)
    if [[ -n "$val" && "$val" != "0" ]]; then
      test_t=$(echo "$val" | grep -o 'TOKENS:[0-9]*' | sed 's/TOKENS://')
      test_sid=$(echo "$val" | grep -o 'SESSION_ID:[^ ]*' | sed 's/SESSION_ID://')
    fi
  fi

  echo "[tick=$tick/$MAX_TICKS] calib=${calib_t:-running}  test=${test_t:-running}"

  if [[ -n "$calib_t" && -n "$test_t" ]]; then
    echo ""
    echo "✅ DONE  CALIB_NOISE=$calib_t  TEST_TOTAL=$test_t"
    echo "   calib_sid=$calib_sid  test_sid=$test_sid"
    echo ""
    echo "[skill-perf] 生成报告..."
    if python3 "$SNAPSHOT_PY" report \
      --session "$TEST_KEY" \
      --session-id "$test_sid" \
      --calib-key "$CALIB_KEY" \
      --skill-name "$SKILL_NAME" \
      --html; then
      echo "✅ 报告生成完成"
    else
      echo "⚠️ 报告生成失败（exit code=$?），请检查 snapshot.py 日志"
    fi
    break
  fi

  # 超时：test subagent 卡住未完成
  if [[ $tick -ge $MAX_TICKS ]]; then
    echo ""
    echo "⏰ 超时（${MAX_TICKS}次轮询），test subagent 可能卡住或已超时退出"
    echo "⚠️ 无法生成报告"
    exit 1
  fi

  sleep 8
done
