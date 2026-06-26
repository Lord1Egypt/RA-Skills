---
name: manual-translator
description: 将docx说明书翻译成指定语言，并重新截取应用界面截图替换文档中的原图。触发场景：(1) 用户发送docx文档要求翻译，(2) 需要重新截取软件界面截图，(3) 包含截图替换的文档本地化工作
---
# Manual Translator

## Overview

将 docx 格式的说明书翻译成指定语言，并重新截取应用程序界面截图替换文档中的原图。支持 Web 应用、本地 EXE、项目启动等多种应用类型。

## 优化版翻译流程

### Step 1: 收集信息

用户需要提供：

- **docx 文件路径**: 要翻译的说明书文档
- **目标语言**: 如英文(EN)、日文(JA)、韩文(KO)等
- **DeepLX API Key** (可选): 用于翻译

### Step 2: 分段翻译 (推荐)

为避免 API 限流或超时，建议使用分段翻译：

```python
# 分批翻译，每批50项
batch_size = 50
for i in range(0, total, batch_size):
    batch = texts[i:i+batch_size]
    for text in batch:
        # 翻译...
    # 每批保存中间结果
    doc.save(f"output_part{batch+1}.docx")
```

### Step 3: 表格翻译

Docx 文档中的表格需要单独处理：

```python
# 遍历所有表格
for table in doc.tables:
    for row in table.rows:
        for cell in row.cells:
            text = cell.text.strip()
            if text and has_chinese(text):  # 检测是否包含中文
                cell.text = translate(text)
    # 每表格保存，防止中途失败
    doc.save(output_file)
```

### Step 4: 合并与输出

1. 合并所有分节翻译结果
2. 替换原文档中的中文内容
3. 保留文档格式、图片、表格结构

## DeepL API 使用

API 格式：

```
POST https://api.deeplx.org/{API_KEY}/translate
Body: {"text": "原文", "target_lang": "目标语言代码"}
```

目标语言代码：EN, JA, KO, ZH, FR, DE, ES, IT, PT, RU 等

**备用方案**: 如果 API 不可用，使用模型自身能力翻译

## 启动应用 (如需截图)

**Web 应用**:

- 直接访问 URL
- 寻找语言切换设置

**项目路径**:

- 前端: `pnpm dev`
- 后端: `pnpm start` 或 `npm run start:dev`

## 关键提示

- **分段翻译**: 每50项一批，每批保存，防止中途失败
- **表格翻译**: 逐表格翻译并保存
- **错误处理**: 使用 try-except 捕获异常，继续处理下一项
- **保留格式**: 只替换文本内容，保留段落格式、表格结构、图片
