---
name: sample-asset-skill
description: 用于演示"业务流程处理 + 数字资源入库"闭环的样例 PRD 资产。
---

# Sample Asset Skill

该 Skill 封装一份产品需求文档（`asset-sample.md`），用于演示：

1. **业务流程处理**：将零散的 Markdown 内容通过 `clawhub` 打包、版本化、发布为可检索的 Skill 资产。
2. **数字资源入库**：发布后的 Skill 资产可通过 `agent-browser` 自动化上传到目标资源中心，完成登记与留痕。

## 包含的资源
- `asset-sample.md`：周度销售报告自动化的 PRD（输入 → 处理 → 输出）。
- `SKILL.md`：本文件，说明用途与复现方式。
- `package.json`：版本与元数据。

## 复现参考
- 处理：`clawhub publish ./sample-asset-skill --slug sample-asset-skill --version 1.0.0`
- 入库：`agent-browser open <hub-url>` → snapshot → fill → click → screenshot
