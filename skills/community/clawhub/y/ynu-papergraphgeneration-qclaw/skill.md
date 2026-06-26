---
name: paper-diagram
description: >
  多模态论文可视化引擎 — 从 PDF 或纯文本论文自动生成学术插图。
  支持：全篇扫描识别可图化内容、双编码器架构图/算法流程图/动机图生成、
  自校核机制、LaTeX/Word 图注输出、Matplotlib 结果图精确绘图。
  也包含独立的 PDF → Text 提取工具。
homepage: https://github.com/yourrepo/paper-diagram-skill
metadata:
  {
    "openclaw": {
      "emoji": "📊",
      "requires": {
        "bins": ["python"],
        "env": [
          "BANANA2_API_URL",
          "BANANA2_API_KEY"
        ]
      },
      "primaryEnv": "BANANA2_API_KEY",
      "envFallbacks": {
        "BANANA2_API_KEY": ["ACEDATA_API_KEY", "PAPER_DIAGRAM_API_KEY"],
        "BANANA2_API_URL": ["PAPER_DIAGRAM_API_URL"]
      }
    }
  }
---

# paper-diagram-skill

从论文（PDF 或纯文本）自动生成学术插图的完整工具链。

## 工具概览

| 工具 | 功能 | 调用方式 |
|------|------|----------|
| **draw.py** | 论文可视化主流程 | `python draw.py [args]` |
| **pdf_to_text.py** | PDF → 纯文本提取 | `python pdf_to_text.py [args]` |

---

## 工具 1：PDF → Text 提取

将 PDF 文件转换为纯文本，供 draw.py 使用。

```bash
# 基本用法
python {baseDir}/scripts/pdf_to_text.py "/path/to/paper.pdf"

# 限制页数（取前 20 页）
python {baseDir}/scripts/pdf_to_text.py "/path/to/paper.pdf" --max-pages 20

# 输出到文件
python {baseDir}/scripts/pdf_to_text.py "/path/to/paper.pdf" -o extracted.txt
```

**支持的后端（自动选择）：** pdfminer.six → PyMuPDF → pdfplumber → PyPDF2 → pypdf

> 注意：推荐先安装 `pip install pdfminer.six`，提取质量最高。

---

## 工具 2：论文图生成

### 快速开始

```bash
# 方式 A：从 PDF 直接生成（自动提取 + 画图）
python {baseDir}/scripts/draw.py \
  --pdf-path "/path/to/paper.pdf" \
  --user-requirement "Transformer 架构图" \
  --api-url "https://api.example.com/generate" \
  --api-key "sk-your-key"

# 方式 B：扫描模式（自动识别所有可图化内容）
python {baseDir}/scripts/draw.py \
  --pdf-path "/path/to/paper.pdf" \
  --mode scan

# 方式 C：批量生成（选定的图）
python {baseDir}/scripts/draw.py \
  --pdf-path "/path/to/paper.pdf" \
  --mode scan \
  --scan-results "<base64-encoded-results>" \
  --selected-ids "1,3,5" \
  --api-url "..." --api-key "..."

# 方式 D：直接传入论文文本
python {baseDir}/scripts/draw.py \
  --paper-content "论文纯文本内容..." \
  --user-requirement "画一个算法流程图" \
  --style cvpr
```

### 核心参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--pdf-path` | PDF 文件路径（会自动提取文本） | — |
| `--paper-content` | 直接传入论文纯文本 | — |
| `--user-requirement` | 用户对图片的描述 | — |
| `--mode` | `single`(单图) 或 `scan`(全篇扫描) | `single` |
| `--api-url` | 生图 API 地址 | 环境变量 |
| `--api-key` | 生图 API 密钥 | 环境变量 |
| `--style` | 学术风格: `cvpr` `neurips` `icml` `nature` | `cvpr` |
| `--skip-check` | 跳过自校核 | False |
| `--section-ref` | 对应论文章节（如 `Section 3.1`） | — |

### 环境变量

生图 API 凭证按以下优先级自动解析，**任意一个有值即可**：

| 优先级 | API Key 变量 | API URL 变量 |
|--------|-------------|-------------|
| 1 (推荐) | `BANANA2_API_KEY` | `BANANA2_API_URL` |
| 2 | `ACEDATA_API_KEY` | `PAPER_DIAGRAM_API_URL` |
| 3 | `PAPER_DIAGRAM_API_KEY` | — |

> 未设置 URL 时默认 `https://api.acedata.cloud/nano-banana/images`

推荐在 `~/.openclaw/openclaw.json` 中配置：

```json
{
  "skills": {
    "paper-diagram": {
      "env": {
        "BANANA2_API_URL": "https://api.acedata.cloud/nano-banana/images",
        "BANANA2_API_KEY": "your-api-key-here",
        "PAPER_DIAGRAM_LLM_URL": "https://your-llm-api/v1/chat/completions",
        "PAPER_DIAGRAM_LLM_KEY": "your-llm-key-here",
        "PAPER_DIAGRAM_LLM_MODEL": "gpt-4"
      }
    }
  }
}
```

### 生成的图类型

| 类型 | 说明 | 生成方式 |
|------|------|----------|
| `teaser` | 动机/概念对比图 | Mermaid → AI 生图 |
| `architecture` | 系统架构图 | Mermaid → AI 生图 |
| `flowchart` | 算法流程图 | Mermaid → AI 生图 |
| `environment` | 实验环境图 | Mermaid → AI 生图 |
| `results` | 结果对比图 | Matplotlib 代码绘图（精确数据）|

### 学术风格预设

| 预设 | 场景 | 主色调 |
|------|------|--------|
| `cvpr` | CV/CG 会议 | 蓝色系 |
| `neurips` | ML/NLP 会议 | 紫橙系 |
| `icml` | ML 会议 | 蓝红绿系 |
| `nature` | Science/Nature 期刊 | 柔蓝柔绿 |

### 输出

- **图片文件**：保存到 `outputs/` 目录（或设置的输出目录）
- **LaTeX 图注**：可直接复制到论文
- **Word 图注**：纯文本格式
- **Mermaid 拓扑**：可导出用于其他绘图工具

### 自校核机制

生成图前会自动对比拓扑描述与原文：
- ✅ 一致 → 直接生成
- ⚠️ 小问题 → 询问用户（接受 / 重新生成 / 手动修改）
- ❌ 严重错误 → 建议重新生成

---

## 推荐工作流

```
论文 PDF
  │
  ▼
pdf_to_text.py  ──→  纯文本
  │                  │
  ▼                  ▼
draw.py (scan)   draw.py (single)
  │                  │
  ▼                  ▼
扫描报告           指定描述 → 生成单张图
  │
  ▼
用户选择 (e.g. 1,3,5)
  │
  ▼
draw.py (batch)  ──→  多张图 + LaTeX 图注
```

## 安装依赖

```bash
pip install pdfminer.six requests
```

可选（提升 PDF 提取质量）：
```bash
pip install pymupdf pdfplumber pypdf
```
