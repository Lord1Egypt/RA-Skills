---

name: urlgo
description: 浏览器控制 CLI
metadata:
  slug: urlgo
  priority: 1000
  builtin_skill_version: "6.3.0"
  trigger: urlgo、浏览器、CDP、截图、网页、打开网页、网页截图、https://、http://
  copaw:
    emoji: "🌐"
    requires: {}
    auto_load: true
    global: true
---

## Keywords

https://, http://, www., 浏览器, CDP, 截图, 网页, mp.weixin, 打开网页, 网页截图

## Summary

连 CDP，开网页，截图，执行 JS。

## Strategy
1. `urlgo status` → CDP 开了没？没开就 `urlgo start`
2. `urlgo open <url>` → 打开页面
3. 截图/读取/点击/输入/执行 JS
4. 返回结果

AVOID:
- AVOID 不检查 CDP 就操作，先 status/start
- AVOID 忘装 websockets，截图和 JS 要用它
- AVOID 用 WebFetch 读网页，应该用 urlgo snapshot 代替

## ⚠️ 踩坑记录（2026-05-06）

### 1. urlgo 不在 PATH
urlgo 脚本不在系统 PATH 中，直接调用报 command not found。

**解法**：调用前将技能目录加入 PATH，或在命令中指定 skill base dir：
```bash
export PATH="$PATH:$(dirname $(readlink -f $0))/.."
```
或使用 skill base dir 全路径调用 `python3 <skill_dir>/urlgo`。

### 2. urlgo start 浏览器进程被 SIGHUP 杀死
旧版 `cmd_start()` 用 `subprocess.run` + shell `&` 启动浏览器。urlgo 脚本退出后，shell 向子进程发 SIGHUP，浏览器随之退出。表现为 `urlgo start` 后立即 `urlgo open` 报"CDP 未开启"。

**解法**：改用 `subprocess.Popen(start_new_session=True)`（Linux）或 `DETACHED_PROCESS`（Windows），断开浏览器与脚本的进程组关联。

### 3. urlgo start 阻塞等待
旧版有 5~10 秒循环轮询 CDP 端口，bash tool 下呈阻塞态，用户需中断。中断后旧版浏览器进程被连带杀死。

**解法**：新版无额外阻塞，最长等待 15 秒后超时返回。

### 4. bash tool 下无输出（stdout 缓冲）
bash tool 捕获 stdout 时 Python 启用块缓冲，`print` 输出积压不刷，bash tool 见"no output"即超时中断，误判为脚本假死。

**解法**：脚本入口加 `sys.stdout.reconfigure(line_buffering=True)`，每行输出即刷。

---

## 命令

| 命令 | 说明 |
|------|------|
| `urlgo status` | 检查 CDP |
| `urlgo start` | 启动浏览器 |
| `urlgo list` | 查看页面 |
| `urlgo open <url>` | 打开网页 |
| `urlgo screenshot <id> <file>` | 截图 |
| `urlgo snapshot <id>` | 读取内容 |
| `urlgo eval <id> "<js>"` | 执行 JS |
| `urlgo click <id> "<sel>"` | 点击 |
| `urlgo type <id> "<sel>" "<text>"` | 输入 |

## 示例

```bash
# 先加 PATH（如不在系统 PATH 中）
export PATH="$PATH:/path/to/urlgo/skill/dir"

# 启动浏览器（后台运行，不会阻塞）
urlgo start

# 打开网页
urlgo open https://example.com

# 读取内容 / 截图
urlgo snapshot 1
urlgo screenshot 1 /tmp/a.png
```

## 依赖

curl, websockets(Python)
