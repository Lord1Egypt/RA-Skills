---
name: zotero-scholar
description: 将论文和摘要保存到 Zotero 文库。需配置 ZOTERO_CREDENTIALS 环境变量。
homepage: https://www.zotero.org
metadata:
  {
    "openclaw":
      {
        "emoji": "🧠",
        "requires": { "bins": ["uv"], "env": ["ZOTERO_CREDENTIALS"] },
        "primaryEnv": "ZOTERO_CREDENTIALS"
      }
  }
---

# Zotero Scholar

专业的文献入库助手。可以将论文元数据、PDF 链接以及 AI 生成的总结一键保存到你的 Zotero 库中。

## 配置说明

此 Skill 需要配置 `ZOTERO_CREDENTIALS` 环境变量，格式为 `userID:apiKey`。
例如：`123456:ksjdflkjsdflkjsdf`。

## 使用示例

### 使用环境变量运行

```bash
uv run {baseDir}/scripts/save_paper.py \
  --title "Attention Is All You Need" \
  --authors "Vaswani et al." \
  --url "https://arxiv.org/abs/1706.03762"
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--title` | 论文标题 |
| `--authors` | 作者列表（逗号分隔） |
| `--url` | 论文链接 (用于排重) |
| `--abstract` | 论文摘要 |
| `--summary` | (AI 生成) 简短总结或 Insight |
| `--tags` | 标签列表（逗号分隔） |

## 依赖说明

此 Skill 包含自我管理的依赖配置（PEP 723）。执行 `uv run` 时会自动安装 `pyzotero`。
