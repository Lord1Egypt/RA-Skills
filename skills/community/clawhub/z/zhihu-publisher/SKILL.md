---
name: zhihu-publisher
description: |
  知乎文章自动发布技能。通过 xbrowser 控制 Chrome 浏览器完成知乎登录、撰写和发布文章的全流程。
  触发词：发布知乎、知乎文章、zhihu publish、发知乎文章、知乎发文章。
  依赖：xbrowser skill（--browser chrome）。
---

# 知乎文章自动发布

## 依赖

- xbrowser skill，xb 路径：`D:\QClaw\resources\openclaw\config\skills\xbrowser\scripts\xb.cjs`
- Chrome 浏览器（`--browser chrome`），**禁止使用 cft/edge**（ref 失效 bug）

## 文章要求

- 目标字数：**1500 字**（含标点），下限 1200，上限 1800

## 流程一：登录（仅需一次）

### 1. 打开登录页
```bash
node xb.cjs run --browser chrome --headed open https://www.zhihu.com/signin
```

### 2. 切换密码登录
```bash
node xb.cjs run --browser chrome -- find role button click --name 密码登录
```

### 3. 获取 ref 并填写凭据
```bash
node xb.cjs run --browser chrome -- batch --bail "wait --load networkidle" "snapshot -i"
```
记录 textbox ref（通常账号 `@e39`、密码 `@e40`、登录按钮 `@e12`），然后：
```bash
node xb.cjs run --browser chrome -- batch --bail "fill @e39 <账号>" "fill @e40 <密码>" "click @e12"
```
> ⚠️ 账号密码通过用户输入获取，**禁止写死到文件中**。

### 4. 验证
- 如触发滑块验证码：URL 停留 `/signin`，需用户**手动拖动滑块**完成验证
- 登录成功：URL 变为 `https://www.zhihu.com/`

## 流程二：发布文章

### 1. 打开编辑器
```bash
node xb.cjs run --browser chrome --headed open https://zhuanlan.zhihu.com/write
node xb.cjs run --browser chrome -- batch --bail "wait --load networkidle" "snapshot -i"
```

### 2. 填标题
```bash
node xb.cjs run --browser chrome -- batch --bail "click @e25" "fill @e25 <标题>"
```

### 3. 填正文（长文本用 JS 逐段插入）
> ❌ 直接 `fill` 长文本（>500字符）会被命令行截断；`fill` 中的 `\n` 会变成普通字符。
>
> ✅ 用 `eval` + `document.execCommand('insertText')` 逐段插入，每段 <500 字符。

```bash
node xb.cjs run --browser chrome -- eval "document.querySelector('.DraftEditor-root [role=textbox]').focus()"
node xb.cjs run --browser chrome -- eval "document.execCommand('insertText', false, '第1段内容...')"
node xb.cjs run --browser chrome -- eval "document.execCommand('insertText', false, '\n\n## 标题\n\n第2段内容...')"
# 继续分段...
```

### 4. 智能排版
```bash
node xb.cjs run --browser chrome -- batch --bail "snapshot -i" "click @e48"
```
> `@e48` 为创作助手面板中的「智能排版」按钮（name 含"智能排版自动修正空格"），实际 ref 以 snapshot 为准。

### 5. 发布
```bash
node xb.cjs run --browser chrome -- batch --bail "snapshot -i" "click @e37" "wait --load networkidle"
```
成功标志：URL 变为 `https://zhuanlan.zhihu.com/p/<ID>`，出现发布成功弹窗。

## 核心规则

| 规则 | 说明 |
|------|------|
| ref 必须每次刷新 | 每步操作前 `snapshot -i`，ref 只在同一 batch 内有效 |
| 禁止跨 batch 用 ref | batch 之间 ref 编号会重新生成 |
| 长文本用 eval | >500 字符的正文必须用 `document.execCommand('insertText')` 分段插入 |
| 正文后必须排版 | 插入完成后点击「智能排版」修复换行和标点 |
| 全程用 chrome | cft/edge 有 ref 失效 bug，`--browser chrome` 是唯一可靠选项 |
