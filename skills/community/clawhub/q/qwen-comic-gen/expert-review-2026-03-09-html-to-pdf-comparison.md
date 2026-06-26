# HTML 转 PDF 技能对比报告

**生成时间：** 2026-03-09 08:57

---

## 🎯 用户需求

**场景：** 手机上查看飞书消息时，无法看到电脑上的 HTML 文件，需要转成 PDF 方便查看。

**核心需求：**
- ✅ HTML → PDF 转换
- ✅ 本地处理（无需上传到外部服务）
- ✅ 保留格式（CSS/布局/颜色）
- ✅ 飞书可发送 PDF 文件

---

## 📊 找到的方案

### 方案 1：html-to-pdf（yonggao/claude-plugins）⭐⭐⭐⭐

**技能信息：**
- **来源：** yonggao/claude-plugins@html-to-pdf
- **安装数：** 4 次
- **API：** 本地 Playwright + WeasyPrint
- **费用：** 免费（本地处理）

**功能：**
- ✅ 多页 PDF（标准 A4，适合打印）
- ✅ 单页长图 PDF（无分页，适合手机查看）
- ✅ PNG 截图（可选）
- ✅ 自动安装依赖

**命令：**
```bash
# 安装技能
npx skills add yonggao/claude-plugins@html-to-pdf -g -y

# 转换为标准 PDF
python html_to_pdf_final.py input.html output.pdf

# 转换为单页长图 PDF（推荐手机查看）
python html_to_long_image.py input.html
```

**优点：**
- ✅ 本地处理，无需外部 API
- ✅ 支持多种输出格式
- ✅ 自动安装依赖
- ✅ 单页长图模式适合手机查看

**缺点：**
- ⚠️ 安装数少（4 次），较新技能
- ⚠️ 需要 Python 环境

---

### 方案 2：htmlcsstoimage（vm0-ai/vm0-skills）⭐⭐⭐

**技能信息：**
- **来源：** vm0-ai/vm0-skills@htmlcsstoimage
- **安装数：** 54 次
- **API：** HTMLCSStoImage API
- **费用：** 免费 50 张/月，之后付费

**功能：**
- ✅ HTML → PNG 图片
- ✅ 网页截图
- ✅ 自定义样式

**命令：**
```bash
# 安装技能
npx skills add vm0-ai/vm0-skills@htmlcsstoimage -g -y

# 配置 API Key
export HCTI_USER_ID="your-user-id"
export HCTI_API_KEY="your-api-key"
```

**优点：**
- ✅ 安装数中等（54 次）
- ✅ 免费额度 50 张/月
- ✅ 简单，无需安装依赖

**缺点：**
- ❌ 需要外部 API（非本地）
- ❌ 输出是图片，不是 PDF
- ❌ 需要注册账号获取 API Key
- ❌ 超出免费额度需付费

---

### 方案 3：playwright-local（jezweb/claude-skills）⭐⭐⭐⭐⭐

**技能信息：**
- **来源：** jezweb/claude-skills@playwright-local
- **安装数：** 507 次（很高！）
- **API：** 本地 Playwright
- **费用：** 免费（本地处理）

**功能：**
- ✅ 网页自动化
- ✅ 网页截图（PNG/PDF）
- ✅ 本地浏览器（Chromium/Firefox/WebKit）

**命令：**
```bash
# 安装技能
npx skills add jezweb/claude-skills@playwright-local -g -y

# 安装浏览器
npx playwright install chromium

# 截图/转 PDF（脚本示例）
const { chromium } = require('playwright');
const browser = await chromium.launch();
const page = await browser.newPage();
await page.goto('file:///path/to/file.html');
await page.pdf({ path: 'output.pdf', format: 'A4' });
await browser.close();
```

**优点：**
- ✅ 安装数高（507 次），成熟稳定
- ✅ 本地处理，无需外部 API
- ✅ 功能强大（不止转 PDF）
- ✅ 官方支持（Playwright 团队）

**缺点：**
- ⚠️ 需要 Node.js 环境
- ⚠️ 需要编写简单脚本（或让技能自动处理）
- ⚠️ 浏览器二进制较大（~400MB）

---

## 🆚 方案对比

| 维度 | html-to-pdf | htmlcsstoimage | playwright-local |
|------|-------------|----------------|------------------|
| **安装数** | 4 次 | 54 次 | 507 次 ⭐ |
| **本地处理** | ✅ 是 | ❌ 否 | ✅ 是 ⭐ |
| **输出格式** | PDF/PNG | PNG | PDF/PNG ⭐ |
| **外部 API** | ❌ 无需 | ✅ 需要 | ❌ 无需 ⭐ |
| **费用** | 免费 | 50 张/月免费 | 免费 ⭐ |
| **手机友好** | ✅ 单页长图 | ✅ 图片 | ✅ PDF ⭐ |
| **依赖** | Python | 无 | Node.js |
| **成熟度** | ⭐⭐ 新技能 | ⭐⭐⭐ 中等 | ⭐⭐⭐⭐⭐ 成熟 |

---

## 🏆 推荐方案

### 首选：playwright-local（⭐⭐⭐⭐⭐）

**理由：**
1. **安装数最高（507 次）** - 成熟稳定，经过验证
2. **本地处理** - 无需外部 API，隐私安全
3. **免费** - 无额外费用
4. **功能强大** - 不止转 PDF，还能做网页自动化
5. **官方支持** - Playwright 团队维护

**适用场景：**
- ✅ 长期需要 HTML 转 PDF
- ✅ 注重隐私（本地处理）
- ✅ 可能需要其他网页自动化功能

---

### 备选：html-to-pdf（⭐⭐⭐⭐）

**理由：**
1. **专为 HTML 转 PDF 设计** - 开箱即用
2. **单页长图模式** - 特别适合手机查看
3. **自动安装依赖** - 省心

**适用场景：**
- ✅ 只需要 HTML 转 PDF
- ✅ 想要最简单的工作流
- ✅ 有 Python 环境

---

## 📋 安装建议

### 方案 A：playwright-local（推荐）

```bash
# 1. 安装技能（2 分钟）
npx skills add jezweb/claude-skills@playwright-local -g -y

# 2. 安装浏览器（5 分钟，下载~400MB）
npx playwright install chromium

# 3. 测试转换（1 分钟）
# 说："阿福，把 expert-review-2026-03-09-qwen-wanx-comic-gen.html 转成 PDF"
```

**总计：** 8 分钟
**费用：** 免费

---

### 方案 B：html-to-pdf（备选）

```bash
# 1. 安装技能（2 分钟）
npx skills add yonggao/claude-plugins@html-to-pdf -g -y

# 2. 自动安装依赖（首次运行自动安装）
# 3. 测试转换（1 分钟）
python html_to_long_image.py expert-review-2026-03-09-qwen-wanx-comic-gen.html
```

**总计：** 5 分钟
**费用：** 免费

---

## 💡 我的建议

**推荐：playwright-local**

**理由：**
1. **成熟稳定** - 507 次安装，经过验证
2. **本地处理** - 隐私安全，无需外部 API
3. **长期价值** - 不止转 PDF，还能做网页自动化
4. **免费** - 无额外费用

**如果选择简单：** html-to-pdf（专为转 PDF 设计，单页长图模式适合手机）

---

## 🚀 下一步

**需要我帮你安装哪个？**

- ✅ playwright-local（推荐，成熟稳定）
- ✅ html-to-pdf（备选，简单易用）

**或者两个都安装，对比效果？**

---

_报告生成时间：2026-03-09 08:57_
