# Tech News Brief — 科技新闻简报

自动化 AI/大模型/半导体科技新闻发现、整理、生成与邮件发送工具。运行一次，完成从多维度搜索到 DOCX 交付的全流程。

## Overview

```
Phase 1          Phase 2–9
发现(多维度搜索) → 下载 → 清洗 → 摘要 → DOCX → 打包 → 发送
```

**输出文件**：`{YYYYMMDD}/` 目录下的 `.md` + `.docx` 文件，ZIP 压缩包发送至指定邮箱。

---

## Features

- **7 维度分层搜索**：中文最新 AI 动态 / 芯片半导体 / 前沿技术(量子/机器人/新能源) / AI 大模型 / 产业政策 / 中美科技博弈 / 学术开源
- **时效性优先**：仅收录 5 天内新闻
- **AI 摘要生成**：符合"xx班"规范，含价值点、五段式摘要
- **完整格式输出**：原文稿 + 摘要稿双格式，支持 `.docx`
- **邮件自动发送**：打包 ZIP 后直接发送

---

## Requirements

- Python 3.10+
- LibreOffice（用于 DOCX 生成）
- 以下环境变量（见配置节）

---

## Directory Structure

```
tech-news-brief/
├── SKILL.md                          # 核心 Skill 定义（ Agent 使用）
├── _meta.json                        # 元数据
├── scripts/
│   ├── download.py                  # Firecrawl 网页抓取（额度有限，仅 fallback）
│   ├── md2doc.py                    # MD → DOCX 转换
│   ├── smtp_send.py                 # 邮件发送（备用）
│   ├── template-original.docx    # 原文稿 DOCX 模板
│   └── template-summary.docx     # 摘要稿 DOCX 模板
└── references/
    ├── sources.md                   # 推荐新闻源列表
    └── writing-guide.md             # 摘要写作规范
```

---

## Environment Variables

| 变量名 | 用途 | 示例 |
|--------|------|------|
| `FIRECRAWL_API_KEY` | 网页抓取（fallback） | `fc-xxx` |
| `REPORTS_DIR` | 输出根目录 | `/path/to/reports` |
| `SMTP_SENDER` | 发件邮箱地址 | `xxx@qq.com` |
| `SMTP_PASSWD` | 邮箱授权码 | `xxxx` |
| `SMTP_TO` | 收件邮箱地址 | `xxx@qq.com` |

> 配置方式：将上述变量写入 `.env` 文件，或在终端 `export` 后运行脚本。

---

## Quick Start

### 1. 安装依赖

```bash
pip install python-docx lxml
```

### 2. 配置环境变量

```bash
export FIRECRAWL_API_KEY="fc-xxx"
export REPORTS_DIR="/path/to/reports"
export SMTP_SENDER="your@qq.com"
export SMTP_PASSWD="your-authorization-code"
export SMTP_TO="recipient@qq.com"
```

### 3. 运行流程

#### 方式 A：通过  Agent（推荐）

在  中以以下任一方式触发：

```
"开始今天的科技新闻整理"
"最近有什么AI新闻"
"排序1-3下载整理"
```

Agent 将自动执行 Phase 1–9，生成文件并发送邮件。

#### 方式 B：手动运行脚本

**Phase 2：下载原文**

```bash
# 路径 A：browser MCP（主路径，自动使用）
# 路径 B：Firecrawl（fallback）
python3 scripts/download.py <URL> <输出路径>
```

**Phase 7：MD 转 DOCX**

```bash
python3 scripts/md2doc.py <文件路径>
```

**Phase 8：打包并发送**

```bash
# 打包
cd $REPORTS_DIR && zip -j {YYYYMMDD}.zip {YYYYMMDD}/*.md {YYYYMMDD}/*.docx

# 发送
python3 scripts/smtp_send.py <收件人邮箱>
```

---

## Output File Naming

| 类型 | 格式 |
|------|------|
| 原文稿 | `{YYYYMMDD}xx班-科技新闻原文{序号}-sml.md` |
| 原文稿（DOCX） | `{YYYYMMDD}xx班-科技新闻原文{序号}-sml.docx` |
| 摘要稿 | `{YYYYMMDD}xx班-科技新闻摘要{序号}-sml.md` |
| 摘要稿（DOCX） | `{YYYYMMDD}xx班-科技新闻摘要{序号}-sml.docx` |

- **序号**：用户指定的排序号（1=第1条）
- **排序ID**：固定为 `sml`（xx班客户编号）

---

## News Source Priority

### 时效性优先来源

| 优先级 | 来源 | 时效性 |
|--------|------|--------|
| ⭐⭐⭐⭐⭐ 最高 | 机器之心 (jiqizhixin.com) / 量子位 (qubitchina.com) | 小时级 |
| ⭐⭐⭐⭐ 高 | 36kr / 虎嗅 / 新智元 | 小时~天级 |
| ⭐⭐⭐ 中高 | 工信部 / gov.cn 科技政策 / 新华网科技 | 天级 |

完整新闻源列表见 [`references/sources.md`](references/sources.md)。

---

## Workflow Summary

| Phase | 操作 | 说明 |
|-------|------|------|
| 1 | 多维度分层搜索 | 7 个维度，最少 8 次搜索 |
| 2 | 下载原文 | browser MCP 为主，Firecrawl 作 fallback |
| 3 | 字数门槛检查 | 不足 300 字跳过 |
| 4 | 清洗正文 | 去除页头/页脚/广告等干扰内容 |
| 5 | 写入原文稿 | 按模板格式写入 MD 文件 |
| 6 | 整理摘要 | AI 撰写中文摘要，含价值点 |
| 7 | MD 转 DOCX | 使用模板文件生成 Word 文档 |
| 8 | 打包发送 | ZIP 压缩包发送至邮箱 |

---

## Notes

- **时效性铁律**：仅收录 5 天内发布的新闻，超出范围一律不收录
- **摘要铁律 1**：主标题 ≤30 字，纯文本单行，无换行符
- **摘要铁律 2**：正文一段成文，≤400 字，无换行符
- **Firecrawl 额度有限**：非必要不使用，仅作 browser MCP 的 fallback

---

## References

- [推荐新闻源](references/sources.md)
- [摘要写作规范](references/writing-guide.md)
