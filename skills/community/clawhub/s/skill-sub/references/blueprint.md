# 步骤蓝皮书

skill-sub 将每个已安装技能的 SKILL.md 解析为结构化步骤蓝图，供搜索和链规划使用。

**硬约束：** search 命令自动比对指纹，过期直接拒绝搜索。
**LLM 提取路径：** check-fingerprint → prepare-llm-input → LLM → apply-blueprint
**Regex 兜底：** scan --force
