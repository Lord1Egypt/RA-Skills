#!/bin/bash
# ============================================================
# 自动周报生成并发送脚本
# 用途：每周四上午 10:27 自动生成本周周报并发送到飞书
# ============================================================

# 不使用 set -e，避免在某个仓库出错时整个脚本退出

# 配置区
WORK_DIR="/Users/ai/cline-skills"
LOG_FILE="$WORK_DIR/auto-weekly-report.log"

# 记录日志函数
log() {
    echo "[$(date '+%Y-%m-%d %H:%M:%S')] $1" | tee -a "$LOG_FILE"
}

# 配置项目根目录，将自动扫描该目录下所有 Git 仓库
# 可通过环境变量 PROJECT_ROOT 自定义，或直接修改下面的默认值
PROJECT_ROOT="${PROJECT_ROOT:-/your/path}"

# 检查路径是否有效
if [ ! -d "$PROJECT_ROOT" ]; then
    log "❌ 错误：项目根目录不存在：$PROJECT_ROOT"
    log "请设置环境变量 PROJECT_ROOT 或修改脚本中的 PROJECT_ROOT 变量"
    exit 1
fi

# 自动查找所有 Git 仓库
log "扫描 Git 仓库：$PROJECT_ROOT"
GIT_REPOS=()
while IFS= read -r repo; do
    GIT_REPOS+=("$repo")
done < <(find "$PROJECT_ROOT" -maxdepth 2 -type d -name ".git" | sed 's/\/.git$//')

if [ ${#GIT_REPOS[@]} -eq 0 ]; then
    log "⚠️ 未找到任何 Git 仓库"
    exit 1
fi

log "找到 ${#GIT_REPOS[@]} 个 Git 仓库"

log "=========================================="
log "开始自动生成周报"

# 计算本周的日期范围（本周一到今天）
if [[ "$OSTYPE" == "darwin"* ]]; then
    # macOS
    THIS_MONDAY=$(date -v-Mon +%Y-%m-%d)
    TODAY=$(date +%Y-%m-%d)
else
    # Linux
    THIS_MONDAY=$(date -d 'last monday' +%Y-%m-%d)
    TODAY=$(date +%Y-%m-%d)
fi

log "周报时间范围：$THIS_MONDAY 到 $TODAY"

# 生成周报文件名
REPORT_DATE=$(date +%Y%m%d)
REPORT_FILE="$WORK_DIR/weekly-report-$REPORT_DATE.md"

log "生成周报文件：$REPORT_FILE"

# 获取用户信息
GIT_USER=$(git config user.name 2>/dev/null || echo "Unknown")
GIT_EMAIL=$(git config user.email 2>/dev/null || echo "")

log "统计用户：$GIT_USER"

# 初始化统计变量
TOTAL_COMMITS=0
TOTAL_ADD=0
TOTAL_DEL=0
ALL_COMMITS=""

# 遍历所有仓库统计
for REPO in "${GIT_REPOS[@]}"; do
    if [ ! -d "$REPO/.git" ]; then
        log "跳过非 git 仓库：$REPO"
        continue
    fi

    log "统计仓库：$REPO"
    cd "$REPO"

    # 获取提交记录
    COMMITS=$(git log --since="$THIS_MONDAY" --until="$TODAY 23:59:59" \
        --author="$GIT_USER" --format="%ad|%s" --date=short 2>/dev/null || echo "")

    if [ -n "$COMMITS" ]; then
        ALL_COMMITS="$ALL_COMMITS$COMMITS"$'\n'

        # 统计提交次数
        COMMIT_COUNT=$(echo "$COMMITS" | grep -c '^' || echo 0)
        TOTAL_COMMITS=$((TOTAL_COMMITS + COMMIT_COUNT))

        # 统计代码变更
        STATS=$(git log --since="$THIS_MONDAY" --until="$TODAY 23:59:59" \
            --author="$GIT_USER" --pretty=tformat: --numstat 2>/dev/null | \
            awk '{add+=$1; del+=$2} END {print add" "del}')

        if [ -n "$STATS" ]; then
            ADD=$(echo "$STATS" | awk '{print $1}')
            DEL=$(echo "$STATS" | awk '{print $2}')
            TOTAL_ADD=$((TOTAL_ADD + ADD))
            TOTAL_DEL=$((TOTAL_DEL + DEL))
        fi
    fi
done

log "统计完成：$TOTAL_COMMITS 次提交，+$TOTAL_ADD -$TOTAL_DEL 行代码"

# 生成周报内容
cat > "$REPORT_FILE" << EOF
# 周报 - ${THIS_MONDAY} 至 ${TODAY}

## 本周工作内容

EOF

# 分析提交并生成工作内容（这里简化处理，实际使用时由 AI 智能分析）
if [ $TOTAL_COMMITS -eq 0 ]; then
    cat >> "$REPORT_FILE" << EOF
本周无提交记录。

EOF
else
    # 简单按日期分组显示提交（实际使用时应该由 AI 智能归纳）
    echo "$ALL_COMMITS" | grep -v '^$' | sort -r | head -20 | \
        awk -F'|' '{printf "%d. %s；\n", NR, $2}' | \
        sed '$ s/；$/。/' >> "$REPORT_FILE"

    cat >> "$REPORT_FILE" << EOF

EOF
fi

# 添加工作数据
cat >> "$REPORT_FILE" << EOF
## 工作数据

- 提交次数：$TOTAL_COMMITS 次
- 代码变更：+$TOTAL_ADD -$TOTAL_DEL 行
- 统计仓库：${#GIT_REPOS[@]} 个

---

**统计时间**：$(date '+%Y-%m-%d %H:%M:%S')
**生成工具**：Auto Weekly Report Generator
EOF

log "周报生成完成：$REPORT_FILE"
log "📝 周报已保存，等待 AI 优化后统一发送"
log "=========================================="

# 注：原自动发送功能已移除
# 现在由 AI 优化周报内容后统一调用 send-to-feishu.sh 发送
# 避免重复发送周报到飞书
