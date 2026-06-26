---
name: tencent-lke-chat
description: 腾讯云智能体开发平台 HTTP SSE 对话接口技能。用于调用腾讯云智能体对话接口，支持流式响应处理、事件解析（reply/token_stat/reference/error/thought）。在需要与腾讯云LKE智能体进行HTTP SSE对话时使用，包括发送消息、处理流式响应、解析各类事件。
---

# 腾讯云智能体对话接口 (HTTP SSE)

本技能提供腾讯云智能体开发平台的HTTP SSE对话接口调用指导。

## 接口概览

- **请求地址**: `https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse`
- **请求方式**: POST
- **协议**: HTTP SSE (Server-Sent Events)

## 快速开始

### 1. 获取 AppKey

在腾讯云控制台 > 智能体开发平台 > 应用管理 > 发布管理中获取应用的 AppKey。

### 2. 基本调用示例

```bash
curl --location 'https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse' \
--header 'Content-Type: application/json' \
--data '{
  "session_id": "a29bae68-cb1c-489d-8097-6be78f136acf",
  "bot_app_key": "YourAppKey",
  "visitor_biz_id": "a29bae68-cb1c-489d-8097-6be78f136acf",
  "content": "你好",
  "incremental": true,
  "streaming_throttle": 10
}'
```

## 请求参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| session_id | string(64) | 是 | 会话ID，2-64字符，格式：^[a-zA-Z0-9_-]{2,64}$ |
| bot_app_key | string(128) | 是 | 应用密钥 |
| visitor_biz_id | string(64) | 是 | 访客ID，标识当前用户 |
| content | string | 是 | 消息内容 |
| request_id | string(255) | 否 | 请求ID，用于消息串联 |
| file_infos | Object[] | 否 | 文件信息（需配合实时文档解析） |
| streaming_throttle | int32 | 否 | 流式回包频率控制，默认5 |
| custom_variables | map[string]string | 否 | 自定义参数（工作流/API参数） |
| system_role | string | 否 | 角色指令（提示词） |
| incremental | bool | 否 | 内容是否增量输出，默认false |
| search_network | string | 否 | 联网搜索：enable/disable/空（跟随配置） |
| model_name | string | 否 | 指定模型：hunyuan/lke-deepseek-r1/lke-deepseek-v3 等 |
| stream | string | 否 | 是否流式：enable/disable/空 |
| workflow_status | string | 否 | 工作流开关：enable/disable/空 |

### file_infos 数据结构

```json
{
  "file_name": "文档.pdf",
  "file_size": "1024000",
  "file_url": "https://cos.url/xxx",
  "file_type": "pdf",
  "doc_id": "doc_xxx"
}
```

## 响应事件类型

SSE流会返回以下事件类型：

### 1. reply - 回复事件

```json
{
  "type": "reply",
  "payload": {
    "content": "回复内容",
    "is_final": false,
    "is_evil": false,
    "is_from_self": false,
    "is_llm_generated": true,
    "record_id": "msg_xxx",
    "session_id": "session_xxx",
    "timestamp": 1701330805,
    "reply_method": 1,
    "knowledge": [...],
    "quote_infos": [...]
  }
}
```

**关键字段**:
- `is_final`: true表示消息输出完毕
- `is_evil`: true表示命中敏感内容
- `reply_method`: 回复方式（1=大模型回复, 16=工作流回复, 18=智能体回复等）
- `quote_infos`: 引用信息，用于标注参考来源

### 2. token_stat - Token统计事件

```json
{
  "type": "token_stat",
  "payload": {
    "elapsed": 1616,
    "token_count": 323,
    "status_summary": "success",
    "procedures": [
      {
        "name": "knowledge",
        "title": "调用知识库",
        "status": "success",
        "input_count": 308,
        "output_count": 15
      }
    ]
  }
}
```

### 3. reference - 参考来源事件

```json
{
  "type": "reference",
  "payload": {
    "record_id": "msg_xxx",
    "references": [
      {
        "id": "ref_xxx",
        "type": 2,
        "name": "文档名称",
        "doc_name": "xxx.docx",
        "url": "https://..."
      }
    ]
  }
}
```

**参考来源类型**:
- 1: 问答
- 2: 文档片段
- 4: 联网检索内容

### 4. thought - 思考事件 (DeepSeek-R1)

```json
{
  "type": "thought",
  "payload": {
    "procedures": [
      {
        "name": "thought",
        "title": "思考",
        "debugging": {
          "content": "思考过程..."
        }
      }
    ]
  }
}
```

### 5. error - 错误事件

```json
{
  "type": "error",
  "error": {
    "code": 460004,
    "message": "应用不存在"
  }
}
```

## 错误码

| 错误码 | 说明 |
|--------|------|
| 400 | 请求参数错误 |
| 460001 | Token校验失败 |
| 460004 | 应用不存在 |
| 460007 | 会话创建失败 |
| 460011 | 超出并发数限制 |
| 460020 | 模型请求超时 |
| 460032 | 模型余额不足 |
| 460034 | 输入内容过长 |

## 进阶用法

### 使用自定义模型

```json
{
  "model_name": "lke-deepseek-r1",
  "content": "你好"
}
```

支持的模型:
- `hunyuan`: 混元高级版
- `hunyuan-turbo`: 混元Turbo版
- `lke-deepseek-r1`: DeepSeek-R1
- `lke-deepseek-v3`: DeepSeek-V3
- `lke-deepseek-r1-0528`: DeepSeek-R1-0528
- `lke-deepseek-v3-0324`: DeepSeek-V3-0324

### 工作流参数传递

```json
{
  "custom_variables": {
    "UserID": "10220022",
    "Data": "{\"Score\":{\"Chinese\":89}}"
  }
}
```

### 知识库检索范围设置

```json
{
  "custom_variables": {
    "tag_field": "user1|user2"
  }
}
```

## 前端渲染组件

如需前端渲染消息，可使用官方组件:

```bash
# Vue 2 或 React
npm install lke-component

# Vue 3
npm install lke-component-vue3
```

## 参考资料

- 完整接口文档: [references/api_reference.md](references/api_reference.md)
- 示例脚本: [scripts/](scripts/)
