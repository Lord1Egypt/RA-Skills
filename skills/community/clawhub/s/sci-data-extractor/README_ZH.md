# Sci-Data-Extractor

> **科学文献数据提取工具** - 从科学论文 PDF 中智能提取结构化数据

[![License: CC BY 4.0](https://img.shields.io/badge/License-CC%20BY%204.0-lightgrey.svg)](https://creativecommons.org/licenses/by/4.0/)
[![Python 3.11+](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)

## 项目简介

**Sci-Data-Extractor** 是一个 Claude Code Skill，旨在帮助科研工作者从科学文献 PDF 中自动提取结构化数据。无论是表格、图表还是文本中的数据，都可以通过 AI 智能识别并转换为可用的格式（CSV、Markdown 表格等）。

### 核心特性

- **🔍 多种 OCR 方式**：支持 Mathpix OCR（高精度）和 PyMuPDF（免费）
- **🤖 AI 智能提取**：使用 Claude Sonnet 4.5 / GPT-4o 提取数据
- **📊 灵活输出**：支持 Markdown 表格和 CSV 格式
- **🎯 预设模板**：内置酶动力学、实验结果、文献综述等模板
- **🔄 批量处理**：支持批量提取多个文献文件
- **⚙️ 高度可配置**：支持自定义提取字段和规则

## 安装

### 方法一：通过 npx 一键安装（推荐）

```bash
npx skills add https://github.com/JackKuo666/sci-data-extractor.git
```

### 方法二：通过 Git 克隆

```bash
# 克隆到 Claude Code 的 skills 目录
git clone https://github.com/JackKuo666/sci-data-extractor.git ~/.claude/skills/sci-data-extractor
```

### 方法三：手动安装

1. 下载本项目的 ZIP 文件或克隆到本地
2. 将 `sci-data-extractor` 文件夹复制到 Claude Code 的 skills 目录：
   - **macOS/Linux**: `~/.claude/skills/`
   - **Windows**: `%USERPROFILE%\.claude\skills\`
3. 确保文件夹结构如下：

```
~/.claude/skills/sci-data-extractor/
├── SKILL.md       # 技能定义文件
├── extractor.py   # 核心提取脚本
├── README.md      # 说明文档
└── requirements.txt # 依赖列表
```

### 安装 Python 依赖

**方式一：使用 uv（推荐，最快）**

```bash
# 安装 uv（如果还没安装）
curl -LsSf https://astral.sh/uv/install.sh | sh

# 在项目目录创建虚拟环境并安装依赖
cd ~/.claude/skills/sci-data-extractor
uv venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
uv pip install -r requirements.txt
```

**方式二：使用 conda（适合已有 conda 的科研用户）**

```bash
cd ~/.claude/skills/sci-data-extractor
conda create -n sci-data-extractor python=3.11 -y
conda activate sci-data-extractor
pip install -r requirements.txt
```

**方式三：使用 venv（Python 内置，无需额外安装）**

```bash
cd ~/.claude/skills/sci-data-extractor
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# 或 .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### 验证安装

重启 Claude Code 或重新加载 skills 后，在对话中输入：

```
/extract-data
```

如果安装成功，该技能将被激活。

## 配置

### 环境变量

创建 `.env` 文件或设置以下环境变量：

```bash
# 必需：LLM API 配置
export EXTRACTOR_API_KEY="your-api-key-here"
export EXTRACTOR_BASE_URL="https://api.anthropic.com"  # 或其他兼容端点

# 可选：Mathpix OCR 配置（用于高质量 OCR）
export MATHPIX_APP_ID="your-mathpix-app-id"
export MATHPIX_APP_KEY="your-mathpix-app-key"

# 可选：默认参数
export EXTRACTOR_MODEL="claude-sonnet-4-5-20250929"
export EXTRACTOR_TEMPERATURE="0.1"
export EXTRACTOR_MAX_TOKENS="16384"
```

### 获取 API 密钥

- **Anthropic Claude**: https://console.anthropic.com/
- **OpenAI**: https://platform.openai.com/api-keys
- **Mathpix OCR**: https://api.mathpix.com/

## 使用方法

### 在 Claude Code 中使用

#### 1. 快速提取（使用预设模板）

```
/extract-data 从 paper.pdf 中提取酶动力学数据
```

#### 2. 自定义提取

```
/extract-data 从 article.pdf 中提取所有表格的临床试验数据
```

#### 3. 批量处理

```
/batch-extract 处理 ./literature 文件夹中的所有 PDF
```

#### 4. 图表数据提取

```
/extract-data 从 figure3.png 中提取曲线数据点
```

### 命令行直接使用

#### 基础用法

```bash
# 使用 PyMuPDF（免费）提取
python extractor.py input.pdf -o output.md

# 使用 Mathpix OCR（高精度）
python extractor.py input.pdf -o output.md --ocr mathpix
```

#### 使用预设模板

```bash
# 酶动力学数据
python extractor.py paper.pdf --template enzyme -o results.md

# 实验结果数据
python extractor.py paper.pdf --template experiment -o results.md

# 文献综述数据
python extractor.py paper.pdf --template review -o results.md
```

#### 自定义提取提示

```bash
python extractor.py paper.pdf \
  -p "提取所有与蛋白质结构相关的数据，包括分辨率、R值、R_free值等" \
  -o results.md
```

#### 输出 CSV 格式

```bash
python extractor.py paper.pdf --template enzyme -o results.csv --format csv
```

#### 打印结果到终端

```bash
python extractor.py paper.pdf --template enzyme -o results.md --print
```

## 预设模板说明

### 模板 1: 酶动力学数据 (`enzyme`)

提取字段：
- Enzyme（酶名称）
- Organism（来源生物）
- Substrate（底物）
- Km / Unit_Km（米氏常数）
- Kcat / Unit_Kcat（催化常数）
- Kcat_Km / Unit_Kcat_Km（催化效率）
- Temperature（温度）
- pH（酸碱度）
- Mutant（突变体）
- Cosubstrate（辅底物）

### 模板 2: 实验结果数据 (`experiment`)

提取字段：
- Experiment（实验名称）
- Condition（实验条件）
- Result（结果值）
- Unit（单位）
- Standard_Deviation（标准差）
- Sample_Size（样本量）
- p_value（显著性）

### 模板 3: 文献综述数据 (`review`)

提取字段：
- Author（作者）
- Year（年份）
- Journal（期刊）
- Title（标题）
- DOI（数字对象标识符）
- Key_Findings（主要发现）
- Methodology（研究方法）

## 使用场景

### 场景 1: 构建酶动力学数据库

```bash
# 批量提取多篇文献的酶动力学数据
for file in literature/*.pdf; do
    python extractor.py "$file" --template enzyme -o "results/$(basename "$file" .pdf).csv" --format csv
done
```

### 场景 2: 提取临床实验数据

```bash
python extractor.py clinical_trial.pdf \
  -p "提取所有临床试验的患者数量、治疗方案、有效率和副作用数据" \
  -o clinical_data.csv --format csv
```

### 场景 3: 整理文献综述

```bash
python extractor.py review_paper.pdf --template review -o references.md
```

### 场景 4: 提取材料性质数据

```bash
python extractor.py materials.pdf \
  -p "提取所有材料的机械性能数据，包括强度、模量、断裂伸长率等" \
  -o materials.csv --format csv
```

## 输出格式

### Markdown 表格

```markdown
| Enzyme | Organism | Substrate | Km | Unit_Km | Kcat | Unit_Kcat |
|--------|----------|-----------|-----|---------|------|-----------|
| HEX1 | Saccharomyces cerevisiae | Glucose | 0.12 | mM | 1840 | s^-1 |
```

### CSV 格式

```csv
Enzyme,Organism,Substrate,Km,Unit_Km,Kcat,Unit_Kcat
HEX1,Saccharomyces cerevisiae,Glucose,0.12,mM,1840,s^-1
```

## 项目结构

```
sci-data-extractor/
├── SKILL.md              # Claude Code 技能定义
├── extractor.py          # 核心提取脚本
├── README.md             # 项目说明文档
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量示例
└── examples/             # 使用示例
    ├── enzyme_paper.pdf  # 示例 PDF
    └── custom_prompt.txt # 自定义提示示例
```

## 技术架构

```
┌─────────────────┐
│   PDF 输入文件   │
└────────┬────────┘
         │
         ▼
┌─────────────────────────┐
│   OCR 处理层            │
│  • Mathpix OCR (可选)   │
│  • PyMuPDF (默认)       │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   文本预处理            │
│  • 删除参考文献         │
│  • 清理格式             │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   AI 提取层             │
│  • Claude Sonnet 4.5    │
│  • GPT-4o               │
└────────┬────────────────┘
         │
         ▼
┌─────────────────────────┐
│   输出格式化            │
│  • Markdown 表格        │
│  • CSV                  │
└────────┬────────────────┘
         │
         ▼
┌─────────────────┐
│   结构化数据输出 │
└─────────────────┘
```

## 依赖项

- **Python 3.11+**
- **PyMuPDF**: PDF 文本提取
- **OpenAI**: LLM API 调用（兼容 Claude）
- **Requests** (可选): Mathpix OCR 调用

## 常见问题

### Q: Mathpix OCR 和 PyMuPDF 有什么区别？

**A:**
- **Mathpix OCR**: 高精度，能识别公式和复杂表格，但需要 API 付费
- **PyMuPDF**: 完全免费，适合纯文本内容，公式识别效果较差

### Q: 如何处理超过 token 限制的长文档？

**A:** 工具会自动分段处理，将长文档分成多个部分，最后合并结果。对于大型表格或大量数据提取，可以通过增加 `EXTRACTOR_MAX_TOKENS` 环境变量来提高输出上限（默认值：16384，可设置为 32768 或更高）。

### Q: 提取的数据准确吗？

**A:** AI 提取的准确率取决于文档的清晰度和数据结构。建议：
1. 对提取结果进行人工验证
2. 对于重要数据，使用 Mathpix OCR 提高精度
3. 可以通过调整 prompt 优化提取效果

### Q: 可以提取图片中的图表数据吗？

**A:** 可以！Claude Code 支持图片分析功能，可以识别图表并提取数据点。

### Q: 如何自定义提取字段？

**A:** 使用 `-p` 参数提供自定义提示，例如：

```bash
python extractor.py paper.pdf \
  -p "提取表格1中的所有数据，包括样品名称、浓度、吸光度、荧光强度" \
  -o results.md
```

## 贡献指南

欢迎贡献代码、报告问题或提出新功能建议！

1. Fork 本项目
2. 创建特性分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 引用

如果本项目对你的研究有帮助，请引用：

```bibtex
@software{sci_data_extractor,
  title={Sci-Data-Extractor: AI-Powered Scientific Literature Data Extraction},
  author={JackKuo},
  year={2025},
  url={https://github.com/JackKuo666/sci-data-extractor}
}
```

## 许可证

本项目采用 **Creative Commons Attribution 4.0 International (CC BY 4.0)** 许可证。

## 相关资源

- [原项目: Automated Enzyme Kinetics Extractor](https://huggingface.co/spaces/jackkuo/Automated-Enzyme-Kinetics-Extractor)
- [相关论文: Enzyme Co-Scientist](https://www.biorxiv.org/content/10.1101/2025.03.02.153459v1)
- [Claude Code Skills 文档](https://docs.anthropic.com/en/docs/claude-code/skills)

## 联系方式

- GitHub: [JackKuo666/sci-data-extractor](https://github.com/JackKuo666/sci-data-extractor)
- GitHub Issues: [提交问题](https://github.com/JackKuo666/sci-data-extractor/issues)

---

**注意**: 本工具仅供学术研究使用，使用提取的数据时请遵守版权法规并引用原始文献。
