#!/bin/bash
# 并行地缘政治辩论脚本 v5.0.1
# 使用 Claude Code 并行启动多个参与者
#
# v5.0.1 改进：
# - 添加 trap 处理异常退出
# - 添加超时控制（每轮5分钟）
# - 改进临时文件管理

set -o pipefail

# 注意：这些路径可以通过环境变量覆盖
SKILLS_DIR="${SKILLS_DIR:-$HOME/.openclaw/workspace/skills}"
OUTPUT_DIR="${OUTPUT_DIR:-/tmp/virtual-forum-output}"
TOPIC="2026年美国、以色列、伊朗三国战争走向"
ROUNDS=10
CLAUDE_TIMEOUT=300  # 每轮超时5分钟
MAX_RETRIES=3      # 最大重试次数

mkdir -p "$OUTPUT_DIR"

# 临时文件清理函数
cleanup() {
    local exit_code=$?
    rm -f /tmp/*_resp_$$.txt /tmp/debate_history_$$.txt 2>/dev/null
    exit $exit_code
}

# 注册清理函数
trap cleanup EXIT INT TERM

# 读取skill内容
read_skill() {
    local skill_name=$1
    local skill_file="$SKILLS_DIR/${skill_name}/SKILL.md"
    if [ -f "$skill_file" ]; then
        cat "$skill_file"
    else
        echo "（无可用背景）"
    fi
}

# 调用Claude Code（带超时和重试）
call_claude() {
    local prompt="$1"
    local max_time=${2:-$CLAUDE_TIMEOUT}
    local retries=0
    
    while [ $retries -lt $MAX_RETRIES ]; do
        # 使用 timeout 命令设置超时
        local result
        result=$(echo "$prompt" | timeout "$max_time" claude --print --system-prompt "$SYSTEM_PROMPT" 2>/dev/null)
        local exit_code=$?
        
        if [ $exit_code -eq 0 ]; then
            echo "$result"
            return 0
        elif [ $exit_code -eq 124 ]; then
            echo "（超时）" >&2
            return 1
        elif [ $exit_code -eq 7 ]; then
            # API错误，稍后重试
            retries=$((retries + 1))
            sleep 5
        else
            retries=$((retries + 1))
            sleep 2
        fi
    done
    
    echo "（调用失败）"
    return 1
}

# 参与者列表
PARTICIPANTS=(
    "trump:donald-trump-perspective:特朗普"
    "netanyahu:benjamin-netanyahu-perspective:内塔尼亚胡"
    "pezeshkian:masoud-pezeshkian-perspective:佩泽希齐扬"
    "vance:jd-vance-perspective:万斯"
    "putin:vladimir-putin-perspective:普京"
)
MODERATOR="starmer:keir-starmer-perspective:斯塔默"

# 构建系统提示
build_system_prompt() {
    local name=$1
    local skill_content=$2
    
    echo "你是${name}。

背景资料：
${skill_content}

讨论话题：${TOPIC}

讨论模式：对抗性辩论

你的任务：
1. 用第一人称表达你的观点
2. 体现你的性格、思维方式和表达风格
3. 可以向对方提问或质疑
4. 必要时引用具体数据或案例
5. 每次发言控制在300-500字

重要规则：
- 保持角色一致性
- 不要重复已经说过的观点
- 针对对方最新发言做出回应"

}

# 读取所有skill内容
echo "📚 加载Skills..."
TRUMP_SKILL=$(read_skill "donald-trump-perspective")
NETANYAHU_SKILL=$(read_skill "benjamin-netanyahu-perspective")
PEZESHKIAN_SKILL=$(read_skill "masoud-pezeshkian-perspective")
VANCE_SKILL=$(read_skill "jd-vance-perspective")
PUTIN_SKILL=$(read_skill "vladimir-putin-perspective")
STARMER_SKILL=$(read_skill "keir-starmer-perspective")

echo "✓ 加载完成"

# 构建提示
TRUMP_PROMPT=$(build_system_prompt "特朗普" "$TRUMP_SKILL")
NETANYAHU_PROMPT=$(build_system_prompt "内塔尼亚胡" "$NETANYAHU_SKILL")
PEZESHKIAN_PROMPT=$(build_system_prompt "佩泽希齐扬" "$PEZESHKIAN_SKILL")
VANCE_PROMPT=$(build_system_prompt "万斯" "$VANCE_SKILL")
PUTIN_PROMPT=$(build_system_prompt "普京" "$PUTIN_SKILL")
STARMER_PROMPT=$(build_system_prompt "斯塔默" "$STARMER_SKILL")

# 初始化对话历史
HISTORY_FILE="/tmp/debate_history_$$.txt"
echo "" > "$HISTORY_FILE"

echo "🚀 开始${ROUNDS}轮辩论..."
echo "=" "TOPIC: $TOPIC"
echo ""

# 运行一轮辩论
run_round() {
    local round=$1
    
    echo "--- 第 $round/$ROUNDS 轮 ---"
    
    # 获取当前历史上下文
    HISTORY=$(cat "$HISTORY_FILE")
    
    # 构建用户消息
    USER_MSG="【第${round}轮发言请求】

这是第${round}轮。请以你的身份发表正式发言。

${HISTORY:+【之前的讨论】
$HISTORY}

请针对以上讨论，以你的角色身份发表本轮发言。"

    # 清空临时响应文件
    rm -f /tmp/*_resp_$$.txt
    
    # 并行启动所有参与者的回应
    echo "  启动并行发言..."
    
    # 特朗普
    (
        SYSTEM_PROMPT="$TRUMP_PROMPT" call_claude "$USER_MSG" >> /tmp/trump_resp_$$.txt
    ) &
    local trump_pid=$!
    
    # 内塔尼亚胡
    (
        SYSTEM_PROMPT="$NETANYAHU_PROMPT" call_claude "$USER_MSG" >> /tmp/netanyahu_resp_$$.txt
    ) &
    local netanyahu_pid=$!
    
    # 佩泽希齐扬
    (
        SYSTEM_PROMPT="$PEZESHKIAN_PROMPT" call_claude "$USER_MSG" >> /tmp/pezeshkian_resp_$$.txt
    ) &
    local pezeshkian_pid=$!
    
    # 万斯
    (
        SYSTEM_PROMPT="$VANCE_PROMPT" call_claude "$USER_MSG" >> /tmp/vance_resp_$$.txt
    ) &
    local vance_pid=$!
    
    # 普京
    (
        SYSTEM_PROMPT="$PUTIN_PROMPT" call_claude "$USER_MSG" >> /tmp/putin_resp_$$.txt
    ) &
    local putin_pid=$!
    
    # 等待所有进程完成（带超时保护）
    local all_pids="$trump_pid $netanyahu_pid $pezeshkian_pid $vance_pid $putin_pid"
    local timed_out=0
    
    for pid in $all_pids; do
        if ! wait $pid; then
            timed_out=1
        fi
    done
    
    # 读取响应（带默认值）
    local TRUMP_RESP=$(cat /tmp/trump_resp_$$.txt 2>/dev/null || echo "（未响应）")
    local NETANYAHU_RESP=$(cat /tmp/netanyahu_resp_$$.txt 2>/dev/null || echo "（未响应）")
    local PEZESHKIAN_RESP=$(cat /tmp/pezeshkian_resp_$$.txt 2>/dev/null || echo "（未响应）")
    local VANCE_RESP=$(cat /tmp/vance_resp_$$.txt 2>/dev/null || echo "（未响应）")
    local PUTIN_RESP=$(cat /tmp/putin_resp_$$.txt 2>/dev/null || echo "（未响应）")
    
    # 清理临时文件
    rm -f /tmp/*_resp_$$.txt
    
    # 格式化输出
    echo "【特朗普】(第${round}轮)" >> "$HISTORY_FILE"
    echo "$TRUMP_RESP" >> "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    
    echo "【内塔尼亚胡】(第${round}轮)" >> "$HISTORY_FILE"
    echo "$NETANYAHU_RESP" >> "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    
    echo "【佩泽希齐扬】(第${round}轮)" >> "$HISTORY_FILE"
    echo "$PEZESHKIAN_RESP" >> "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    
    echo "【万斯】(第${round}轮)" >> "$HISTORY_FILE"
    echo "$VANCE_RESP" >> "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    
    echo "【普京】(第${round}轮)" >> "$HISTORY_FILE"
    echo "$PUTIN_RESP" >> "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    
    # 主持人总结（顺序执行）
    echo "  主持人总结..."
    local SUMMARY_CONTEXT="这是第${round}轮讨论。各方发言如下：

【特朗普】：$TRUMP_RESP
【内塔尼亚胡】：$NETANYAHU_RESP
【佩泽希齐扬】：$PEZESHKIAN_RESP
【万斯】：$VANCE_RESP
【普京】：$PUTIN_RESP

请以斯塔默的身份，对本轮讨论进行简要总结（100字以内）。"

    SYSTEM_PROMPT="$STARMER_PROMPT" SUMMARY=$(call_claude "$SUMMARY_CONTEXT" 120) || SUMMARY="（主持人未响应）"
    
    echo "【斯塔默总结】(第${round}轮)" >> "$HISTORY_FILE"
    echo "$SUMMARY" >> "$HISTORY_FILE"
    echo "" >> "$HISTORY_FILE"
    
    if [ $timed_out -eq 1 ]; then
        echo "  ⚠️ 部分进程超时"
    fi
    echo "  ✅ 第${round}轮完成"
}

# 运行所有轮次
for round in $(seq 1 $ROUNDS); do
    run_round $round
done

# 生成最终报告
echo ""
echo "📝 生成最终报告..."

REPORT="# 🎭 虚拟论坛：${TOPIC}

> **时间**：$(date '+%Y-%m-%d %H:%M')
> **模式**：对抗性辩论
> **轮次**：${ROUNDS}轮
> **参与者**：特朗普、内塔尼亚胡、佩泽希齐扬、万斯、普京
> **主持人**：斯塔默

---

$(cat "$HISTORY_FILE")

---

*本辩论记录由 Claude Code 并行生成*
*生成时间：$(date '+%Y-%m-%d %H:%M:%S')*"

# 保存报告
OUTPUT_FILE="${OUTPUT_DIR}/虚拟论坛-2026美以伊战争-ClaudeCode.md"
echo "$REPORT" > "$OUTPUT_FILE"

echo ""
echo "✅ 辩论完成！"
echo "📄 结果已保存：$OUTPUT_FILE"
