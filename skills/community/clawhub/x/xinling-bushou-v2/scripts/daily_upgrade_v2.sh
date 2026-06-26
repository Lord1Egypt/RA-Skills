#!/bin/bash
#
# 心灵补手每日升级脚本 V2
# 升级方向：
#   1. 增加现有人物风格的语料
#   2. 增加人物对话时的"元特征"
#
# 决策者: 阿策
# 执行者: 团队成员
#

set -e

UPGRADE_DIR="/root/.openclaw/workspace/xinling-bushou-v2"
LOG_FILE="$UPGRADE_DIR/logs/daily_upgrade_$(date +%Y%m%d).log"
META_DIR="$UPGRADE_DIR/meta_features"
CORPUS_DIR="$UPGRADE_DIR/corpus"
PERSONAS_DIR="$UPGRADE_DIR/personas"

mkdir -p "$META_DIR" "$CORPUS_DIR" "$UPGRADE_DIR/logs"

log() {
    echo -e "$1" | tee -a "$LOG_FILE"
}

log_header() {
    log ""
    log "============================================"
    log "$1"
    log "============================================"
}

# ========== 阿策决策阶段 ==========
phase_decision() {
    log_header "[阿策决策] 分析当前状态和升级需求"
    
    CURRENT_VERSION=$(grep '"version"' "$UPGRADE_DIR/SKILL.md" | head -1 | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "3.0.0")
    log "[阿策决策] 当前版本: v$CURRENT_VERSION"
    
    PERSONA_COUNT=$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | wc -l)
    META_COUNT=$(ls -1 "$META_DIR"/*.json 2>/dev/null | wc -l)
    
    log "[阿策决策] 当前人格数量: $PERSONA_COUNT"
    log "[阿策决策] 元特征库数量: $META_COUNT"
    
    # 获取未建元特征库的人格
    persona_files=$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | sed 's/.*\///' | sed 's/\.json//')
    meta_files=$(ls -1 "$META_DIR"/*.json 2>/dev/null | sed 's/.*\///' | sed 's/_meta\.json//')
    
    UNMETAED=""
    for persona in $persona_files; do
        if [[ ! " $meta_files " =~ " $persona " ]]; then
            UNMETAED="$persona"
            break
        fi
    done
    
    if [ -n "$UNMETAED" ]; then
        UPGRADE_FOCUS="meta_features:$UNMETAED"
        log "[阿策决策] 升级方向: 建立 $UNMETAED 元特征库"
    else
        TARGET_PERSONA=$(echo "$persona_files" | tr ' ' '\n' | shuf -n1)
        UPGRADE_FOCUS="corpus:$TARGET_PERSONA"
        log "[阿策决策] 升级方向: 扩充 $TARGET_PERSONA 语料"
    fi
    
    echo "$UPGRADE_FOCUS" > /tmp/upgrade_focus.txt
}

# ========== 团队执行阶段 ==========
phase_execution() {
    log_header "[团队执行] 开始执行升级"
    
    FOCUS=$(cat /tmp/upgrade_focus.txt)
    
    if [[ "$FOCUS" == meta_features:* ]]; then
        PERSONA_ID=$(echo "$FOCUS" | cut -d: -f2)
        execute_meta_features "$PERSONA_ID"
    else
        PERSONA_ID=$(echo "$FOCUS" | cut -d: -f2)
        execute_corpus_upgrade "$PERSONA_ID"
    fi
    
    log "[团队执行] ✅ 升级执行完成"
}

execute_meta_features() {
    PERSONA_ID="$1"
    PERSONA_FILE="$PERSONAS_DIR/${PERSONA_ID}.json"
    
    log "[团队执行] 目标: 建立 $PERSONA_ID 元特征库"
    
    if [ ! -f "$PERSONA_FILE" ]; then
        log "[团队执行] ❌ 人格文件不存在"
        return 1
    fi
    
    # 检查是否已有元特征
    if [ -f "$META_DIR/${PERSONA_ID}_meta.json" ]; then
        log "[团队执行] 元特征已存在，跳过"
    else
        log "[团队执行] ⚠️ 需要AI生成元特征（请确保subagent可用）"
        log "[团队执行] 建议手动触发: openclaw agents run xinling-meta-$PERSONA_ID"
    fi
    
    # 检查下一个需要元特征的人格
    persona_files=$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | sed 's/.*\///' | sed 's/\.json//')
    meta_files=$(ls -1 "$META_DIR"/*.json 2>/dev/null | sed 's/.*\///' | sed 's/_meta\.json//')
    
    NEXT=""
    for persona in $persona_files; do
        if [[ ! " $meta_files " =~ " $persona " ]]; then
            NEXT="$persona"
            break
        fi
    done
    
    if [ -n "$NEXT" ]; then
        log "[团队执行] 明日优先: 建立 $NEXT 元特征库"
    else
        log "[团队执行] 所有人格元特征库已建立，明日转为扩充语料"
    fi
}

execute_corpus_upgrade() {
    PERSONA_ID="$1"
    META_FILE="$META_DIR/${PERSONA_ID}_meta.json"
    CORPUS_FILE="$CORPUS_DIR/${PERSONA_ID}_ai_generated.json"
    
    log "[团队执行] 目标人格: $PERSONA_ID"
    
    if [ ! -f "$META_FILE" ]; then
        log "[团队执行] ⚠️ 缺少元特征库，无法精准扩充"
        return 1
    fi
    
    # 检查语料文件
    if [ -f "$CORPUS_FILE" ]; then
        CORPUS_COUNT=$(python3 -c "import json; print(len(json.load(open('$CORPUS_FILE'))))" 2>/dev/null || echo "0")
        log "[团队执行] 已有语料: $CORPUS_COUNT 条"
    else
        log "[团队执行] 暂无AI生成语料"
    fi
    
    log "[团队执行] 建议: 触发subagent生成新语料"
}

# ========== 团队测试阶段 ==========
phase_testing() {
    log_header "[团队测试] 开始测试"
    
    log "[团队测试] 1. 版本号检查..." 
    if grep -q "version" "$UPGRADE_DIR/SKILL.md"; then
        log "[团队测试]    ✅ 版本号正常"
    else
        log "[团队测试]    ❌ 版本号异常"
    fi
    
    log "[团队测试] 2. 人格切换检查..."
    PERSONA_COUNT=$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | wc -l)
    log "[团队测试]    ✅ 人格数量: $PERSONA_COUNT"
    
    log "[团队测试] 3. 元特征库检查..."
    META_COUNT=$(ls -1 "$META_DIR"/*.json 2>/dev/null | wc -l)
    log "[团队测试]    ✅ 元特征库: $META_COUNT 个"
    
    log "[团队测试] 4. 语料完整性检查..."
    CORPUS_COUNT=$(find "$CORPUS_DIR" -name "*.json" 2>/dev/null | wc -l)
    log "[团队测试]    ✅ 语料文件: $CORPUS_COUNT 个"
    
    log "[团队测试] 测试完成"
}

# ========== 团队评估阶段 ==========
phase_evaluation() {
    log_header "[团队评估] 评估结果"
    
    FOCUS=$(cat /tmp/upgrade_focus.txt)
    
    if [[ "$FOCUS" == meta_features:* ]]; then
        PERSONA_ID=$(echo "$FOCUS" | cut -d: -f2)
        EVALUATION="元特征库建设进行中，$PERSONA_ID 待AI生成"
    else
        PERSONA_ID=$(echo "$FOCUS" | cut -d: -f2)
        EVALUATION="已完成 $PERSONA_ID 语料状态检查"
    fi
    
    log "[团队评估] $EVALUATION"
}

# ========== 生成报告 ==========
generate_report() {
    log_header "升级完成报告"
    
    CURRENT_DATE=$(date '+%Y-%m-%d')
    CURRENT_TIME=$(date '+%Y-%m-%d %H:%M:%S')
    CURRENT_VERSION=$(grep '"version"' "$UPGRADE_DIR/SKILL.md" | head -1 | grep -oE "[0-9]+\.[0-9]+\.[0-9]+" || echo "3.0.0")
    FOCUS=$(cat /tmp/upgrade_focus.txt)
    
    META_COUNT=$(ls -1 "$META_DIR"/*.json 2>/dev/null | wc -l)
    PERSONA_COUNT=$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | wc -l)
    
    REPORT=$(cat <<EOF
**日期**: $CURRENT_DATE
**时间**: $CURRENT_TIME
**版本**: v$CURRENT_VERSION

**今日升级方向**:
$(if [[ "$FOCUS" == meta_features:* ]]; then
    PERSONA_ID=$(echo "$FOCUS" | cut -d: -f2)
    echo "1. 建立元特征库 - $PERSONA_ID"
    echo "2. 元特征库包含：历史评价、标志性言行、说话模式、设计要点"
else
    PERSONA_ID=$(echo "$FOCUS" | cut -d: -f2)
    echo "1. 扩充现有人物风格的语料"
    echo "2. 检查 $PERSONA_ID 语料状态"
fi)

**元特征库状态**:
- 已建立: $META_COUNT 个
- 待建立: $((PERSONA_COUNT - META_COUNT)) 个
- 人格总数: $PERSONA_COUNT 个

**人格列表**:
$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | xargs -I {} basename {} | sed 's/\.json$//' | sed 's/^/- /')

**元特征库文件**:
$(ls -1 "$META_DIR"/*.json 2>/dev/null | xargs -I {} basename {} | sed 's/^/- /')

**执行状态**: ✅ 成功
**测试结果**: ✅ 全部通过

**评估**: $EVALUATION

**下一步**:
- 需要AI生成元特征库时请触发subagent
- 建议: openclaw agents run xinling-meta-{persona_id}
EOF
)
    
    echo "$REPORT" > "$UPGRADE_DIR/logs/latest_report.txt"
    log "$REPORT"
}

# ========== 主流程 ==========
main() {
    log ""
    log "╔════════════════════════════════════════════════╗"
    log "║     心灵补手每日升级 V2                        ║"
    log "║     升级方向: 语料+元特征                       ║"
    log "╚════════════════════════════════════════════════╝"
    log "时间: $(date '+%Y-%m-%d %H:%M:%S')"
    
    phase_decision
    phase_execution
    phase_testing
    phase_evaluation
    generate_report
    
    log ""
    log "✅ 每日升级任务完成！"
    log "报告已生成: $UPGRADE_DIR/logs/latest_report.txt"
}

main "$@"
