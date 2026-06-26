#!/bin/bash
# 快速技能练习日志脚本
# 用法: ./quick-log.sh <技能名称> <分钟数> <质量评分>

if [ $# -lt 3 ]; then
    echo "用法: $0 <技能名称> <练习分钟数> <质量评分(1-10)>"
    echo "示例: $0 Python编程 45 7"
    exit 1
fi

SKILL_NAME="$1"
DURATION="$2"
QUALITY="$3"
DATE=$(date +%Y%m%d)
TIMESTAMP=$(date -Iseconds)

# 创建技能目录（如果不存在）
mkdir -p ".learnings/skills"

# 追加日志条目
cat >> ".learnings/skills/${SKILL_NAME}.md" << EOF

## [PRC-${DATE}-001] Practice Session

**Logged**: ${TIMESTAMP}Z
**Duration**: ${DURATION} minutes
**Quality Score**: ${QUALITY}/10
**Focus Areas**: [填写练习重点]
**Energy Level**: [1-10]
**Distractions**: [low/medium/high]

### What I Practiced
- [填写具体内容]

### Challenges & Breakthroughs
- Challenge: 
- Breakthrough: 
- Still confused: 

### Key Insights
1. 
2. 
3. 

### Next Session Focus
1. 
2. 
3. 

### Metrics Update
- [技能维度]: [旧分] → [新分]/10
- Confidence: [旧分] → [新分]/10

---
EOF

echo "✅ 练习日志已添加到 .learnings/skills/${SKILL_NAME}.md"
echo "📝 请编辑文件填写详细信息"