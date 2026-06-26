#!/bin/bash
# Self-Evolution-CN Activator Hook
# 任务完成后提醒评估学习
# 保持输出最小化（~50-100 tokens）

set -e

# 输出提醒作为系统上下文
cat << 'EOF'
<self-evolution-reminder>
完成此任务后，评估是否需要记录学习：
- 发现了非显而易见的解决方案？
- 遇到了意外行为？
- 学到了项目特定的模式？
- 需要调试才能解决的错误？

如果是：使用 self-evolution-cn 技能格式记录到 .learnings/
如果是高价值（重复出现、广泛适用）：考虑技能提取
</self-evolution-reminder>
EOF
