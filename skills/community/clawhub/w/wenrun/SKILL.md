---
name: wenrun
version: 1.0.1
model: default
description: 文润 — 中文AI文本自然度检测与润色。检测中文AI文本中的模板化痕迹并给出优化建议。
use_when:
  - 写完后想去掉AI味的文章、报告、公众号内容
  - 批量检测文本的"AI度"
  - 在上传前检查内容自然度
  - 作为AI助手的后处理步骤
trigger_keywords:
  - 去AI味
  - 润色
  - 自然度
  - AI检测
  - 文字优化
  - 中文润色
  - 写作文风
  - humanize
environment: local
network: none
dependencies: none (Python stdlib only)
disclaimer: 本工具优化建议仅供参考，不保证完全消除AI检测特征。最终内容责任由用户自行承担。
---

# 文润 (WenRun)

中文 AI 文本自然度检测与优化工具。

## 功能

| 模式 | 说明 |
|------|------|
| **分析** | 扫描文本，识别 AI 文本特征，输出 AI 度评分 + 问题定位 |
| **润色** | 基于分析结果自动改写，可配置风格（日常、学术、营销、自媒体）[即将推出]|

## 使用方式

```bash
# 分析文本
python3 scripts/wenrun.py analyze --text "要检测的文章内容..."

# 分析文件
python3 scripts/wenrun.py analyze --file article.txt

# 润色文本
python3 scripts/wenrun.py polish --text "要润色的内容..." --style casual

# 润色文件
python3 scripts/wenrun.py polish --file article.txt --style wechat
```

## 特征库

当前版本内置 8 大类 60+ 条中文 AI 文本特征规则。
详见 [features/ai-patterns.json](features/ai-patterns.json)。

## 免责声明

**重要声明：**
1. **仅供参考**：本工具的分析结果和建议仅供参考，不构成对 AI 检测结果的保证。
2. **非保证**：本工具无法保证 100% 准确识别 AI 生成文本，存在误报和漏报的可能。
3. **用户责任**：最终内容质量和使用责任由用户自行承担。
4. **持续迭代**：AI 文本特征不断变化，本工具的特征库将持续更新。

**Disclaimer (English):**
1. **For Reference Only**: Analysis results and suggestions are for reference only and do not guarantee AI detection accuracy.
2. **No Guarantee**: This tool cannot guarantee 100% accuracy in identifying AI-generated text.
3. **User Responsibility**: The ultimate responsibility for content quality and use rests with the user.
4. **Continuous Updates**: AI text patterns evolve; this tool's feature library will be updated accordingly.
