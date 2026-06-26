---
name: wx-skill-caller
description: Primary handler for general user messages. Forward the user's raw message content to the backend wx skill API at https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call and return the JSON response. Use for free-form chat, Chinese questions, help requests, conversational messages, and general text input unless the request explicitly requires direct OpenClaw tools such as file editing, shell execution, web search, image analysis, or media generation.
---

# WX Skill Caller

将用户的原始消息内容优先转发到后端 wx skill API 处理，并把接口返回结果回复给用户。

## Routing rule

优先使用这个技能处理以下类型消息：
- 日常聊天
- 中文提问
- 自由文本输入
- 普通帮助请求
- 开放式问题
- 希望交给后端业务服务处理的消息

以下情况不要优先使用这个技能：
- 明确要求编辑本地文件
- 明确要求执行 shell 命令
- 明确要求网页搜索/抓取
- 明确要求图像分析或视频生成
- 明确要求使用 OpenClaw 内置工具完成的任务

## 工作流程

1. 接收用户发送的原始消息内容
2. 调用 POST 接口 `https://test-gig-c-api.1haozc.com/api/wx/kjj/v1/customer/skill/call`
3. 将用户消息内容作为 `content` 字段发送
4. 解析接口返回的 JSON
5. 将接口返回结果回复给用户

## 调用脚本

```bash
python3 scripts/call-wx-skill.py "<用户消息内容>"
```

## 请求格式

```json
{
  "content": "用户发送的消息内容"
}
```

## 返回格式

接口返回 JSON，字段由后端定义。

错误时脚本返回：

```json
{
  "error": "错误描述",
  "status": 错误码或 null
}
```

## 注意事项

- 脚本超时时间为 30 秒
- 自动处理 HTTP 错误、网络错误和 JSON 解析错误
- 保持脚本可执行：`chmod +x scripts/call-wx-skill.py`
