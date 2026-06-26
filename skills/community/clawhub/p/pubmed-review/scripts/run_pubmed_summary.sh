#!/bin/bash
# PubMed Summary Processor
# 用法: bash run_pubmed_summary.sh <articles_json> <task_id>
set -e

ARTICLES_JSON="$1"
TASK_ID="$2"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
BASE_DIR="$(dirname "$SCRIPT_DIR")"  # scripts/ 的父目录即项目根目录
RESULTS_DIR="${BASE_DIR}/results/pubmed"
# notify 路径：优先环境变量，其次尝试 which
NOTIFY_SCRIPT="${NOTIFY_PATH:-$(which notify 2>/dev/null || echo '/usr/local/bin/notify')}"

echo "[pubmed_summary] 开始生成综述: TASK_ID=$TASK_ID"

# 检查 articles_json 是否存在
if [ ! -f "$ARTICLES_JSON" ]; then
    echo "[pubmed_summary] ERROR: articles.json 不存在: $ARTICLES_JSON"
    exit 1
fi

# 输出 summary.md 路径
SUMMARY_FILE="${RESULTS_DIR}/${TASK_ID}_summary.md"

# 加载 MiniMax LLM 环境变量（优先环境变量指定文件，其次项目根目录 .env.minimax）
MINIMAX_ENV_FILE="${MINIMAX_ENV_FILE:-${BASE_DIR}/.env.minimax}"
if [ -f "$MINIMAX_ENV_FILE" ]; then
    set -a && source "$MINIMAX_ENV_FILE" && set +a
fi

# 调用 LLM 生成综述
echo "[pubmed_summary] 调用 pubmed_llm_summarize.py ... (model=$MINIMAX_MODEL)"
set +e
LLM_OUTPUT=$(python3 "${SCRIPT_DIR}/pubmed_llm_summarize.py" "$ARTICLES_JSON" "$SUMMARY_FILE" 2>&1)
LLM_EXIT=$?
set -e

if [ $LLM_EXIT -ne 0 ]; then
    echo "[pubmed_summary] ERROR: pubmed_llm_summarize.py 失败，退出码: $LLM_EXIT"
    exit 1
fi

if [ ! -f "$SUMMARY_FILE" ]; then
    echo "[pubmed_summary] ERROR: summary.md 未生成: $SUMMARY_FILE"
    exit 1
fi

SUMMARY_SIZE=$(stat -c%s "$SUMMARY_FILE" 2>/dev/null || echo "0")
echo "[pubmed_summary] 综述已生成: $SUMMARY_FILE (${SUMMARY_SIZE} bytes)"

# 从 LLM_OUTPUT 中提取 brief（跳过日志行，保留剩余内容）
BRIEF=$(echo "$LLM_OUTPUT" | grep -v '^\[' | grep -v '^$' | tail -n +2)

if [ -z "$BRIEF" ]; then
    BRIEF="综述已生成，详见文件。"
fi

# 获取 topic 和文章数
TOPIC=$(python3 -c "
import json
try:
    tasks_file = '${BASE_DIR}/tasks/ablesci_tasks.json'
    with open(tasks_file) as f:
        for t in json.load(f):
            if t.get('id') == '${TASK_ID}':
                print(t.get('payload', {}).get('topic', '${TASK_ID}'))
                break
        else:
            print('${TASK_ID}')
except:
    print('${TASK_ID}')
" 2>/dev/null)

ARTICLE_COUNT=$(python3 -c "
import json
with open('${ARTICLES_JSON}') as f:
    articles = json.load(f)
print(len(articles))
" 2>/dev/null || echo "?")

MESSAGE="📋 PubMed 文献综述完成

主题：${TOPIC}
摘要提取：${ARTICLE_COUNT} 篇
综述文件：${SUMMARY_FILE}

---
${BRIEF}"...


echo "[pubmed_summary] 发送飞书通知..."
MSG_FILE=$(mktemp)
echo "$MESSAGE" > "$MSG_FILE"
set +e
$NOTIFY_SCRIPT -t "PubMed文献综述完成" -m "$(cat "$MSG_FILE")"
NOTIFY_EXIT=$?
set -e
rm -f "$MSG_FILE"
if [ $NOTIFY_EXIT -ne 0 ]; then
    echo "[pubmed_summary] ERROR: 飞书通知发送失败，退出码: $NOTIFY_EXIT"
else
    echo "[pubmed_summary] 飞书通知发送成功"
fi

echo "[pubmed_summary] 完成"
exit 0
