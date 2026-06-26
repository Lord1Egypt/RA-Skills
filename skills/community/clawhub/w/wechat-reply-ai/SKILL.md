---
name: wechat-auto-reply-toolkit
description: Windows 本地微信自动回复与消息处理工具。用于 Codex 需要在已登录的 PC 微信上执行联系人定位、OCR 读取最新消息、生成并发送中文回复、发送图片/视频/文件、截图最新图片预览、或启动常驻守护进程加速代回时。适用于“回 xxx”“查看微信最新消息”“帮我发图片/视频”“把微信代回流程固化成快路径”等场景。
---

# 微信自动回复工具

## 概览

使用这个 skill 处理 Windows 本地 PC 微信的聊天读取、消息发送和高频代回。

优先复用 `scripts/wechat_send.py` 与 `scripts/wechat_assistant_daemon.py`，不要重复重写窗口定位、OCR、滚动到底、中文发送编码和守护进程逻辑。

## 快速选择

1. 单次读取、单次回复、单次发送媒体文件：直接用 `scripts/wechat_send.py`
2. 连续多轮代回、想减少冷启动时间：先启动 `scripts/wechat_assistant_daemon.py`
3. 需要排查微信窗口、OCR 抓取、滚动到底、截图范围：先读 [references/ocr-and-window-rules.md](references/ocr-and-window-rules.md)
4. 需要决定回复口吻或代回风格：读 [references/reply-style-guide.md](references/reply-style-guide.md)
5. 需要确认环境、依赖、运行前提：读 [references/runtime-requirements.md](references/runtime-requirements.md)

## 标准工作流

1. 确认 Windows 已打开并登录 PC 微信，目标聊天可以在当前账号中搜索到。
2. 优先尝试复用当前聊天会话；如果聊天头部 OCR 已经匹配目标联系人，不要再次搜索联系人。
3. 优先读取“最新消息”而不是整屏聊天；除非需要上下文，否则不要重复跑 OCR。
4. 即时代回时，不要额外联网；只有用户明确要求“查证”“联网确认”“按最新资料回复”时再上网。
5. 生成回复后，优先走 `--message-file` 或守护进程发送，避免中文在终端链路中变成乱码或 `???`。
6. 如果用户只说“回 mike--”这一类短指令，完成发送后只向用户展示最终回出的内容，不展开思考过程。
7. 检测到 `Esc` 按键时，立刻中断调试或长轮询操作。

## 快速命令

### 单次读取最新可见消息

```powershell
python scripts/wechat_send.py --contact "mike--" --read-latest --history-lines 10 --exe "D:\app\Weixin\Weixin.exe"
```

### 单次读取最新来消息

```powershell
python scripts/wechat_send.py --contact "mike--" --read-latest-incoming --exe "D:\app\Weixin\Weixin.exe"
```

### 通过 UTF-8 文件发送中文回复

```powershell
python scripts/wechat_send.py --contact "mike--" --message-file "D:\temp\reply.txt" --exe "D:\app\Weixin\Weixin.exe"
```

### 发送图片、视频或任意文件

```powershell
python scripts/wechat_send.py --contact "mike--" --image "D:\pics\a.jpg" --video "D:\videos\b.mp4"
python scripts/wechat_send.py --contact "mike--" --file "D:\docs\report.pdf"
```

### 截取最新图片预览

```powershell
python scripts/wechat_send.py --contact "mike--" --capture-latest-image --preview-output "D:\temp\latest.png"
```

### 启动常驻助手并复用会话

```powershell
python scripts/wechat_assistant_daemon.py --start --exe "D:\app\Weixin\Weixin.exe"
python scripts/wechat_assistant_daemon.py --read-latest-incoming --contact "mike--"
python scripts/wechat_assistant_daemon.py --send-message "收到，我来处理。" --contact "mike--"
```

## 执行规则

- 优先走最快本地路径，不要在同一轮里重复搜索联系人、重复拖动滚动条、重复 OCR 同一块区域。
- 使用守护进程时，把“读消息”和“发消息”都交给 `scripts/wechat_assistant_daemon.py`，避免每次重新初始化 OCR。
- 微信窗口识别优先使用 `uiautomation` + `pywinauto` 的现有逻辑，避开托盘图标窗口和无效白屏窗口。
- 如果需要读取图片内容，先抓预览图，再决定是否做 OCR 或视觉识别；不要把聊天区里的 `[图片]` 占位符误当成真实图像内容。
- 对高风险场景的代回，例如医疗、法律、财务，回复要谨慎、具体、不过度承诺；必要时提醒用户及时联系线下专业人士。

## 资源导航

- 环境要求与依赖： [references/runtime-requirements.md](references/runtime-requirements.md)
- 快速代回流程与提速策略： [references/fast-reply-workflow.md](references/fast-reply-workflow.md)
- 微信窗口、滚动条、OCR 裁剪规则： [references/ocr-and-window-rules.md](references/ocr-and-window-rules.md)
- 常见代回口吻与安全边界： [references/reply-style-guide.md](references/reply-style-guide.md)
- 代回助手默认人设： [persona.md](persona.md)
