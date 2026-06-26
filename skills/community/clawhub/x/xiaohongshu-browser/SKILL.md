---
name: xiaohongshu-browser
description: Browse Xiaohongshu (小红书) and take screenshots of posts. Supports keyword search, post modal screenshots, and returns post links. Requires prior manual login.
tags:
  - xiaohongshu
  - social-media
  - scraping
  - screenshot
requires:
  bins:
    - python
  env: []
---

# Xiaohongshu Browser / 小红书浏览器

用 Playwright 自动化浏览小红书，搜索关键词并截图帖子弹窗预览。

Automate Xiaohongshu browsing — search keywords and screenshot post modal previews.

## 前置要求 / Prerequisites

**Python 3.x** + **Playwright**：

```bash
pip install playwright
playwright install chromium
```

## 使用步骤

### 第一步：首次登录（只需要做一次）

1. 运行登录脚本，会弹出浏览器窗口：

```bash
python <skill_dir>/scripts/xhs_open.py
```

2. 在弹出的浏览器里**手动登录小红书**（扫码或账号密码都行）

3. 登录成功后，创建一个控制文件来保存登录状态：

```bash
# Windows (PowerShell):
Set-Content "$env:USERPROFILE\.openclaw\.close_browser" "CLOSE"

# Windows (CMD):
echo CLOSE > %USERPROFILE%\.openclaw\.close_browser

# Linux / macOS:
echo CLOSE > ~/.openclaw/.close_browser
```

4. 看到终端输出 `AUTH_SAVED` 就说明登录状态保存好了

> 💡 登录状态保存在 `~/.openclaw/xhs_data`，以后搜索时会自动使用，不需要重复登录。

### 第二步：搜索并截图

```bash
python <skill_dir>/scripts/xhs_search.py "关键词" 数量
```

**参数说明：**
- 第一个参数：搜索关键词（默认：`御姐`）
- 第二个参数：截图几个帖子（默认：`5`）

**示例：**

```bash
# 搜索"美食"，截图前3个帖子
python <skill_dir>/scripts/xhs_search.py "美食" 3

# 搜索"穿搭"，截图前10个
python <skill_dir>/scripts/xhs_search.py "穿搭" 10

# 不传参数，用默认值
python <skill_dir>/scripts/xhs_search.py
```

### 输出结果

截图保存在 `<skill_dir>/output/` 目录，文件名格式：`post_序号_时间戳.png`

每张截图包含帖子弹窗预览（图文详情）。

## 常见问题

### 需要重新登录？

小红书的登录会过期，如果搜索时遇到登录弹窗，需要重新登录：

```bash
# 1. 删除旧的登录数据
# Windows:
Remove-Item -Recurse -Force "$env:USERPROFILE\.openclaw\xhs_data"
# Linux / macOS:
rm -rf ~/.openclaw/xhs_data

# 2. 重新运行登录脚本
python <skill_dir>/scripts/xhs_open.py
```

### 搜索没结果？

- 小红书可能会限制频繁访问，等几分钟再试
- 关键词不要太长，2-6个字最佳
- 不要带 `#` 号，直接搜关键词

## 目录结构

```
xiaohongshu-browser/
├── SKILL.md              # 本说明文件
├── scripts/
│   ├── xhs_open.py       # 登录脚本（首次使用）
│   └── xhs_search.py     # 搜索+截图脚本
└── output/               # 截图输出目录
```

## 注意事项

- 使用无头浏览器（headless），不会弹出窗口
- 操作间有随机延迟，降低被检测风险
- 频繁使用可能触发小红书的反爬机制
- 帖子链接需要 `xsec_token` 才能直接访问（搜索结果中已包含）
