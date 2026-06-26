---
name: xhs-publisher
description: 小红书笔记创作与发布完整技能。用户给定主题或资料，自动完成：文案撰写 → Markdown 卡片生成 → 图片渲染 → 小红书发布，全流程一键完成。
author: merged from content-writer + xhs-note-creator
license: MIT
platforms:
  - openclaw
tags:
  - xhs
  - 小红书
  - content
  - social-media
  - publishing
---

# 小红书笔记创作与发布技能

一键完成从主题到小红书发布的全流程：文案撰写 → 生成 Markdown → 渲染图片卡片 → 自动发布。

## 使用方式

当用户说「发小红书」「写一篇小红书」「发布到小红书」「生成小红书笔记」时触发本技能。

### 输入确认

收到请求后，开始制作。第四步「发布小红书」前会展示内容预览，
**必须等用户明确确认「可以发布」后才执行发布**，不会自动发布。

### 工作流程

自动完成以下 4 步，第四步需用户确认：

#### 第一步：撰写小红书文案

根据用户主题，生成完整小红书风格内容，包括：
- 吸引眼球的标题（≤20字）
- 钩子开头（1-2句激发好奇）
- 正文（分段清晰，每段 2-3 句，含 emoji 点缀）
- 总结 + CTA
- Tags 标签（5-10 个）

#### 第二步：生成渲染用 Markdown

将文案写成专用于图片渲染的 Markdown 文件：

```markdown
---
emoji: "🤖"
title: "大标题（≤15字）"
subtitle: "副标题（≤15字）"
---

# 第一部分标题

正文内容...

# 第二部分标题

正文内容...

...
```

**注意**：正文用 `---` 分隔符分成多个段落，每段约 200-400 字左右，避免单段内容过长导致渲染被截断。

#### 第三步：渲染图片卡片

```bash
python3 scripts/render_xhs.py <markdown_file> -o <输出目录> -m auto-split -t default
```

- 推荐模式：`auto-split`（根据内容高度自动切分，不会截断内容）
- 默认主题：`default`（简约灰白）
- 生成的图片：封面 `cover.png` + 正文卡片 `card_1.png` `card_2.png` ...

#### 第四步：发布小红书

```bash
XHS_COOKIE=<cookie> python3 scripts/publish_xhs.py \
  --title "<标题>" \
  --desc "<描述>" \
  --images cover.png card_1.png card_2.png ...
```

- Cookie 从 `~/.openclaw/workspace/.xhs_cookie.env` 读取
- Cookie 失效时告知用户重新提供

---

## 图片规格

| 类型 | 尺寸 | 比例 |
|------|------|------|
| 封面 | 1080×1440px | 3:4 |
| 正文卡片 | 1080×? px | 3:4（高度按内容自适应）|

---

## 可用主题

| 主题 | 风格 |
|------|------|
| `default` | 简约灰白（默认）|
| `playful-geometric` | 活泼几何（紫粉渐变）|
| `neo-brutalism` | 新粗野主义（红黄撞色）|
| `botanical` | 植物园自然（绿色系）|
| `professional` | 专业商务（蓝色系）|
| `retro` | 复古怀旧（橙棕系）|
| `terminal` | 终端命令行（暗黑系）|
| `sketch` | 手绘素描（灰调）|

---

## 分页模式说明

| 模式 | 适用场景 |
|------|---------|
| `auto-split` | **推荐**。内容长短不稳定时使用，自动切分不会截断 |
| `separator` | 内容已手动用 `---` 控制好量 |
| `auto-fit` | 固定尺寸，整体缩放文字填满 |
| `dynamic` | 根据内容动态调整高度（仅适合短内容）|

---

## Cookie 配置

> ⚠️ **安全警告**：Cookie 等同于账号密码！
> - 持有此 Cookie 可代表您的账号进行发布操作
> - 请勿在公开场合分享
> - 建议使用专用小号，并及时在网页端撤销授权

Cookie 保存在：`~/.openclaw/workspace/.xhs_cookie.env`

格式：
```
XHS_COOKIE=your_cookie_string_here
```

获取方式：
1. 浏览器登录小红书（https://www.xiaohongshu.com）
2. F12 → Network → 任意请求 → Request Headers → 复制 `Cookie` 字段
3. 告知 Agent 更新
4. 如需撤销：网页端 → 设置 → 账号安全 → 退出登录对应设备

---

## 依赖安装

如遇缺少依赖提示，运行：
```bash
pip install markdown PyYAML playwright xhs python-dotenv requests
playwright install chromium
```
