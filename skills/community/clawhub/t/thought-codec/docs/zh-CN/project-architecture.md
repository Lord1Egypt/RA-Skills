# 项目架构

ThoughtCodec 采用中英双语开源 Skill 库结构。每个 Skill 拥有稳定文件夹、英文说明文件和简体中文说明文件。

## 目录树

```text
.
|-- .github/
|   |-- ISSUE_TEMPLATE/
|   |-- pull_request_template.md
|   `-- workflows/
|-- assets/
|   |-- logo.svg
|   |-- logo-mono.svg
|   |-- banner.svg
|   |-- social-preview.svg
|   `-- diagrams/
|-- catalog/
|   `-- skills.json
|-- docs/
|   |-- en/
|   `-- zh-CN/
|-- examples/
|-- scripts/
|-- skills/
|   |-- architecture-scaffolding/
|   |-- sop-instantiation/
|   |-- rule-prompt-optimizer/
|   |-- code-abstraction-encapsulation/
|   `-- personal-methodology-engine/
|-- README.md
|-- README.zh-CN.md
`-- LICENSE
```

## Skill 文件夹模式

```text
skills/<skill-id>/
|-- SKILL.md
|-- SKILL.zh-CN.md
`-- examples/
    `-- basic-usage.md
```

`SKILL.md` 是英文主版本，`SKILL.zh-CN.md` 是简体中文版本。
当某个 Skill 确实需要图片或参考材料时，再添加专属的 `assets/` 或 `references/` 目录。

## 命名规则

- Skill 文件夹使用小写 kebab-case。
- Skill ID 必须与文件夹名和 catalog 条目一致。
- 公共图片资源使用描述性小写命名。
- 中文文档路径或文件名中使用 `zh-CN`。

## Catalog 规则

每个正式发布的 Skill 都必须写入 `catalog/skills.json`，并包含：

- `id`
- 英文和中文标题
- 类型：`decompression`、`compression` 或 `loop`
- 支持模型
- 英文和中文描述
- 英文和中文文件路径

## 视觉资产规则

项目级图片放在 `assets/`。某个 Skill 专属的图片放在对应 Skill 文件夹中。

必要项目图片：

- `assets/logo.svg`
- `assets/logo-mono.svg`
- `assets/banner.svg`
- `assets/social-preview.svg`
- `assets/diagrams/architecture.svg`
- `assets/diagrams/decompression-compression.svg`
- `assets/diagrams/agentic-loop.svg`
