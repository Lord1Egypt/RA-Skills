---
name: ZeeLin 微博自动发布
description: "通过浏览器操作网页版微博，用户登录后 Agent 撰写内容并自动发布。无需 API，需 Browser Relay 挂上微博标签页。Keywords: 微博, 发微博, 自动发布, Weibo, ZeeLin."
user-invocable: true
metadata: {"openclaw":{"emoji":"📱","skillKey":"zeelin-weibo-autopost"}}
---

# ZeeLin 微博自动发布 📱

通过**网页版微博**（weibo.com）自动发微博：用户先登录，Agent 撰写内容后用脚本打开微博、填入正文、点击发布。

---

## 何时触发

- 「发一条微博」「帮我发微博」「自动发微博」
- 「把这段话发到微博」「写一条微博并发布」
- 「微博自动发布」

**爬取微博**：用户说「爬取微博」「抓取微博内容」时，见 TOOLS.md「爬取微博（防卡住）」——用 web_fetch 抓**至多 1～2 条具体链接**，或 browser **只 open + snapshot 一次**即返回，不要无限滚动或多次操作，否则易卡住。

---

## 使用前准备

1. **登录微博**：在 Chrome 打开 https://weibo.com 并登录。
2. **挂上 Browser Relay**：在该标签页点击 OpenClaw Browser Relay 扩展，Badge 显示 **ON**。
3. 执行发微博时脚本会打开微博页、找发微博入口、输入内容、点发布。

---

## 工作流程

### Step 1：确认内容

用户给文案或主题。若只给主题，Agent 生成一条微博正文（建议 140～500 字，可带话题 #xxx）。

### Step 2：执行发布脚本

用 `exec` 执行脚本，传入微博正文。**必须传 timeout**（建议 60000）避免 request timed out：

```json
{"tool": "exec", "args": {"command": "bash /Users/youke/.openclaw/workspace/skills/zeelin-weibo-autopost/scripts/post_weibo.sh \"微博正文内容\"", "timeout": 60000}}
```

（若报脚本未找到，请把路径中的 `/Users/youke` 改成你本机用户家目录；Windows 用户改为实际 SKILL 路径，如 `C:/Users/xxx/AppData/Roaming/ZeeLinClaw/SKILLs/zeelin-weibo-autopost/scripts/post_weibo.sh`。）

### Step 3：回报结果

根据脚本输出告诉用户「已提交发布，请到微博页面确认」；若脚本报错，提示检查是否已登录、Relay 是否挂上。

---

## exec 速查

| 操作 | 命令 |
|------|------|
| 发微博 | `bash .../zeelin-weibo-autopost/scripts/post_weibo.sh "正文"`，exec 加 `"timeout": 60000` |

---

## 故障排查

| 现象 | 处理 |
|------|------|
| 脚本未找到 | 使用绝对路径，与 openclaw.json / ZeeLin Claw 的 workspace 一致。 |
| openclaw browser 无输出 | 需已用 Browser Relay 挂上微博标签页（Badge ON），且 Gateway 已启动。 |
| **脚本执行了但微博没发出去** | ① 确认发微博时**当前 Relay 挂上的就是微博页**（weibo.com），且已登录。② 脚本会把每次快照写入 ` /tmp/weibo_snap.txt`，若仍失败请打开该文件，看是否有「发微博」「说点什么」「发布」等字样及对应的 `ref=e数字`；若页面结构变了，可把快照中相关几行发给开发者以更新选择器。③ 微博首页有时是信息流，需先点击顶栏或左侧的「发微博」打开发布框，脚本已包含该步骤；若你看到发布框已打开但未填入或未点发布，多半是输入框/发布按钮的 ref 与当前页面不匹配，需根据快照调整。 |
