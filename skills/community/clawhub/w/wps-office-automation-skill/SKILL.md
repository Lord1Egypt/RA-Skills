# WPS Office Automation Skill

本地化的办公自动化ClawHub Skill，支持文档、表格、演示、PDF的全格式智能处理。

## 功能特性

### 文档处理
- 公文生成：自动生成符合格式规范的公文（通知、报告、会议纪要）
- 智能润色：支持正式化、精简化、商务化多风格润色
- 合同审查：智能识别风险条款，生成审查报告

### 表格处理
- 数据清洗：自动识别异常值、重复项，生成清洗报告
- 智能分析：一句话完成求和、筛选、透视分析
- 图表生成：自动创建可视化图表，支持多种样式

### 演示处理
- 大纲生成：根据主题自动生成PPT大纲
- 智能排版：自动匹配商务模板，完成图文排版
- 批量生成：从Excel数据批量生成多页PPT

### PDF处理
- 格式转换：PDF转Word/Excel，保留格式
- 内容提取：提取核心要点，生成摘要
- 批量处理：合并/拆分/水印

## 使用方法

### 基本调用

```python
from main import execute

result = await execute({
    "action": "生成通知公文",
    "doc_type": "notice",
    "title": "测试通知",
    "subject": "测试内容"
})
```

### 支持的操作类型

| 操作类型 | 说明 |
|---------|------|
| generate_document | 生成公文 |
| polish_document | 润色文档 |
| review_contract | 审查合同 |
| clean_data | 清洗数据 |
| analyze_data | 分析数据 |
| generate_chart | 生成图表 |
| generate_ppt_outline | 生成PPT大纲 |
| create_presentation | 创建演示文稿 |
| convert_pdf | 转换PDF |
| extract_pdf | 提取PDF内容 |
| merge_pdf | 合并PDF |
| split_pdf | 拆分PDF |

## 技术特性

- 本地处理，无需网络连接
- 无需外部API密钥
- 数据安全可控
- 异步I/O操作
- 模块化设计

## 依赖

- python-docx>=0.8.11
- openpyxl>=3.1.2
- python-pptx>=0.6.21
- PyPDF2>=3.0.1
- pdfplumber>=0.10.3
- pandas>=2.0.0
- Pillow>=10.0.0
- pydantic>=2.5.0
- reportlab>=4.0.0

## 版本

当前版本: 1.1.0

详见 [CHANGELOG.md](CHANGELOG.md)
