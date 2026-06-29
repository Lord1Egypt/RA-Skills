# WPS Office 全家桶

基于自然语言的 WPS Office 自动化 Skill，支持 Word/Excel/PPT 创建、编辑、格式转换。

## 功能

- 📄 **WPS 文字** - 创建/编辑/格式/导出
- 📊 **WPS 表格** - 数据/公式/图表/筛选
- 🎬 **WPS 演示** - 创建/幻灯片/主题/导出
- 🔄 **格式转换** - Word/Excel/PPT/PDF 互转
- 📁 **文档管理** - 打开/保存/最近文档

## 使用方式

```bash
python scripts/wps_word.py create --title "我的文档"
python scripts/wps_excel.py create --name "预算表"
python scripts/wps_ppt.py create --title "汇报"
python scripts/format_converter.py convert --input "D:\文档\报告.docx" --output-format pdf
```

## 依赖

```bash
pip install -r requirements.txt
```

## 风险提示

1. **文件安全**：操作前建议备份重要文件
2. **格式兼容性**：部分复杂格式转换可能丢失原始排版
3. **依赖要求**：需安装 WPS Office 2019+ 或 WPS 365
