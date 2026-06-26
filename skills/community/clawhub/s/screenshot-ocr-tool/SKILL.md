# Screenshot OCR Tool - 屏幕截图OCR工具

## 概述
专门用于处理屏幕截图的OCR工具，特别适合中医考试题识别。

## 技能列表

### 1. Screenshot OCR Extraction
从屏幕截图中提取文字内容，特别适合处理考试题。

**参数：**
- `image_path` (string, 必需): 截图文件路径
- `output_format` (string, 可选): 输出格式
  - `text`: 纯文本
  - `structured`: 结构化
  - `question_answer`: 问答分离

**实现：** Python 脚本 `./scripts/screenshot_ocr.py`

## 使用示例
```
输入：考试题目截图
输出：提取后的文字内容
```
