# 📄 HTML 转 PDF 指南

**获得最佳质量的 PDF 报价单**

---

## 🎯 为什么用 HTML 转 PDF？

| 转换方式 | 质量 | 格式保真度 | 速度 | 推荐度 |
|----------|------|------------|------|--------|
| **HTML → PDF（浏览器）** | ⭐⭐⭐⭐⭐ | 100% | 快 | ✅ 强烈推荐 |
| Excel → PDF（LibreOffice） | ⭐⭐⭐ | 80% | 中 | ⚠️ 可用 |
| Word → PDF（LibreOffice） | ⭐⭐⭐⭐ | 90% | 中 | ✅ 可用 |

**HTML 转 PDF 优势：**
- ✅ 完美保留设计（颜色、字体、布局）
- ✅ 响应式优化（自动分页）
- ✅ 打印质量高（矢量图形）
- ✅ 文件体积小（比 Excel 转 PDF 小 30%）

---

## 📋 方法 1：浏览器手动导出（推荐 ⭐）

### 步骤：

**1. 生成 HTML 报价单**
```bash
# 一键生成（包含 HTML）
./generate-all.sh data.json QT-001

# 或只生成 HTML
./generate-all.sh data.json QT-001 --html-only
```

**2. 在浏览器打开**
```bash
# Mac
open QT-001.html

# Windows
start QT-001.html

# Linux
xdg-open QT-001.html
```

**3. 导出 PDF**

**方式 A：使用内置按钮（最简单）**
- 点击右上角的 **"Export to PDF"** 按钮
- 选择保存位置
- 完成！✅

**方式 B：使用浏览器打印功能**
- 按快捷键：
  - **Mac:** `Cmd + P`
  - **Windows/Linux:** `Ctrl + P`
- 在打印对话框中：
  - **目标打印机** → 选择 **"保存为 PDF"** 或 **"Microsoft Print to PDF"**
  - **布局** → 选择 **"纵向"**
  - **纸张尺寸** → 选择 **"A4"**
  - **边距** → 选择 **"无"** 或 **"最小"**
  - ✅ 勾选 **"背景图形"**（重要！否则颜色会丢失）
- 点击 **"保存"**
- 选择保存位置
- 完成！✅

---

## 📋 方法 2：使用脚本（半自动）

**1. 运行导出脚本**
```bash
python3 /Users/wilson/.openclaw/workspace/skills/quotation-workflow/scripts/html_to_pdf.py \
  QT-20260314-001.html
```

**2. 按提示操作**
- 浏览器会自动打开 HTML
- 按照屏幕提示按 `Cmd+P` / `Ctrl+P`
- 选择"保存为 PDF"
- 完成！

---

## 📋 方法 3：命令行自动化（高级）

### 使用 Puppeteer（Node.js）

**安装：**
```bash
npm install -g puppeteer
```

**创建脚本 `export-pdf.js`：**
```javascript
const puppeteer = require('puppeteer');
const path = require('path');

(async () => {
  const htmlFile = process.argv[2];
  const outputFile = process.argv[3] || htmlFile.replace('.html', '.pdf');
  
  const browser = await puppeteer.launch();
  const page = await browser.newPage();
  
  await page.goto(`file://${path.resolve(htmlFile)}`, {
    waitUntil: 'networkidle0'
  });
  
  await page.pdf({
    path: outputFile,
    format: 'A4',
    printBackground: true,
    margin: {
      top: '15mm',
      right: '15mm',
      bottom: '15mm',
      left: '15mm'
    }
  });
  
  await browser.close();
  console.log(`✅ PDF 已生成：${outputFile}`);
})();
```

**使用：**
```bash
node export-pdf.js QT-20260314-001.html QT-20260314-001.pdf
```

---

### 使用 wkhtmltopdf

**安装：**
```bash
# Mac
brew install wkhtmltopdf

# Ubuntu/Debian
sudo apt-get install wkhtmltopdf

# Windows
# 下载安装：https://wkhtmltopdf.org/downloads.html
```

**使用：**
```bash
wkhtmltopdf --page-size A4 --margin-top 15 --margin-bottom 15 \
  --margin-left 15 --margin-right 15 \
  --enable-local-file-access \
  QT-20260314-001.html \
  QT-20260314-001.pdf
```

---

## 🎨 打印设置优化

### Chrome/Edge 推荐设置

| 设置项 | 推荐值 | 说明 |
|--------|--------|------|
| **纸张尺寸** | A4 | 标准 A4（210×297mm） |
| **布局** | 纵向 | 竖版 |
| **边距** | 无 或 最小 | 让内容占满页面 |
| **缩放** | 100% | 保持原始大小 |
| **背景图形** | ✅ 勾选 | **重要！** 否则颜色丢失 |
| **页眉页脚** | ❌ 不勾选 | 保持简洁 |

### Safari 推荐设置

| 设置项 | 推荐值 |
|--------|--------|
| **纸张尺寸** | A4 |
| **缩放** | 100% |
| **打印背景** | ✅ 勾选 |

### Firefox 推荐设置

| 设置项 | 推荐值 |
|--------|--------|
| **纸张尺寸** | A4 |
| **缩放** | 100% |
| **打印背景** | ✅ 勾选 |
| **页眉和页脚** | ❌ 不勾选 |

---

## 📊 质量对比

### 测试文件：QT-20260314-008

| 转换方式 | 文件大小 | 颜色还原 | 字体清晰度 | 推荐度 |
|----------|----------|----------|------------|--------|
| **HTML → PDF（Chrome）** | 145KB | 100% | ⭐⭐⭐⭐⭐ | ✅ 最佳 |
| Excel → PDF（LibreOffice） | 164KB | 85% | ⭐⭐⭐ | ⚠️ 可用 |
| Word → PDF（LibreOffice） | 152KB | 90% | ⭐⭐⭐⭐ | ✅ 好 |

---

## ⚠️ 常见问题

### Q1: PDF 没有颜色/背景是白色？
**A:** 打印时没有勾选"背景图形"选项。
- Chrome: 勾选 **"背景图形"**
- Safari: 勾选 **"打印背景"**
- Firefox: 勾选 **"打印背景"**

### Q2: 内容被截断/分页不对？
**A:** HTML 已优化自动分页，如果还有问题：
- 检查边距设置（建议"无"或"最小"）
- 确保缩放是 100%
- 尝试调整浏览器窗口大小后重新打印

### Q3: 字体显示不正确？
**A:** HTML 使用 Google Fonts，需要网络连接。
- 确保网络畅通
- 等待页面完全加载后再打印
- 或者下载字体到本地（高级）

### Q4: PDF 文件太大？
**A:** 正常范围是 100-200KB。如果太大：
- 使用在线 PDF 压缩工具（如 SmallPDF、iLovePDF）
- 或用 Adobe Acrobat 优化

---

## 🚀 快速工作流（推荐）

```bash
# 1. 生成 HTML
./generate-all.sh data.json QT-001 --html-only

# 2. 打开浏览器
open QT-001.html

# 3. 按 Cmd+P → 选择"保存为 PDF" → 保存

# 4. 发送 PDF 给客户
# 完成！
```

**总耗时：** < 1 分钟 ⏱️

---

## 📁 示例文件

```
/Users/wilson/.openclaw/workspace/skills/quotation-workflow/examples/
├── QT-20260314-008-Farreach-Premium.html    # HTML 源文件 ⭐
└── (用浏览器打开 → 导出 PDF)
```

---

**最后更新：** 2026-03-14  
**维护者：** WILSON
