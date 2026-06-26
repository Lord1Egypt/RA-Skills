---
name: xiaohongshu-publisher
version: 2.3.0
description: Automatically publish notes to Xiaohongshu (小红书) creator center. Generates cover images (PIL poster, multiple styles), writes content from templates, and publishes via Playwright browser context. Cross-platform (Windows/macOS/Linux). Login once, publish many times. Use when user wants to post to 小红书, XHS, or Red Note.
---

# 小红书自动发布技能

自动发布笔记到小红书创作者中心。内容生成 → 封面图生成（多张） → 自动发布，全流程自动化。

## 核心特性

- ✅ 跨平台（Windows / macOS / Linux）
- ✅ 无硬编码路径，所有目录可通过环境变量或参数配置
- ✅ 浏览器会话默认不持久化到磁盘（安全），可通过 `--profile-dir` 或 `XHS_PROFILE_DIR` 显式开启
- ✅ 内容自动生成（6大话题模板库 + 通用模板）
- ✅ 封面图自动生成（5种布局 × 7种纹理 × 10种配色，每张风格不同）
- ✅ 多图上传（默认3张，可配置）
- ✅ 一条命令完成全流程

## 环境变量（可选）

| 变量 | 说明 | 默认值 |
|------|------|--------|
| `SKILL_DATA_DIR` | 数据根目录（图片/内容/截图） | `<skill>/.local/` |
| `XHS_PROFILE_DIR` | 浏览器 profile 目录（登录态持久化） | 临时目录（不持久化） |
| `XHS_FONT_PATH` | 自定义字体路径 | 系统默认中文字体 |

## 快速开始

### 首次登录（只需一次）

```bash
python scripts/save_login.py                          # 默认保存到 .local/xhs_browser_profile/
python scripts/save_login.py --profile-dir ~/xhs_data  # 自定义目录
```

### 一键发布

```bash
python scripts/auto_publish.py --topic 美食                                    # 临时 profile，不保留登录态
python scripts/auto_publish.py --topic 科技 --profile-dir .local/xhs_browser_profile  # 复用已保存的登录态
python scripts/auto_publish.py --topic 穿搭 --count 5
python scripts/auto_publish.py --topic 生活 --image a.png b.png c.png
```

也可以通过环境变量设置 profile 目录，避免每次传参：

```bash
export XHS_PROFILE_DIR=.local/xhs_browser_profile   # Linux/macOS
set XHS_PROFILE_DIR=.local\xhs_browser_profile       # Windows
python scripts/auto_publish.py --topic 美食
```

### 参数说明

| 参数 | 说明 | 默认值 |
|------|------|--------|
| `--topic` | 话题（美食/旅游/穿搭/科技/生活/健身） | 科技 |
| `--title` | 自定义标题（<20字） | 自动生成 |
| `--content` | 自定义正文 | 自动生成 |
| `--cover-text` | 封面图文字 | 用标题 |
| `--image` | 已有图片路径（可多张） | 自动生成 |
| `--profile-dir` | 浏览器 profile 目录（登录态持久化） | 临时目录 |
| `--count` | 生成图片数量 | 3 |

## 话题模板

| 话题 | 标题数 | 正文数 |
|------|--------|--------|
| 美食 | 8 | 2 |
| 旅游 | 7 | 2 |
| 穿搭 | 6 | 2 |
| 科技 | 8 | 3 |
| 生活 | 6 | 2 |
| 健身 | 5 | 1 |
| 通用 | 7 | 2 |

## 封面图风格

- 布局：居中大字报 / 顶部标题 / 左对齐杂志风 / 高亮框 / 数字装饰
- 纹理：网格 / 圆点 / 圆形 / 条纹 / 方块 / 噪点 / 纯色
- 配色：10种小红书风格（含浅色系和深色系）
- 尺寸：1080×1080（1:1）

## 文件结构

```
xiaohongshu-publisher/
├── SKILL.md
├── scripts/
│   ├── config.py               # 跨平台路径配置
│   ├── auto_publish.py         # 一键发布入口
│   ├── generate_content.py     # 内容生成
│   ├── generate_cover.py       # 封面图生成
│   ├── publish.py              # 发布流程
│   └── save_login.py           # 首次登录
└── references/
    └── selectors.md            # 页面选择器参考
```

## 依赖

```bash
pip install playwright pillow
playwright install chromium
```

## 发布流程

1. 打开 `creator.xiaohongshu.com/publish/publish`
2. 点击下拉箭头 → 选择"上传图文"
3. 通过 `accept` 属性定位图片 file input（区分视频/图片）
4. 逐张上传图片（每张间隔3秒）
5. 等待编辑器出现（轮询+滚动，最多30秒）
6. 填写正文（逐字输入）
7. 填写标题
8. 点击发布

## 故障排查

| 问题 | 解决方案 |
|------|----------|
| 未登录 | `python scripts/save_login.py` |
| 登录态失效 | 删除 profile 目录后重新运行 `save_login.py` |
| 找不到编辑器 | 查看 screenshots/ 截图和 HTML dump |
| 图片只上传1张 | 检查 file input 是否被正确重新定位 |
| 标题超长 | 自动截断到20字 |

## 更新日志

### v2.3 (2026-03-07)
- 跨平台：去除所有硬编码 Windows 路径（`E:\`、`C:\Windows\Fonts`）
- 安全：浏览器 profile 默认使用临时目录，不再自动持久化到磁盘
- 可配置：通过 `--profile-dir` 参数或 `XHS_PROFILE_DIR` / `SKILL_DATA_DIR` / `XHS_FONT_PATH` 环境变量自定义目录
- 字体：自动检测 Windows / macOS / Linux 系统中文字体
- 修复：`generate_cover.py` 噪点纹理在 RGBA 模式下的潜在 bug
- 新增：`config.py` 统一路径配置模块

### v2.2 (2026-03-06)
- 多图上传：逐张上传，默认3张
- 封面图升级：5种布局 + 7种纹理 + 10种配色，大字报风格
- 内容丰富：科技话题去掉 AI 硬编码，新增数码好物等模板
- 图片 input 精确定位：通过 accept 属性区分视频/图片 input
- 编辑器等待优化：轮询+滚动，最多30秒

### v2.1 (2026-03-06)
- persistent context 登录持久化
- Tab 切换修复（下拉箭头 → 上传图文）
- 图片尺寸 1080×1080

### v1.0
- 初始版本
