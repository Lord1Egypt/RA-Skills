# Form Filler - 智能申报表填写工具

## 概述

这是一个用于自动填写 Word 表格申报表的工具。它能够将申报报告的内容智能填入申请表的对应位置，同时保持原文档格式不变，新内容格式统一。

## 开发背景

在实际工作中，经常需要将申报报告的内容填写到标准格式的申请表中。这个过程：
1. 重复性高
2. 容易出错
3. 格式要求严格

本工具旨在自动化这个过程，提高效率，减少错误。

## 技术实现

### 核心技术

1. **win32com** - 操作 Word 文档
2. **表格结构识别** - 分析申请表表格结构
3. **格式控制** - 精确控制文本格式

### 关键问题及解决方案

#### 问题1：原有格式被改变

**现象**：填写内容后，原标题的格式（字体大小、下划线等）发生变化

**原因**：使用 `cell.Range.Font` 会影响整个单元格

**解决方案**：
```python
# 将标题和内容分开处理
title_range = doc.Range(cell.Range.Start, cell.Range.Start + title_len)
set_format(title_range)

content_range = doc.Range(content_start, content_end)
set_format(content_range)
```

#### 问题2：内容被表格遮挡

**现象**：填入的内容太多，表格下边框遮挡了部分文字

**原因**：表格行高固定

**解决方案**：
```python
row.HeightRule = 0  # 设置行高为自动
table.Rows.AllowBreakAcrossPages = True  # 允许跨页
```

#### 问题3：出现控制字符

**现象**：文档中出现 `_x0007_` 或其他乱码

**原因**：Word 控制字符未清理

**解决方案**：
```python
text = text.replace('\r\x07', '').replace('\x07', '')
```

#### 问题4：项目名称位置

**现象**：项目名称需要填在特定位置（如下划线后）

**解决方案**：
```python
find = doc.Content.Find
find.Text = "新技术新项目名称"
if find.Execute():
    # 移动到行末（下划线位置）
    sel.EndKey(Unit=5)  # wdLine
    sel.TypeText(project_name)
```

## 使用流程

### 步骤1：准备文件

- 申报报告（包含完整内容）
- 空表申报表（Word 格式）

### 步骤2：分析表格结构

```python
# 打开文档
doc = word.Documents.Open(form_path)
main_table = doc.Tables(2)

# 遍历表格行
for row_idx in range(1, main_table.Rows.Count + 1):
    cell = main_table.Cell(row_idx, 1)
    print(f"行{row_idx}: {cell.Range.Text}")
```

### 步骤3：配置内容映射

```python
content_map = {
    1: "第一章内容",
    2: "第二章内容",
    # ...
}
```

### 步骤4：执行填写

```python
fill_form(source_doc, form_doc, output_path, content_map)
```

## 最佳实践

### 1. 格式规范

推荐的新内容格式：
- 字体：宋体
- 字号：小四（12磅）
- 颜色：黑色
- 下划线：无
- 加粗：否

### 2. 内容控制

- 内容不要过长
- 保持段落清晰
- 适当使用换行

### 3. 质量检查

填写完成后，建议检查：
1. 格式是否统一
2. 内容是否完整
3. 表格是否正常显示

## 错误处理

### 常见错误

| 错误 | 原因 | 解决方案 |
|------|------|----------|
| 无法打开文档 | 文件路径错误 | 检查路径是否存在 |
| 表格索引错误 | 表格索引超出范围 | 检查表格数量 |
| 格式设置失败 | Range 无效 | 确保 Range 范围正确 |

## 扩展性

### 支持其他格式

可以扩展支持：
- PDF 表单填写
- Excel 表格填写
- 其他 Office 文档

### 自定义格式

可以通过参数自定义：
- 字体类型
- 字号大小
- 颜色
- 其他格式属性

## 版本历史

### v1.0.0 (2026-03-19)

- 初始版本
- 支持 Word 表格填写
- 自动格式控制
- 表格行高自动调整

## 许可证

MIT License

## 贡献

欢迎提交 Issue 和 Pull Request！