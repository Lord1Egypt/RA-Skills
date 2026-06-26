---
name: zotero-scholar
description: 将论文保存到 Zotero 文库，请按照 userid:apiKey 的格式配置 ZOTERO_CREDENTIALS 环境变量。
homepage: https://www.zotero.org
metadata:
  {
    "openclaw":
      {
        "emoji": "📚",
        "requires": { "bins": ["python"], "env": ["ZOTERO_CREDENTIALS"] },
        "primaryEnv": "ZOTERO_CREDENTIALS"
      }
  }
---

# Zotero Scholar

专业的文献入库助手。可以将论文元数据、PDF 链接以及 AI 生成的总结一键保存到你的 Zotero 库中。

## 使用说明

此 Skill 依赖本机安装的 Python（建议 Python 3.10 或更高版本），不再要求 `brew` 或 `uv`。

环境变量 `ZOTERO_CREDENTIALS` 的格式为：

```bash
userid:apiKey
```

例如在 Windows PowerShell 中：

```powershell
$env:ZOTERO_CREDENTIALS="你的userid:你的apiKey"
```

例如在 Windows CMD 中：

```cmd
set ZOTERO_CREDENTIALS=你的userid:你的apiKey
```

## 使用示例

```bash
python {baseDir}/scripts/save_paper.py \
  --title "Attention Is All You Need" \
  --authors "Vaswani et al." \
  --url "https://arxiv.org/abs/1706.03762"
```

## 依赖安装

请先在本机安装 Python 依赖：

```bash
pip install pyzotero
```

## 参数说明

| 参数 | 说明 |
|------|------|
| `--title` | 论文标题 |
| `--authors` | 作者列表（逗号分隔） |
| `--url` | 论文链接（用于排重） |
| `--abstract` | 论文摘要 |
| `--summary` | AI 生成的简短总结或 Insight |
| `--tags` | 标签列表（逗号分隔） |
