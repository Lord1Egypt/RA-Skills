---
name: screenshot-tool
version: 1.0.0
description: "网页截图 + 文档截图工具。支持网页全页截图、PPT/Word/Excel/PDF 转高清图片。保留原始样式，300 DPI 高清输出。"
read_when:
  - 需要截图网页
  - 需要将 PPT/Word/PDF 转为图片
  - 需要高清文档截图
metadata: {"clawdbot":{"emoji":"📸","requires":{"bins":["libreoffice","pdftoppm","agent-browser"]}}}
allowed-tools: Bash(screenshot-tool:*)
dependencies:
  - agent-browser: "网页截图功能必需，用于 headless 浏览器截图"
  - libreoffice: "文档转换功能必需，用于 PPT/Word/Excel 转 PDF"
  - poppler-utils: "PDF 处理必需，用于 PDF 转图片"
---

# Screenshot Tool - 网页 & 文档截图工具

支持网页截图和文档转高清图片，保留原始样式。

## 功能

| 功能 | 说明 |
|------|------|
| **网页截图** | 使用 headless 浏览器截图，支持整页、单页 |
| **文档转图** | PPT/Word/Excel/PDF 转 300 DPI 高清图片 |
| **高清输出** | 4000×2250 像素，适合打印和展示 |

## 依赖安装

### 必需依赖

| 依赖 | 用途 | 安装命令 |
|------|------|---------|
| **agent-browser** | 网页截图 | `npm install -g agent-browser && agent-browser install` |
| **LibreOffice** | 文档转 PDF | `sudo apt-get install -y libreoffice-impress libreoffice-writer libreoffice-calc` |
| **poppler-utils** | PDF 处理 | `sudo apt-get install -y poppler-utils` |
| **Python 库** | PDF 转图片 | `pip3 install pdf2image pillow` |

### 安装步骤

```bash
# 1. 安装 agent-browser（网页截图必需）
npm install -g agent-browser
agent-browser install
agent-browser install --with-deps  # 如需要系统依赖

# 2. 安装 LibreOffice（文档转换必需）
sudo apt-get install -y libreoffice-impress libreoffice-writer libreoffice-calc

# 3. 安装 poppler-utils（PDF 处理必需）
sudo apt-get install -y poppler-utils

# 4. 安装 Python 依赖
pip3 install pdf2image pillow

# 5. 安装中文字体（可选，用于中文文档）
sudo apt-get install -y fonts-wqy-zenhei fonts-wqy-microhei fonts-noto-cjk
```

### 验证安装

```bash
# 验证 agent-browser
agent-browser --version

# 验证 LibreOffice
libreoffice --version

# 验证 poppler
which pdftoppm pdfinfo
```

## 使用方法

### 1. 网页截图

```bash
# 截图单个网页
python3 skills/screenshot-tool/scripts/web_screenshot.py --url "https://example.com" --output page.png

# 截图并滚动（长页面）
python3 skills/screenshot-tool/scripts/web_screenshot.py --url "https://example.com" --full-page --output page.png
```

### 2. 文档转图片

```bash
# PPT/Word/Excel/PDF 转图片
python3 skills/screenshot-tool/scripts/doc_screenshot.py --input file.pptx --output-dir ./images

# 指定 DPI（默认 300）
python3 skills/screenshot-tool/scripts/doc_screenshot.py --input file.pdf --dpi 200 --output-dir ./images
```

### 3. 使用 agent-browser 截图

```bash
# 打开网页
agent-browser open "https://example.com" --timeout 60000

# 截图
agent-browser screenshot output.png --full

# 关闭浏览器
agent-browser close
```

## 支持的格式

### 文档格式
| 格式 | 扩展名 | 状态 |
|------|--------|------|
| PowerPoint | .pptx, .ppt | ✅ 支持 |
| Word | .docx, .doc | ✅ 支持 |
| Excel | .xlsx, .xls | ✅ 支持 |
| PDF | .pdf | ✅ 支持 |
| OpenDocument | .odp, .odt, .ods | ✅ 支持 |

### 网页截图
| 方式 | 说明 | 依赖 |
|------|------|------|
| agent-browser | 使用 headless Chrome | **agent-browser** |
| OpenClaw browser | 内置浏览器工具 | OpenClaw 内置 |

## 输出规格

| 参数 | 默认值 | 说明 |
|------|--------|------|
| DPI | 300 | 分辨率 |
| 格式 | PNG | 图片格式 |
| 尺寸 | 4000×2250 | 16:9 比例 |

## 示例

### 示例1：网页截图
```bash
# 截图京东首页
python3 skills/screenshot-tool/scripts/web_screenshot.py \
  --url "https://www.jd.com" \
  --output jd_homepage.png \
  --wait 5
```

### 示例2：PPT 转图片
```bash
# 转换整个 PPT
python3 skills/screenshot-tool/scripts/doc_screenshot.py \
  --input presentation.pptx \
  --output-dir ./slides \
  --dpi 300
```

### 示例3：PDF 转图片
```bash
# 转换 PDF 前5页
python3 skills/screenshot-tool/scripts/doc_screenshot.py \
  --input document.pdf \
  --output-dir ./pages \
  --first-page 1 \
  --last-page 5
```

## 流程说明

### 文档转图片流程
```
PPT/Word/Excel → LibreOffice → PDF → pdf2image → PNG (300 DPI)
                                         ↑
                                    依赖: poppler-utils
```

### 网页截图流程
```
URL → agent-browser (headless Chrome) → Screenshot → PNG
              ↑
        依赖: agent-browser CLI
```

## 故障排除

### LibreOffice 转换失败
```bash
# 检查 LibreOffice 安装
libreoffice --version

# 手动转换测试
libreoffice --headless --convert-to pdf file.pptx
```

### pdf2image 错误
```bash
# 检查 poppler 安装
which pdftoppm pdfinfo

# 重新安装
sudo apt-get install -y poppler-utils
```

### 中文字体显示问题
```bash
# 安装中文字体
sudo apt-get install -y fonts-wqy-zenhei fonts-wqy-microhei fonts-noto-cjk
```

## 文件结构

```
skills/screenshot-tool/
├── SKILL.md              # 本文件
├── scripts/
│   ├── web_screenshot.py    # 网页截图脚本
│   └── doc_screenshot.py    # 文档转图片脚本
└── README.md             # 详细说明
```

## License

MIT
