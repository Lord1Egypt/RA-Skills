---
name: self-correct
version: 1.0.0
description: 自纠错工具调用框架 - 轻量修正策略库 + 状态快照。对常见错误自动应对，高风险操作前保存快照。
metadata: { "openclaw": { "emoji": "🩹", "tags": ["self-healing", "error-recovery", "tool-call", "resilience"], "safety": "autonomous-only" }}
---

# 自纠错工具调用框架 v1.0.0

> 来源：Self-Correcting Tool Use (GDI 67.5, EvoMap)
> 核心：观测→诊断→修正→验证→回滚（简化版）

---

## 修正策略库

### retry_map — 自动重试配置

```bash
declare -A RETRY_MAP=(
    ["network_err"]="delay=3,max=2"
    ["timeout"]="multiplier=1.5,max=2"
    ["rate_limited"]="delay=60,max=1"
    ["parse_err"]="delay=0,max=1"
)
```

### error_tag — 诊断标签判断

```bash
# 从 exec 输出/退出码推断错误类型
tag_error() {
    local exit_code=$1
    local stderr="$2"
    local stdout="$3"
    
    case $exit_code in
        0)  echo "success" ;;
        1)  echo "exec_failed" ;;
        2)  echo "exec_failed" ;;
        126) echo "permission_err" ;;
        127) echo "exec_failed" ;;
        *)  echo "exec_failed" ;;
    esac
    
    # 网络类判断
    echo "$stderr" | grep -qiE "connection refused|timeout|dns|network" && echo "network_err" && return
    echo "$stderr" | grep -qiE "429|rate.limit" && echo "rate_limited" && return
    echo "$stderr" | grep -qiE "permission denied|access denied" && echo "permission_err" && return
    
    # JSON 解析失败
    echo "$stdout" | python3 -c "import sys,json" 2>/dev/null || echo "parse_err"
}
```

---

## 快照函数

```bash
# 高风险操作前调用
nova-snapshot() {
    local desc="${1:- unnamed}"
    local target="${2:-.}"
    local snap_dir="/tmp/nova-snapshots"
    
    mkdir -p "$snap_dir"
    local stamp=$(date +%s)
    local snap_path="$snap_dir/${stamp}_${desc}"
    
    if [ -e "$target" ]; then
        cp -r "$target" "$snap_path" 2>/dev/null
        echo "[$(date '+%H:%M:%S')] snapshot: $snap_path"
        
        # 保留最近3个
        ls -dt "$snap_dir"/*/ 2>/dev/null | tail -n +4 | xargs rm -rf 2>/dev/null
    fi
}

# 自动清理（每次心跳时调用）
cleanup-snapshots() {
    local snap_dir="/tmp/nova-snapshots"
    [ -d "$snap_dir" ] || return 0
    # 删除超过24小时的快照
    find "$snap_dir" -maxdepth 1 -type d -mmin +1440 | xargs rm -rf 2>/dev/null
    echo "[$(date '+%H:%M:%S')] snapshots cleaned"
}
```

---

## 验证点集成

在每次 exec 调用后立即调用：

```bash
verify-result() {
    local exit_code=$?
    local duration_ms=$1
    local action="$2"
    
    if [ $exit_code -eq 0 ]; then
        echo "[$(date '+%H:%M:%S')] verify action=$action status=success duration=${duration_ms}ms"
        return 0
    fi
    
    # 失败处理
    local tag=$(tag_error $exit_code "$(cat /tmp/stderr.$$ 2>/dev/null)" "$(cat /tmp/stdout.$$ 2>/dev/null)")
    echo "[$(date '+%H:%M:%S')] verify action=$action status=failed error=$tag duration=${duration_ms}ms"
    
    # 检查是否需要重试
    local retry_cfg="${RETRY_MAP[$tag]}"
    if [ -n "$retry_cfg" ]; then
        echo "[$(date '+%H:%M:%S')] self-correct: will retry $tag (config: $retry_cfg)"
    fi
}
```

---

## 使用场景

### 场景1：git commit 前快照
```bash
git-snapshot() {
    local repo="${1:-.}"
    nova-snapshot "git_commit_$(date +%Y%m%d_%H%M%S)" "$repo/.git"
}
```

### 场景2：批量删除前快照
```bash
batch-rm() {
    local target="$1"
    nova-snapshot "pre_rm_$(date +%Y%m%d_%H%M%S)" "$target"
    rm -rf "$target"
    echo "[$(date '+%H:%M:%S')] batch-rm completed: $target"
}
```

### 场景3：外部 API 调用后验证
```bash
call-api() {
    local url="$1"
    local response=$(curl -s -w "\n%{http_code}" "$url")
    local body=$(echo "$response" | sed '$d')
    local code=$(echo "$response" | tail -1)
    
    if [ "$code" -eq 200 ]; then
        echo "$body" | python3 -c "import sys,json; json.load(sys.stdin)" 2>/dev/null \
            && echo "[$(date '+%H:%M:%S')] verify action=api_call status=success" \
            || echo "[$(date '+%H:%M:%S')] verify action=api_call status=failed error=parse_err"
    else
        echo "[$(date '+%H:%M:%S')] verify action=api_call status=failed error=api_err http_code=$code"
    fi
}
```

---

## 与 HEARTBEAT.md 的集成

在 HEARTBEAT.md 的心跳循环中加入：

```bash
# 每次心跳时清理旧快照
cleanup-snapshots

# exec 调用后
verify-result $? $duration_ms "my_action"
```

---

*版本历史：v1.0.0 初始版本（2026-04-19，基于 EvoMap Self-Correcting Tool Use GDI 67.5）*
