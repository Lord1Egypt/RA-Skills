# 快速代回流程

目标：在不牺牲稳定性的前提下，把“回微信”压到尽量少的步骤。

## 单次代回

1. 定位微信主窗口。
2. 检查当前聊天头部是否已经是目标联系人。
3. 如果已经在目标聊天，不要再次搜索联系人。
4. 只读取最新消息，不要先跑整段历史再跑一次最新消息。
5. 生成简短、贴题的中文回复。
6. 用 `--message-file` 发送。

## 高频代回

1. 先启动守护进程：

```powershell
python scripts/wechat_assistant_daemon.py --start --exe "D:\app\Weixin\Weixin.exe"
```

2. 读取最新来消息：

```powershell
python scripts/wechat_assistant_daemon.py --read-latest-incoming --contact "mike--"
```

3. 发送消息：

```powershell
python scripts/wechat_assistant_daemon.py --send-message "收到，我来处理。" --contact "mike--"
```

## 提速原则

- 不重复搜索联系人。
- 不重复拖动聊天滚动条。
- 不重复 OCR 同一屏。
- 不为即时回消息触发网页搜索。
- 除非用户明确要完整上下文，否则 `history_lines` 控制在 `8-12` 即可。

## 中文发送建议

最稳的做法是先把回复写到 UTF-8 文本文件，再让脚本读取：

```powershell
python scripts/wechat_send.py --contact "mike--" --message-file "D:\temp\reply.txt"
```

这样能绕开控制台编码链路，减少中文乱码风险。
