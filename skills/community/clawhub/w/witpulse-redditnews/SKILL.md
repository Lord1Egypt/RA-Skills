---
name: WitPulse-redditnews
description: 主动式 Reddit 科技热点感知，结合当前会话上下文，以毒舌幽默风格生成科技圈热点点评。
---

# WitPulse-redditnews (v1.1.0)

你的专属科技舆情雷达，主动监测 Reddit 热点。本 Skill 为纯文本驱动，不含任何二进制组件。

## 快速运行
直接调用 Python 脚本即可执行任务：

- **抓取热点**: 
  `python3 ~/.agents/skills/WitPulse-redditnews/scripts/fetch_reddit.py`
- **运行分析链**: 
  `bash ~/.agents/skills/WitPulse-redditnews/scripts/run_witpulse.sh`
- **连通性校验**: 
  `python3 ~/.agents/skills/WitPulse-redditnews/scripts/validate_subreddits.py`

## 核心配置
通过 `config.json` 自定义关注领域：
```json
{"subreddits": ["r/technology"], "language": "zh-CN"}
```

## 输出标准 (Mandatory Audit Protocol)
本 Skill 提供的输出流必须由 Agent 严格审计，确保包含：
1. **[标题](链接)**: 源头真实性校验。
2. **[深度点评]**: 结合上下文的毒舌金句。

*注：本 skill 的“上下文联动”依赖于 Agent 的推理能力。*
