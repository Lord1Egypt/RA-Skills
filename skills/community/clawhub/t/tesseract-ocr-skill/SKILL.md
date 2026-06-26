---
name: tesseract-ocr-skill
description: 基于Tesseract引擎的OCR文字识别技能，支持中文、英文、中英混合三种模式，输出text/structured/question_answer三种格式。
---

# Tesseract OCR Skill

使用 Tesseract 引擎从图像中提取文字内容。

## 功能

- 支持中文（简体）、英文、中英混合三种语言模式
- 支持三种输出格式：
  - `text`: 纯文本输出
  - `structured`: 结构化输出（识别题目、选项、答案）
  - `question_answer`: 问答对格式

## 使用方式

```bash
python <skill-path>/tesseract_ocr_skill.py <image_path> --lang chi_sim+eng --format text
```

## 参数

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `image_path` | 图片文件路径 | 必填 |
| `--lang` | 识别语言 | `chi_sim+eng` |
| `--format` | 输出格式 | `text` |
| `--output` | 输出文件路径 | 控制台输出 |

## 依赖

- Python 3.x
- pytesseract
- Pillow
- Tesseract OCR 引擎（需单独安装）

## 安装 Tesseract

Windows: 下载安装包 https://github.com/UB-Mannheim/tesseract/wiki
