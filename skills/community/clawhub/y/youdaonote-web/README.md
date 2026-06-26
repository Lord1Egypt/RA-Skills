# Youdao Note Skill

这个 Skill 用于在 Claw / OpenClaw 中操作有道云笔记，主要能力包括：
- 读取笔记内容（含新版压缩笔记）
- 搜索与遍历目录笔记
- 创建笔记

## 使用前提

### 1) 配置环境变量 `YOUDAO_COOKIE`
直接在系统环境变量中新增：
- 变量名：`YOUDAO_COOKIE`
- 变量值：浏览器里复制的**完整 Cookie 字符串**

这段完整 Cookie 必须包含：`YNOTE_CSTK`、`YNOTE_LOGIN`、`YNOTE_SESS`。

获取方式（简版）：
1. 登录 [有道云笔记网页版](https://note.youdao.com/)
2. F12 → Network → 任意请求
3. 复制 Request Headers 中的整段 `Cookie`

设置完成后重启终端/IDE，使环境变量生效。

### 2) 安装依赖
Skill 运行环境需要安装以下依赖：
- `requests`
- `brotli`（必须，用于解码 `Content-Encoding: br`）

安装命令：
```bash
pip install -r requirements.txt
```

## 说明
- 如果能列目录但读不到正文，优先检查 `YOUDAO_COOKIE` 是否过期，重新复制最新完整 Cookie。
- 搜索能力已按网页版请求协议调整，适合作为定位目录与笔记的入口。
- 与 Agent / Claw 对话时，建议直接提供目标文件夹的网页链接（或明确目录信息），这样它可以更快定位并读取 `dir id` 。
示例：
给 Agent / Claw 发送 https://note.youdao.com/web/#/file/WEB807032d64xxxxxxa0xxxxxx87fxxxxxx/note/WEB807032d64xxxxxx45xxxxxxcd4xxxxxx/
建议先让他识别url后列出目录，做一个校对，再开始总结这个目录下的所有笔记。
