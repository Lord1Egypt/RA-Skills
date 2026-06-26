---
name: watermark-remover
description: 去除 PDF 文件中的水印。使用场景：用户请求去除 PDF 文件的水印时触发。支持单个或多个文件批量处理。严格遵循确认流程：环境检查→库安装确认→水印检测→去除确认。
---

# Watermark Remover - PDF 水印去除技能

## 工作流程

### 1. 触发条件

当用户请求去除文件水印时触发，例如：
- "帮我去除这个 PDF 的水印"
- "把这个文件的水印去掉"
- "去除这些文件的水印"

### 2. 环境检查流程

**第一步：检查 Python 环境**
```bash
python --version
```

- 如果 Python 未安装 → **必须获得用户确认**后才能安装
- 如果已安装 → 继续下一步

**第二步：检查所需 Python 库**

需要检查以下库：
- `pypdf` - PDF 处理
- `PyMuPDF` (fitz) - PDF 分析和验证

检查命令：
```bash
python scripts/check_env.py check_all
```

- 如果库未安装 → **必须获得用户确认**后才能安装
- 如果已安装 → 继续下一步

### 3. 水印检测

使用 Python 脚本检测文件中的水印：
```bash
python scripts/detect_watermark.py <文件路径>
```

检测内容包括：
- 水印类型（Pattern/图像/文本）
- 水印位置
- 保存水印预览图到指定位置

**必须向用户展示检测结果并确认**是否开始去除水印。

### 4. 去除水印

获得用户确认后执行：
```bash
python scripts/remove_watermark.py <文件路径> [--output <输出路径>]
```

**输出规则：**
- 如果用户指定输出路径 → 保存到指定位置
- 如果用户未指定 → 保存到原文件同级目录
- 命名格式：`<原文件名>_no_watermark.<扩展名>`

### 5. 验证结果

去除完成后自动验证：
- 检查输出文件是否存在
- 检查水印是否已移除
- 向用户展示验证结果

## 脚本说明

### scripts/check_env.py
检查 Python 环境和所需库的安装状态。

### scripts/detect_watermark.py
检测 PDF 文件中的水印，生成预览图。

### scripts/remove_watermark.py
执行水印去除操作。

## 安全确认原则

⚠️ **以下操作必须获得用户明确确认后才能执行：**

1. 安装 Python
2. 安装 Python 库（pip install）
3. 删除或修改任何文件
4. 修改系统配置文件
5. 开始执行水印去除操作

## 示例对话

**用户**: 帮我去除这个 PDF 的水印

**助手**: 
1. 检测到您需要去除水印，让我先检查环境...
2. ✓ Python 已安装 (3.x.x)
3. ⚠ 缺少库 pypdf，需要安装吗？(y/n)
4. [用户确认后安装]
5. ✓ 环境准备完成
6. 检测到水印：CodeCV 简历（Pattern 类型）
7. 预览图已保存：xxx_watermark_preview.png
8. 确认开始去除水印吗？(y/n)
9. [用户确认后执行]
10. ✓ 水印已去除，文件保存至：xxx_no_watermark.pdf
