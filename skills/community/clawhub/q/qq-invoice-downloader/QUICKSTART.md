# QQ邮箱发票下载器 - 快速开始指南

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install imap-tools pandas openpyxl requests playwright win10toast
playwright install chromium
```

### 2. 运行下载

**推荐方式 - 自动模式：**
```bash
python invoice_downloader_v60.py auto
```
自动从上次同步位置下载到今天，无需手动输入日期！

**指定日期范围：**
```bash
python invoice_downloader_v60.py 260301 260308
```

### 3. 查看结果

发票保存在：`Z:\OpenClaw\InvoiceOC\`

---

## 📋 输出文件

| 文件 | 说明 |
|------|------|
| 📊 发票目录.xlsx | 完整发票清单 |
| 📝 处理摘要.txt | 处理统计 |
| 📋 智能待处理清单.txt | 需手动处理的发票（含建议） |
| 📁 attachments/ | 下载的PDF文件 |

---

## ⚡ 常见命令

```bash
# 自动模式（推荐）
python invoice_downloader_v60.py auto

# 指定日期范围
python invoice_downloader_v60.py 260301 260308

# 默认最近7天
python invoice_downloader_v60.py
```

---

## 🔧 故障排除

| 问题 | 解决方案 |
|------|----------|
| 登录失败 | 检查QQ邮箱授权码是否正确 |
| 浏览器无法打开 | 运行 `playwright install chromium` |
| Z盘不存在 | 修改脚本中的 `BASE_DIR` 路径 |

---

## 📖 详细文档

请参阅 [SKILL.md](./SKILL.md) 获取完整功能说明。
