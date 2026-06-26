# 小红书内容创作助手

一键生成配图 + 自动发布草稿，小红书博主必备工具！

## ✨ v4.5 新功能

- 🌐 **全平台兼容** — Windows / macOS / Linux（OpenClaw 路径自动适配）
- 🤖 **智能路由生图** — 模型优先，豆包兜底，全自动切换
- 🤖 **豆包全自动化** — 无需任何用户引导
- 🎯 **发布确认** — 草稿保存后主动询问是否发布
- 📱 **扫码登录** — 未登录时自动点出二维码
- ✍️ **富文本粘贴** — 800字+长文本不截断

## 🚀 快速开始

### 1. 安装依赖

**无需安装任何额外依赖！** Playwright 由 OpenClaw 自带。

### 2. 配置 MiniMax（可选，不配也能用豆包）

```bash
cp scripts/config.json.example scripts/config.json
# 填入你的 MiniMax API Key
```

### 3. 生图

```bash
node scripts/generate_image_smart.js -p "描述" -n 3
```

### 4. 发布草稿

```bash
node scripts/upload_auto.js \
  --title "标题" \
  --content-file "正文.txt" \
  --images "img1.jpg,img2.jpg"
```

## 📁 目录结构

```
xhs-content-studio/
├── SKILL.md                      # 详细文档
├── README.md                     # 本文件
├── scripts/
│   ├── generate_image_smart.js   # 智能生图（主入口）
│   ├── upload_auto.js            # 发布草稿
│   ├── config.json.example       # 配置模板
│   ├── install.bat               # Windows 安装
│   └── install.sh               # macOS/Linux 安装
└── references/
    ├── hashtags.md              # 标签库
    ├── title-formulas.md        # 标题公式
    └── content-templates.md     # 内容模板
```

## 🔄 更新日志

- v4.5 (2026-03-30): 全平台兼容（macOS/Linux Playwright 路径自动适配）
- v4.4 (2026-03-30): 富文本粘贴修复（长文本不截断）
- v4.3 (2026-03-30): 豆包全自动化生图
- v4.2 (2026-03-30): 自动扫码登录
- v4.1 (2026-03-30): 智能路由生图
- v4.0 (2026-03-30): 跨平台支持 + 发布确认

---

**祝你小红书运营顺利！🎉**
