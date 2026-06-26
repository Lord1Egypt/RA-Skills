# WPS Office Automation Skill

本地化的办公自动化ClawHub Skill，支持文档、表格、演示、PDF的全格式智能处理。

## 功能特性

### 文档处理
- **公文生成**：自动生成符合格式规范的公文（通知、报告、会议纪要）
- **智能润色**：支持正式化、精简化、商务化多风格润色
- **合同审查**：智能识别风险条款，生成审查报告

### 表格处理
- **数据清洗**：自动识别异常值、重复项，生成清洗报告
- **智能分析**：一句话完成求和、筛选、透视分析
- **图表生成**：自动创建可视化图表，支持多种样式

### 演示处理
- **大纲生成**：根据主题自动生成PPT大纲
- **智能排版**：自动匹配商务模板，完成图文排版
- **批量生成**：从Excel数据批量生成多页PPT

### PDF处理
- **格式转换**：PDF转Word/Excel，保留格式
- **内容提取**：提取核心要点，生成摘要
- **批量处理**：合并/拆分/水印

## 安装配置

### 环境要求
- Python 3.9+

### 安装依赖

```bash
pip install -r requirements.txt
```

## 使用示例

### 1. 公文生成

```python
from main import execute

params = {
    "action": "生成通知公文",
    "action_type": "generate_document",
    "doc_type": "notice",
    "title": "关于开展年度工作总结的通知",
    "subject": "请各部门于12月31日前提交年度工作总结报告",
    "keywords": ["年度总结", "工作汇报"],
    "recipient": "各部门",
    "sender": "办公室",
    "date": "2026年3月16日"
}

result = await execute(params)
```

### 2. 文档润色

```python
params = {
    "action": "润色文档",
    "action_type": "polish_document",
    "content": "这个项目做得挺好的，大家都很努力。",
    "style": "formal"  # formal/concise/business
}

result = await execute(params)
```

### 3. 合同审查

```python
params = {
    "action": "审查合同",
    "action_type": "review_contract",
    "content": "合同内容..."
}

result = await execute(params)
```

### 4. 数据清洗

```python
params = {
    "action": "清洗数据",
    "action_type": "clean_data",
    "data": "path/to/data.xlsx",
    "remove_duplicates": True,
    "handle_missing": "mean",  # mean/median/drop
    "remove_outliers": True
}

result = await execute(params)
```

### 5. 数据分析

```python
params = {
    "action": "分析表格",
    "action_type": "analyze_data",
    "analysis_type": "sum",  # sum/average/count/max/min/filter/pivot
    "data": "path/to/data.xlsx",
    "columns": ["销售额", "利润"],
    "group_by": "地区"
}

result = await execute(params)
```

### 6. 图表生成

```python
params = {
    "action": "生成柱状图",
    "action_type": "generate_chart",
    "chart_type": "bar",  # bar/line/pie/scatter
    "data": "path/to/data.xlsx",
    "x_column": "月份",
    "y_columns": ["销售额", "成本"],
    "title": "月度销售分析"
}

result = await execute(params)
```

### 7. PPT大纲生成

```python
params = {
    "action": "生成PPT大纲",
    "action_type": "generate_ppt_outline",
    "topic": "2026年度工作计划",
    "slide_count": 12,
    "target_audience": "公司管理层",
    "key_points": ["市场拓展", "产品研发", "团队建设"]
}

result = await execute(params)
```

### 8. 创建演示文稿

```python
params = {
    "action": "创建PPT",
    "action_type": "create_presentation",
    "outline": {
        "title": "项目汇报",
        "slides": [
            {"title": "项目背景", "content": ["背景1", "背景2"]},
            {"title": "项目进展", "content": ["进展1", "进展2"]}
        ]
    },
    "style": "business"  # business/creative/minimal/tech
}

result = await execute(params)
```

### 9. PDF转换

```python
import base64

with open("document.pdf", "rb") as f:
    pdf_data = base64.b64encode(f.read()).decode('utf-8')

params = {
    "action": "PDF转Word",
    "action_type": "convert_pdf",
    "file_data": pdf_data,
    "target_format": "word",  # word/excel
    "preserve_formatting": True
}

result = await execute(params)
```

### 10. PDF内容提取

```python
params = {
    "action": "提取PDF内容",
    "action_type": "extract_pdf",
    "file_data": pdf_data,
    "extraction_type": "summary",  # text/tables/summary/key_points
    "page_range": "1-5,8,10-12"
}

result = await execute(params)
```

### 11. PDF合并

```python
files = []
for file_path in ["file1.pdf", "file2.pdf", "file3.pdf"]:
    with open(file_path, "rb") as f:
        files.append(base64.b64encode(f.read()).decode('utf-8'))

params = {
    "action": "合并PDF",
    "action_type": "merge_pdf",
    "files": files
}

result = await execute(params)
```

### 12. PDF拆分

```python
params = {
    "action": "拆分PDF",
    "action_type": "split_pdf",
    "file_data": pdf_data,
    "split_mode": "range",  # page/range
    "page_ranges": ["1-3", "4-6", "7-10"]
}

result = await execute(params)
```

## 自然语言指令

Skill支持自然语言指令，自动识别意图：

- "生成一份关于年会的通知公文"
- "润色这段文字，改成正式风格"
- "审查这份合同的风险"
- "清洗这个Excel表格的数据"
- "分析销售数据，按地区分组求和"
- "生成一个柱状图，展示月度销售额"
- "生成PPT大纲"
- "把这个PDF转成Word文档"
- "提取这份PDF的核心要点"
- "合并这三个PDF文件"

## API响应格式

所有操作返回统一的响应格式：

```json
{
  "success": true,
  "message": "操作成功",
  "data": {
  },
  "file_data": "base64编码的文件数据",
  "file_name": "生成的文件名"
}
```

## 错误处理

```json
{
  "success": false,
  "message": "错误描述",
  "data": null
}
```

## 架构设计

```
wps-office-automation/
├── __init__.py              # 包初始化
├── skill.yaml               # Skill元数据
├── requirements.txt         # 依赖声明
├── main.py                  # 主入口
├── modules/                 # 功能模块
│   ├── document.py          # 文档处理
│   ├── spreadsheet.py       # 表格处理
│   ├── presentation.py      # 演示处理
│   └── pdf.py               # PDF处理
└── examples/                # 使用示例
```

## 技术特性

### 安全性
- 本地处理，无需网络连接
- 无需外部API密钥
- 数据安全可控

### 可靠性
- 纯本地处理
- 错误处理和降级
- 详细的日志记录

### 性能
- 异步I/O操作
- 流式处理大文件
- 内存优化

### 扩展性
- 模块化设计
- 插件式架构
- 易于添加新功能

## 开发指南

### 添加新功能

1. 在 `modules/` 下创建新模块
2. 在 `main.py` 中添加处理函数
3. 在 `IntentParser` 中添加意图识别规则
4. 更新文档和示例

### 本地测试

```python
import asyncio
from main import execute

async def test():
    result = await execute({
        "action": "生成通知公文",
        "doc_type": "notice",
        "title": "测试通知",
        "subject": "测试内容"
    })
    print(result)

asyncio.run(test())
```

## 许可证

MIT License

## 联系方式

- 作者：ClawHub Developer
- 版本：1.0.0
- 更新日期：2026-03-16
