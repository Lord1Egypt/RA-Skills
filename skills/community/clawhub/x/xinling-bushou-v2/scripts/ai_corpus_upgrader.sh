#!/bin/bash
#
# 心灵补手 AI 语料扩充脚本
# 使用subagent调用AI生成元特征库和语料
#

UPGRADE_DIR="/root/.openclaw/workspace/xinling-bushou-v2"
META_DIR="$UPGRADE_DIR/meta_features"
PERSONAS_DIR="$UPGRADE_DIR/personas"
CORPUS_DIR="$UPGRADE_DIR/corpus"
LOG_FILE="$UPGRADE_DIR/logs/ai_corpus_$(date +%Y%m%d).log"

mkdir -p "$META_DIR" "$CORPUS_DIR"

echo "============================================" | tee -a "$LOG_FILE"
echo "心灵补手 AI 语料扩充器 $(date '+%Y-%m-%d %H:%M:%S')" | tee -a "$LOG_FILE"
echo "============================================" | tee -a "$LOG_FILE"

# 获取未建元特征库的人格
persona_files=$(ls -1 "$PERSONAS_DIR"/*.json 2>/dev/null | grep -v "_registry" | sed 's/.*\///' | sed 's/\.json//')
meta_files=$(ls -1 "$META_DIR"/*.json 2>/dev/null | sed 's/.*\///' | sed 's/_meta\.json//')

echo "人格列表: $persona_files" | tee -a "$LOG_FILE"
echo "已建元特征: $meta_files" | tee -a "$LOG_FILE"

# 找未建元特征的人格
for persona in $persona_files; do
    if [[ ! " $meta_files " =~ " $persona " ]]; then
        TARGET_PERSONA="$persona"
        break
    fi
done

if [ -z "$TARGET_PERSONA" ]; then
    echo "所有人格已建元特征库，随机选择扩充语料" | tee -a "$LOG_FILE"
    TARGET_PERSONA=$(echo "$persona_files" | tr ' ' '\n' | shuf -n1)
    IS_CORPUS_ONLY=1
else
    IS_CORPUS_ONLY=0
fi

echo "目标人格: $TARGET_PERSONA" | tee -a "$LOG_FILE"

# 读取人格信息
PERSONA_FILE="$PERSONAS_DIR/${TARGET_PERSONA}.json"
if [ ! -f "$PERSONA_FILE" ]; then
    echo "人格文件不存在: $PERSONA_FILE" | tee -a "$LOG_FILE"
    exit 1
fi

NAME=$(python3 -c "import json; d=json.load(open('$PERSONA_FILE')); print(d.get('name', d.get('meta', {}).get('name', '$TARGET_PERSONA')))")
DESC=$(python3 -c "import json; d=json.load(open('$PERSONA_FILE')); print(d.get('description', d.get('meta', {}).get('description', '')))")

echo "人物: $NAME" | tee -a "$LOG_FILE"
echo "描述: $DESC" | tee -a "$LOG_FILE"

if [ "$IS_CORPUS_ONLY" -eq 0 ]; then
    echo "任务: 建立元特征库" | tee -a "$LOG_FILE"
else
    echo "任务: 扩充语料" | tee -a "$LOG_FILE"
fi

echo "============================================" | tee -a "$LOG_FILE"
echo "完成" | tee -a "$LOG_FILE"
