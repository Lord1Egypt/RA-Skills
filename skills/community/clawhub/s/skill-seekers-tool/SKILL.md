# Skill Seekers

将文档网站、GitHub 仓库、PDF 等转换为 Claude AI 技能的 Python CLI 工具。

## 激活条件

当用户提到以下内容时激活：
- 安装 skill-seekers
- 转换文档为 AI 技能
- 创建 claude skill
- 从网站/仓库创建技能

## 功能

### 1. 安装 skill-seekers

```bash
pip install skill-seekers
```

或安装完整功能：
```bash
pip install skill-seekers[all-llms,video,docx,epub,chroma]
```

### 2. 创建技能

从各种源创建技能：
```bash
# 文档网站
skill-seekers create https://docs.django.com/

# GitHub 仓库
skill-seekers create facebook/react

# 本地项目
skill-seekers create ./my-project

# PDF 文档
skill-seekers create manual.pdf

# Word 文档
skill-seekers create report.docx

# Jupyter Notebook
skill-seekers create notebook.ipynb
```

### 3. 打包输出

创建技能后，打包成目标格式：
```bash
# Claude AI Skill (ZIP)
skill-seekers package output/django --target claude

# LangChain Documents
skill-seekers package output/django --target langchain

# LlamaIndex TextNodes
skill-seekers package output/django --target llama-index

# Markdown (适用于 Pinecone 等向量数据库)
skill-seekers package output/django --target markdown
```

### 4. 支持的源类型 (17+)

- 文档网站 (URL)
- GitHub 仓库
- 本地项目目录
- PDF 文档
- Word 文档 (.docx)
- EPUB 电子书
- Jupyter Notebook
- OpenAPI 规范
- PowerPoint 演示文稿
- AsciiDoc 文档
- 本地 HTML 文件
- 视频 (YouTube/本地)

### 5. 支持的输出目标

| 目标 | 说明 |
|------|------|
| claude | Claude AI Skill (ZIP + YAML) |
| gemini | Google Gemini Skill |
| openai | OpenAI / Custom GPT |
| langchain | LangChain Documents |
| llama-index | LlamaIndex TextNodes |
| haystack | Haystack Documents |
| markdown | Pinecone-ready Markdown |

## 环境要求

- Python 3.10+
- pip

## 可选依赖

根据需要安装：
```bash
# MCP 服务器支持
pip install skill-seekers[mcp]

# 视频处理
pip install skill-seekers[video]

# Word 文档支持
pip install skill-seekers[docx]

# 向量数据库支持
pip install skill-seekers[chroma,weaviate]
```

## 官方资源

- PyPI: https://pypi.org/project/skill-seekers/
- 官网: https://skillseekersweb.com/
- GitHub: https://github.com/yusufkaraaslan/Skill_Seekers