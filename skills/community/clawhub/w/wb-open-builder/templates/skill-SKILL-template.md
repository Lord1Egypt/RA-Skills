---
name: {{skill-name}}                          # 选填：技能标识，kebab-case
display_name: {{展示名称}}                     # 选填：市场展示名
display_name_en: {{English Display Name}}     # 选填：英文展示名
description: {{一句话描述技能能力，写清用途和触发词}}   # 必填
description_zh: {{简短中文介绍}}               # 必填
description_en: {{A Brief English Introduction}}  # 必填
category: {{平台分类之一，示例 writing}}        # 选填：取值以开放平台创建页为准
allowed-tools: {{Tool1, Tool2, Tool3}}        # 选填：工具白名单（逗号分隔）
version: 1.0.0                                # 必填：语义化版本 x.y.z
disable-model-invocation: false               # 选填：true 则 AI 不自动触发，仅手动调用
user-invocable: true                          # 选填：false 则隐藏菜单，仅供 AI 内部使用
author: {{合作方名称}}                         # 必填
---

<!-- 填充说明：必填字段（description/description_zh/description_en/version/author）一个不缺；选填字段按需保留，不需要的整行删除（省略即默认行为）；行内 # 注释填充后删除 -->

# {{技能标题}}

当用户需要 {{触发场景}} 时，按以下步骤执行：

1. {{步骤一：输入与前置确认}}
2. {{步骤二：核心处理流程}}
3. {{步骤三：输出与落盘}}

## 输出规范

- {{输出格式、质量要求、不确定信息标注规则}}

## 子资源引用（按需保留）

- 规范与知识文档：@references/{{doc-name}}.md
- 可执行脚本：`python scripts/{{script-name}}.py {{args}}`（依赖：{{runtime}}）
- 模板文件：templates/{{template-name}}
