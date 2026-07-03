---
name: skillpress
description: "技能锻造炉。从对话/任务中分析可重复流程，自动生成标准 SKILL.md 模板。受 Claude Code Skillify 设计模式启发，完全原创实现——不涉及任何泄露代码。"
metadata:
  openclaw:
    emoji: "🔨"
    requires:
      bins: [python3]
---

# OpenClaw SkillForge 🔨

> 灵感来自 Claude Code 的 Skillify 模式：把一次完成的流程自动转化为可复用的技能。
> 实现完全原创。

## 使用方式

### 从当前会话生成技能
当完成一个重复性任务后，告诉我："把这个流程做成技能"。

我会：
1. 分析任务步骤
2. 提取输入参数和判断条件
3. 生成标准 SKILL.md 模板
4. 创建对应的脚本骨架

### 手动使用
```bash
python3 {{SKILL_DIR}}/scripts/forge.py create my-skill \
  --name "技能名称" \
  --emoji "🔧" \
  --description "一句话描述" \
  --steps step1,step2,step3 \
  --bins python3
```

### 查看已生成的技能信息
```bash
python3 {{SKILL_DIR}}/scripts/forge.py info my-skill
```
