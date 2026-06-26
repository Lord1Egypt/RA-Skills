---
name: wechat-favorites
description: 微信收藏夹导出、智能分类与知识库管理。支持从解析后的 favorite.db 导出收藏记录、自动归纳分类（从用户内容发现自然类别）、LLM 智能增强（可选）、批量导入 IMA 知识库（可选）、多平台导出（Obsidian/Notion，可选）、增量分类。核心功能支持离线使用，网络功能默认关闭。
metadata:
  version: 1.2.0
  display_name: 微信收藏知识库
---

# 微信收藏知识库

Decrypt, categorize and organize wechat favorites (Official Account collection) into knowledge base

收藏夹导出 · 智能分类 · 知识库导入 · 多平台导出

**快速上手：** 解析收藏夹 → 导出记录 → 自动归纳类别 → 智能分类 → 导出到 Obsidian/Notion 或导入 IMA

> 💡 **试试这样说：** "帮我整理微信收藏" / "导出收藏夹并自动归纳分类" / "从我的收藏中发现自然类别" / "把微信收藏导入知识库"

---

**触发词：** 微信收藏（WeChat Favorites）、收藏夹导出（favorites export）、收藏文章分类（favorites classification）、自动归纳分类（auto-discover categories）、IMA 知识库导入（knowledge base import）、Obsidian 导出（Obsidian export）、Notion 导出（Notion export）、收藏整理（favorites organizer）

---

## 新增功能

> 完整更新日志见 [CHANGELOG.md](CHANGELOG.md)

- **自动归纳分类** — 从收藏内容中 LLM 发现自然类别，不再受限于固定 9 大类
- **Obsidian / Notion 导出** — Markdown 按年月归档+增量同步 / 批量导入 Notion 数据库
- **LLM 增量分类** — 新增收藏无需全量重跑，支持结果合并与标签标准化
- **自定义分类** — classify_favorites.py 新增 `--categories` 参数，支持自定义分类 JSON

---

## 为什么用这个工具？

微信收藏夹积累了大量文章：随手打的标签越来越复杂，待读越积越多，从来没有真正整理过，也不记得读了哪些、学到了什么。这个工具可以：

- **自动归纳** — 从你的收藏中发现自然类别，不再受限于固定分类
- **关键词匹配** — 快速扫描全部收藏，按关键词归类
- **LLM 增强** — 低置信度条目用大模型智能重判（可选）
- **知识库导入** — 一键导入 IMA，构建个人知识库（可选）
- **多平台导出** — 导出为 Markdown 到 Obsidian，或批量导入 Notion 数据库（可选）
- **增量分类** — 新增收藏无需全量重跑，LLM 增量分类 + 结果合并

---

## 核心能力

| 能力 | 说明 |
|------|------|
| **收藏导出** | 从解析后的 `favorite.db` 导出全部收藏记录为 CSV |
| **自动归纳** | 从用户收藏内容自动发现分类体系（v1.2 新增） |
| **关键词分类** | 默认 9 大类（生物医药/AI/投资等），或使用自定义分类 |
| **标签增强** | 二级标签 57 个 + 跨领域标签 6 类（仅默认分类） |
| **LLM 增强（可选）** | 置信度低时自动调用 LLM 二次分类，需配置 API Key |
| **IMA导入（可选）** | 批量导入到 IMA 知识库，需配置凭证 |
| **Notion 导出（可选）** | 导出收藏到 Notion 数据库，需配置 API Token（v1.2 新增） |
| **Obsidian 导出（可选）** | 导出收藏为 Markdown 文件到 Obsidian vault（v1.2 新增） |
| **报告生成** | 分类统计、各分类 CSV 导出 |

---

## 前置条件

### 1. 微信收藏数据库

本工具需要已解析的 `favorite.db` 文件。解析步骤请使用专门的微信数据库处理工具。

### 2. Python 环境

```bash
pip install pycryptodome zstandard
```

### 3. LLM 配置（自动归纳需要）

自动归纳功能需要调用 LLM API：

```bash
export LLM_API_KEY="your-openrouter-api-key"
export LLM_API_URL="https://openrouter.ai/api/v1/chat/completions"
export LLM_MODEL="deepseek/deepseek-chat"
```

或使用本地模型：

```bash
export LLM_API_URL="http://localhost:11434/v1/chat/completions"
export LLM_MODEL="qwen2.5:14b"
```

### 4. IMA 导入（可选）

如需导入 IMA 知识库，配置凭证：`~/.config/ima/client_id` 和 `~/.config/ima/api_key`

### 5. Notion 导出（可选）

如需导出到 Notion，配置 API Token：

```bash
export NOTION_API_TOKEN="secret_xxx"
```

### 6. Obsidian 导出（可选）

无需额外配置，直接指定 vault 路径即可。

---

## 快速开始

### 方式一：自动归纳分类（推荐）

```bash
cd scripts

# 1. 导出收藏记录
python export_favorites.py

# 2. 自动发现分类体系
python auto_discover.py

# 3. 使用自定义分类
python classify_favorites.py --categories user_categories.json

# 4. 导入 IMA（可选）
python import_ima.py
```

### 方式二：使用默认 9 大类

```bash
cd scripts

# 1. 导出收藏记录
python export_favorites.py

# 2. 使用默认分类
python classify_favorites.py

# 3. 导入 IMA（可选）
python import_ima.py
```

### 方式三：导出到 Notion / Obsidian（可选）

```bash
# 导出分类后的文章到 Notion 数据库
python export_to_notion.py --input articles_final.csv --token $NOTION_API_KEY --database-id $DATABASE_ID

# 导出到 Obsidian vault（Markdown 文件）
python export_to_obsidian.py --input articles_final.csv --vault "D:\Obsidian\MyVault"
```

---

## 目录结构

```
wechat-favorites/
├── SKILL.md                     # 本文件
├── LICENSE.txt                  # MIT License
├── requirements.txt             # 依赖声明
├── scripts/
│   ├── auto_discover.py         # 自动归纳分类（v1.2 新增）
│   ├── classify_favorites.py    # 智能分类
│   ├── llm_classify.py          # LLM 二次分类模块
│   ├── llm_incremental.py       # LLM 增量分类（v1.2 新增）
│   ├── merge_llm_results.py      # 合并多次 LLM 结果（v1.2 新增）
│   ├── normalize_categories.py   # 分类标准化（v1.2 新增）
│   ├── export_favorites.py      # 收藏导出
│   ├── export_to_notion.py      # 导出至 Notion（v1.2 新增）
│   ├── export_to_obsidian.py    # 导出至 Obsidian（v1.2 新增）
│   ├── import_ima.py            # IMA 导入
│   └── ...
├── exported_favorites/          # 导出输出
│   ├── favorites_all.csv        # 全部收藏
│   ├── user_categories.json     # 自动归纳的分类体系
│   ├── articles_final.csv       # 带分类标签
│   └── cat_*.csv                # 各分类文件
└── references/
    ├── classification.md        # 分类算法说明
    └── schema.md                # 数据库结构
```

---

## 数据流程

### 自动归纳流程

```
favorites_all.csv
      │
      ▼ auto_discover.py（采样 + LLM 归纳）
user_categories.json
      │
      ▼ classify_favorites.py --categories user_categories.json
articles_final.csv + cat_*.csv
```

### 默认分类流程

```
favorites_all.csv
      │
      ▼ classify_favorites.py（9 大类关键词匹配）
articles_final.csv + cat_*.csv
```

### 增量分类流程（v1.2 新增）

```
# 已有分类结果
articles_final.csv
      │
      ▼ llm_incremental.py（仅处理新增收藏）
articles_final_updated.csv
      │
      ▼ merge_llm_results.py（合并多次结果）
articles_final_merged.csv
```

### Obsidian 导出流程（v1.2 新增）

```
articles_final.csv
      │
      ▼ export_to_obsidian.py --vault "D:\Obsidian\MyVault"
D:\Obsidian\MyVault\2026\06\article-title.md
```

### Notion 导出流程（v1.2 新增）

```
articles_final.csv
      │
      ▼ export_to_notion.py --database-id YOUR_DB_ID
Notion Database（含全部收藏页面）
```

---

## 自动归纳输出格式

`user_categories.json` 结构：

```json
{
  "categories": [
    {
      "name": "生物医药研发",
      "description": "创新药、临床试验、生物技术相关",
      "keywords": ["创新药", "ADC", "CAR-T", "临床", "靶点", ...]
    },
    ...
  ],
  "meta": {
    "source": "auto_discover",
    "sample_size": 500,
    "total_articles": 32333,
    "created_at": "2026-04-27 23:45"
  }
}
```

---

## 分类体系

### 方式一：自动归纳（动态）

运行 `auto_discover.py` 后，分类体系由 LLM 根据你的收藏内容归纳，类别数量、名称、关键词均动态生成。

### 方式二：默认 9 大类（固定）

| 分类 | 关键词示例 |
|------|-----------|
| 生物医药 | 创新药、ADC、CAR-T、mRNA、临床试验 |
| AI科技 | GPT、大模型、Agent、RAG、芯片 |
| 投资金融 | IPO、融资、估值、基金、VC |
| 科学研究 | Nature、Science、论文、研究 |
| 商业财经 | 企业、行业、市场、商业模式 |
| 生活方式 | 健康、运动、旅行、读书 |
| 媒体资讯 | 新闻、热点、评论、舆论 |
| 政治国际 | 国际、外交、地缘、中美 |

### 二级标签（仅默认分类）

每个一级分类下设细分标签，如：
- 生物医药：ADC、CAR-T、mRNA、创新药、临床、神经科学...
- AI科技：大模型、AI应用、AI医疗、机器人、GPU...
- 投资金融：VC/PE、二级市场、IPO、并购、估值...

完整标签列表见 `references/classification.md`。

---

## 安全说明

| 操作 | 数据流向 | 说明 |
|------|----------|------|
| **收藏导出** | 本地只读 | 完全离线 |
| **关键词分类** | 本地计算 | 完全离线 |
| **自动归纳** | 本地 → LLM API（需配置） | 发送采样标题，仅在启用时调用 |
| **LLM 分类** | 本地 → OpenRouter（需配置） | 发送标题+摘要，仅在启用时调用 |
| **IMA 导入** | 本地 → ima.qq.com（需配置） | 发送 URL 列表，仅在启用时调用 |
| **Obsidian 导出** | 本地文件写入 | 完全离线 |
| **Notion 导出** | 本地 → Notion API（需配置） | 发送收藏数据，仅在启用时调用 |

**离线模式：** 导出 + 默认分类完全离线；自动归纳需 LLM API。

**建议：** 在信任的网络环境使用自动归纳功能。

---

## 常见问题

**Q: 自动归纳出的类别不满意？**
A: 编辑 `user_categories.json` 手动调整，或重新运行 `auto_discover.py --sample 1000` 增加采样。

**Q: 可以在默认分类和自定义分类之间切换吗？**
A: 可以。不带 `--categories` 参数即为默认分类。

**Q: 自动归纳需要多少条数据？**
A: 建议 500 条以上，太少可能导致类别不全。

---

## 更新日志

### v1.2.0 — 2026-06-07

- 自动归纳分类 — 从收藏内容中 LLM 发现自然类别，不再受限于固定 9 大类
- Obsidian / Notion 导出 — Markdown 按年月归档+增量同步 / 批量导入 Notion 数据库
- LLM 增量分类 — 新增收藏无需全量重跑，支持结果合并与标签标准化
- 自定义分类 — classify_favorites.py 新增 --categories 参数，支持自定义分类 JSON

### v1.1.4 — 2026-04-26

- 安全审核修复：SAFE_MODE 离线模式，核心功能默认关闭网络
- 中英双语文档完善
- 安全说明强化：新增 ## 安全说明章节，强调本地化、隐私保护与数据安全

### v1.1 — 2026-04

- 分类体系升级：新增三级分类体系——9大主类、57个二级标签、6个跨领域标签，分类更精细多元
- 文档全面优化：完善 SKILL.md，补充分类逻辑说明、LLM 使用指南、实测数据、文件格式说明
- 快速上手简化：精简配置示例、优化命令说明、增强引导提示、补充常用触发词，方便快速上手
- LLM 智能增强（可选）：新增 LLM 辅助分类脚本（llm_classify.py、llm_incremental.py、merge_llm_results.py、normalize_categories.py），低置信度或模糊条目可交由大模型重新分类
- 安全说明强化：新增## 安全说明章节，强调本地化、隐私保护与数据安全
- 版本升级：1.1.0 → 1.1，新显示名（微信收藏知识库）

---

## License

MIT License

---

本工具仅供个人备份和学习使用。请勿用于任何商业用途或违法行为。
