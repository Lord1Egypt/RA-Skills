---
name: html-image-generator
description: 免费图片生成器 — 用HTML模板+Playwright渲染，输入任意主题即可生成图片。完全免费，无需API Key，支持14种风格+5种尺寸。适用于封面、配图、海报、素材、社交媒体等场景。
version: 2.0.0
author: 旺财 x 大作家
category: image
tags: [image-generator, html, playwright, free, cover, poster, social-media]
license: MIT
---

# 免费图片生成器 v2.0

> **完全免费 | 无需API | 本地生成 | 无限使用**

输入任意主题，选择风格和尺寸，即可生成精美的PNG图片。

---

## 核心原理

```
输入主题 → HTML模板 → Playwright渲染 → PNG图片
```

- 不依赖任何付费API
- 不花一分钱
- 纯本地生成
- 想生成多少生成多少

---

## 快速开始

### 最简单用法

```
生成一张图片，主题：属虎人2026年转运指南
```

### 指定风格

```
生成一张图片
主题：早安｜新的一天
风格：warm
```

### 指定尺寸

```
生成一张图片
主题：周末读书会
风格：poster
尺寸：9x16
```

---

## 风格选择（14种）

| 风格 | 特点 | 适合场景 |
|------|------|----------|
| warm | 暖色渐变、柔和 | 祝福、情感、玄学 |
| fresh | 绿蓝清新、自然 | 生活、旅游、美食 |
| bold | 深色背景、高对比 | 干货、知识、标题 |
| minimal | 简约白底、极简 | 文艺、极简风格 |
| vintage | 复古棕褐、怀旧 | 古风、怀旧话题 |
| cute | 粉嫩可爱、萌系 | 星座、萌宠 |
| notion | 知识风格、干净 | 教程、知识管理 |
| dark | 暗黑酷炫、神秘 | 科技、潮流 |
| poster | 电影海报风 | 活动、人物、事件 |
| watercolor | 水彩晕染、艺术 | 艺术、诗意 |
| gradient | 极光渐变、绚丽 | 科技、自然 |
| neon | 霓虹灯、赛博朋克 | 夜店、派对 |
| paper | 纸张纹理、手账 | 日记、手账 |
| marble | 大理石纹、高端 | 优雅、品质 |

---

## 尺寸规格（5种）

| 尺寸 | 比例 | 像素 | 适合平台 |
|------|------|------|----------|
| 1x1 | 1:1 | 1080×1080 | 朋友圈、微博、Instagram |
| 4x5 | 4:5 | 1080×1350 | 朋友圈竖版、小红书 |
| 9x16 | 9:16 | 1080×1920 | 短视频封面、抖音 |
| 16x9 | 16:9 | 1920×1080 | 横版视频、YouTube |
| 4x3 | 4:3 | 1600×1200 | 通用横版 |

---

## 示例场景

### 1. 运势玄学类

```
主题：属虎人2026年转运指南
风格：warm
尺寸：4x5
```

### 2. 知识干货类

```
主题：5个改变命运的小习惯
风格：bold
尺寸：1x1
```

### 3. 早安问候类

```
主题：早安｜新的一天，新的开始
风格：fresh
尺寸：1x1
```

### 4. 活动海报类

```
主题：周末读书会｜一起阅读
风格：poster
尺寸：9x16
```

### 5. 星座运势类

```
主题：本周星座运势排行榜
风格：cute
尺寸：4x5
```

### 6. 科技潮流类

```
主题：AI人工智能的未来
风格：neon
尺寸：16x9
```

### 7. 艺术诗意类

```
主题：春风又绿江南岸
风格：watercolor
尺寸：4x5
```

### 8. 优雅高端类

```
主题：2026年度盛典
风格：marble
尺寸：poster
尺寸：16x9
```

---

## 技术实现

### 模板路径

```
C:\Users\Administrator\.openclaw\scripts\templates\general-cover.html
```

### Playwright命令

```powershell
# 截图命令格式
& "playwright-path" screenshot --browser=chromium --full-page "file:///$htmlPath" "output.png"

# 示例
& "C:\Users\Administrator\AppData\Roaming\npm\node_modules\openclaw\skills\playwright-scraper-skill\node_modules\.bin\playwright.cmd" screenshot --browser=chromium --full-page "file://C:\Users\Administrator\.openclaw\scripts\templates\general-cover.html" "C:\Users\Administrator\.openclaw\scripts\output.png"
```

### 模板变量

| 变量 | 说明 | 示例 |
|------|------|------|
| {{title}} | 主标题 | 属虎人2026年转运指南 |
| {{subtitle}} | 副标题/描述 | 财运、感情、事业全解析 |
| {{emoji}} | emoji图标 | 🐯 |
| {{style}} | 风格名称 | warm, bold, cute... |
| {{size}} | 尺寸名称 | 1x1, 4x5, 9x16... |
| {{footer}} | 底部标语 | 免费图片生成器 |

---

## 输出规格

- **格式**：PNG（无损压缩）
- **质量**：高清晰度
- **生成时间**：5-10秒
- **文件大小**：通常500KB-2MB

---

## 优势

1. **完全免费** - 不需要任何API Key
2. **本地生成** - 不依赖网络
3. **无限使用** - 想生成多少生成多少
4. **质量清晰** - PNG格式，无压缩失真
5. **风格丰富** - 14种风格可选
6. **尺寸多样** - 适配各种平台
7. **快速便捷** - 输入主题即可
8. **完全可控** - HTML/CSS可自定义

---

## 依赖

- [Playwright](https://playwright.dev/)（已内置于OpenClaw skills）
- Chromium浏览器（自动安装）

---

## 更新日志

### v2.0.0
- ✅ 新增6种风格：gradient、neon、paper、marble、watercolor、poster
- ✅ 新增5种尺寸：1x1、4x5、9x16、16x9、4x3
- ✅ 去除"小红书"限定，改为通用图片生成器
- ✅ 简化使用方式，输入主题即可生成
- ✅ 优化HTML模板，支持尺寸自适应
- ✅ 更适合推广给更多用户

### v1.0.0
- 初始版本，小红书封面图生成器

---

## 作者

由大作家原创灵感，旺财整理发布
