---
name: publish-wechat-draft
description: 发布文章到微信公众号草稿箱。当用户要求发布公众号文章、保存微信草稿、publish wechat draft、或提到"发公众号"/"发微信"时调用。
version: 1.0.0
tools: Read, Bash, Edit, Write
metadata:
  openclaw:
    requires:
      env:
        - WECHAT_PUBLISHER_DIR
      bins:
        - node
        - npm
        - npx
        - git
    primaryEnv: WECHAT_PUBLISHER_DIR
    homepage: https://github.com/lixinran2015/weixingongzhonghao
---

# 微信公众号草稿发布 Skill

使用项目 `weixingongzhonghao-publisher` 的 CLI 工具，将文章发布到微信公众号草稿箱。

## 前置检查

### 1. 查找项目目录

按以下优先级确定 `weixingongzhonghao-publisher` 的项目根目录（`PROJECT_DIR`）：

1. **当前工作目录**：检查是否存在 `package.json` 且 `name` 为 `weixingongzhonghao-publisher`。
2. **环境变量**：如 `process.env.WECHAT_PUBLISHER_DIR` 存在且包含有效的 `package.json`。
3. **用户主目录**：检查 `~/workspace/weixingongzhonghao` 或 `~/weixingongzhonghao` 是否存在有效的 `package.json`。
4. **以上都未找到**：提示用户先执行以下命令之一：
   ```bash
   # 方式 A：克隆仓库到当前目录
   git clone https://github.com/lixinran2015/weixingongzhonghao.git
   cd weixingongzhonghao

   # 方式 B：设置环境变量（如果仓库在其他位置）
   export WECHAT_PUBLISHER_DIR=/path/to/weixingongzhonghao
   ```

一旦找到 `PROJECT_DIR`，后续所有 `npm run` 命令都必须在 `PROJECT_DIR` 下执行（通过 `Bash` 的 `cwd` 或在命令前加 `cd PROJECT_DIR &&`）。

### 2. 确认依赖已安装

在 `PROJECT_DIR` 下运行：
```bash
ls node_modules/.bin/playwright
```
如不存在，运行：
```bash
cd PROJECT_DIR && npm install && npx playwright install chromium
```

## 登录与 Cookie 管理

1. **确定 Cookie 路径**：
   ```bash
   cd PROJECT_DIR && node -e "const p=require('path'); console.log(p.join(process.env.HOME||process.env.USERPROFILE,'.config','weixingongzhonghao','cookies.json'))"
   ```
2. **检查 Cookie 是否有效**：
   ```bash
   cd PROJECT_DIR && npm run check:login
   ```
   - 如果提示 Cookie 无效或为空，**先执行 `cd PROJECT_DIR && npm run login`**：这会打开浏览器等待用户扫码，登录成功后自动保存 Cookie。
   - 如果用户拒绝扫码，停止执行。

## 解析用户意图与文章源

用户可能通过以下几种方式提供内容：

### 方式 A：提供 HTML/MD 文件路径
- 如果路径是相对路径，先基于当前工作目录解析为绝对路径。
- 然后直接在 `PROJECT_DIR` 下使用 `--file` 模式：
  ```bash
  cd PROJECT_DIR && npm run publish -- --file <absolute-path> [--title "标题"]
  ```
- 标题优先级：`--title` 参数 > HTML `<title>` 标签 > 文件名

### 方式 B：只提供纯文本或 Markdown 内容
- 帮用户生成临时 HTML 文件到 `PROJECT_DIR/articles/` 目录：
  1. 读取 `PROJECT_DIR/articles/` 下现有文件，确定可用文件名（如 `articles/untitled-1.html`）
  2. 将内容包装成基础 HTML 结构：
     ```html
     <!DOCTYPE html>
     <html>
     <head><meta charset="utf-8"><title>用户提供的标题</title></head>
     <body>...用户内容...</body>
     </html>
     ```
  3. 使用 `Write` 写入 `PROJECT_DIR/articles/untitled-N.html`
  4. 然后以 `--file` 方式调用发布

### 方式 C：提供配置文件路径
- 如果用户明确要求使用某个 yaml 配置：
  ```bash
  cd PROJECT_DIR && npm run publish -- --config <path>
  ```

## 发布执行流程

1. 如果用户要求调试或首次运行，追加 `--debug` 参数（显示浏览器窗口，slowMo 1000ms）。
2. 运行发布命令，timeout 建议设为 300 秒（Playwright 操作较慢）。
3. **不要静默执行**：在打开浏览器扫码前，明确告知用户需要操作什么。

## 结果反馈

- **成功**：返回草稿链接、耗时，并祝贺用户。
- **失败**：
  1. 读取 `PROJECT_DIR/logs/screenshots/` 下最新的错误截图（按修改时间排序）
  2. 分析截图和终端输出，给出明确的错误原因和下一步建议

## 安全与隐私原则

- **绝不读取或泄露 Cookie 内容**。只验证文件是否存在、格式是否正确。
- **绝不把 Cookie 文件提交到 git**。如发现 `cookies/cookies.json` 被 git 跟踪，立即提醒用户取消跟踪。
- 用户扫码登录时，浏览器窗口由用户控制，Claude 不模拟任何登录操作。
