# 智能简历解析系统 Skill

这是一个OpenClaw平台的智能简历解析Skill，完全本地运行，无需外部API。

## 功能特性
- 📄 支持PDF/Word/图片格式简历解析
- 🔍 自动提取结构化简历信息（个人信息、教育经历、工作经历、项目经历、技能栈等）
- 🎯 岗位JD匹配度分析，多维度打分
- 💡 智能生成简历优化建议
- 📤 支持JSON/Markdown格式导出

## 快速开始
### 1. 安装依赖
```bash
pip install PyPDF2 python-docx pytesseract pillow
```
*注意：OCR功能需要安装Tesseract OCR引擎*

### 2. 解析简历
```bash
# 1. 提取PDF文本
python scripts/extract_pdf.py resume.pdf > resume_text.txt

# 2. 结构化解析
# 将resume_text.txt的内容传入大模型，使用SKILL.md中的提示词获取结构化JSON
```

### 3. 匹配岗位JD
```bash
# 1. 准备JD文本文件 jd.txt
# 2. 使用匹配脚本生成提示词，传入大模型获取匹配度分析
python scripts/match_jd.py resume_structured.json jd.txt
```

## 使用示例
### 解析简历
输入：`解析这个简历 resume.pdf`
输出：结构化的简历JSON + 简历摘要

### 匹配岗位
输入：`这个简历匹配后端开发岗位的JD怎么样？jd.txt`
输出：匹配度评分 + 优势/劣势分析 + 优化建议

## 技术栈
- 文本提取：PyPDF2（PDF）、python-docx（Word）、Tesseract OCR（图片）
- 大模型：本地部署的任意大模型（豆包/Claude/Ollama等）
- 数据格式：JSON标准化输出

## 项目亮点（可写简历）
1. **全本地运行**：无需调用外部API，数据隐私安全
2. **多格式支持**：覆盖主流简历格式，OCR支持图片简历
3. **结构化输出**：标准化JSON格式，方便后续处理
4. **智能匹配**：多维度匹配度分析，提供可落地的优化建议
5. **插件化设计**：作为OpenClaw Skill可一键安装，开箱即用
