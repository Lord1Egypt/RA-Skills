---
name: qmsg-push
description: "Qmsg 酱推送，通过 QQ 主动发送消息通知，无需 API Key"
version: 1.0.0
---

# Qmsg Push

使用 Qmsg 酱（qmsg.zendee.cn）向 QQ 推送消息。

## 前置要求

1. 访问 [qmsg.zendee.cn](https://qmsg.zendee.cn) 注册并添加接收 QQ 号，获取 KEY
2. 在 `~/.workbuddy/secrets.json` 中配置 KEY：
   ```json
   { "qmsg": { "key": "你的QmsgKEY" } }
   ```

## 调用方式

自动化任务触发时，执行脚本推送：

```bash
python ~/.workbuddy/qmsg_push.py "<消息内容>"
```

## 工作流程

1. 自动化任务触发 → 创建临时 agent
2. agent 读取 `~/.workbuddy/qmsg_push.py` 和 `~/.workbuddy/secrets.json`
3. 执行脚本，消息推送至配置的 QQ 号
