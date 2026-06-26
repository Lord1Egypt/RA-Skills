# HTTP SSE 接口完整参考

## 请求地址

```
POST https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse
```

## 请求头

```
Content-Type: application/json
```

## 完整请求参数表

### 基础参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| session_id | string(64) | 是 | 会话ID，2-64字符，格式: `^[a-zA-Z0-9_-]{2,64}$` |
| bot_app_key | string(128) | 是 | 应用密钥 |
| visitor_biz_id | string(64) | 是 | 访客ID，标识当前用户 |
| content | string | 是 | 消息内容，最大长度取决于模型 |
| request_id | string(255) | 否 | 请求ID，用于消息串联，建议必填 |

### 高级参数

| 参数名 | 类型 | 必填 | 默认值 | 说明 |
|--------|------|------|--------|------|
| streaming_throttle | int32 | 否 | 5 | 流式回包频率，建议最大100 |
| incremental | bool | 否 | false | 内容是否增量输出 |
| system_role | string | 否 | - | 角色指令（提示词），标准模式生效 |
| search_network | string | 否 | "" | 联网搜索: enable/disable/空 |
| stream | string | 否 | "" | 流式传输: enable/disable/空 |
| workflow_status | string | 否 | "" | 工作流: enable/disable/空 |
| model_name | string | 否 | - | 指定模型名称 |

### 自定义参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| custom_variables | map[string]string | 否 | 自定义参数，用于工作流或知识库检索范围 |
| visitor_labels | Object[] | 否 | 知识标签列表 |

### 文件参数

| 参数名 | 类型 | 必填 | 说明 |
|--------|------|------|------|
| file_infos | Object[] | 否 | 文件信息数组，配合实时文档解析使用 |

## 模型列表

| 模型名称 | 说明 |
|----------|------|
| hunyuan | 混元大模型高级版 |
| hunyuan-13B | 混元大模型标准版 |
| hunyuan-turbo | 混元大模型Turbo版 |
| hunyuan-standard-256K | 混元大模型长文本版 |
| hunyuan-role | 混元大模型角色扮演版 |
| lke-deepseek-r1 | DeepSeek-R1 |
| lke-deepseek-v3 | DeepSeek-V3 |
| lke-deepseek-r1-0528 | DeepSeek-R1-0528 |
| lke-deepseek-v3-0324 | DeepSeek-V3-0324 |

## 回复方式 (reply_method)

| 值 | 说明 |
|----|------|
| 1 | 大模型回复 |
| 2 | 未知问题回复 |
| 3 | 拒答问题回复 |
| 4 | 敏感回复 |
| 5 | 已采纳问答对优先回复 |
| 6 | 欢迎语回复 |
| 7 | 并发数超限回复 |
| 8 | 全局干预知识 |
| 9 | 任务流回复 |
| 10 | 任务流答案 |
| 11 | 搜索引擎回复 |
| 12 | 知识润色后回复 |
| 13 | 图片理解回复 |
| 14 | 实时文档回复 |
| 15 | 澄清确认回复 |
| 16 | 工作流回复 |
| 17 | 工作流运行结束 |
| 18 | 智能体回复 |
| 19 | 多意图回复 |

## 完整错误码表

| 错误码 | 错误信息 |
|--------|----------|
| 400 | 请求参数错误 |
| 460001 | Token校验失败 |
| 460002 | 事件处理器不存在 |
| 460004 | 应用不存在 |
| 460006 | 消息不存在或没有操作权限 |
| 460007 | 会话创建失败 |
| 460008 | Prompt渲染失败 |
| 460009 | 访客用户不存在 |
| 460010 | 会话不存在或没有操作权限 |
| 460011 | 超出并发数限制 |
| 460020 | 模型请求超时 |
| 460021 | 知识库未发布 |
| 460022 | 访客创建失败 |
| 460023 | 消息点赞点踩失败 |
| 460024 | 标签不合法 |
| 460025 | 图像识别失败 |
| 460031 | 当前应用连接数超出请求限制 |
| 460032 | 当前应用模型余额不足 |
| 460033 | 应用不存在或没有操作权限 |
| 460034 | 输入内容过长 |
| 460035 | 计算内容过长 |
| 460036 | 任务流程节点预览参数异常 |
| 460037 | 搜索资源已用尽 |
| 460038 | 该AppID请求存在异常行为 |

## cURL 完整示例

### 基础对话

```bash
curl --location 'https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse' \
--header 'Content-Type: application/json' \
--data '{
  "session_id": "a29bae68-cb1c-489d-8097-6be78f136acf",
  "bot_app_key": "YourAppKey",
  "visitor_biz_id": "visitor_123",
  "content": "你好"
}'
```

### 使用 DeepSeek-R1 模型

```bash
curl --location 'https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse' \
--header 'Content-Type: application/json' \
--data '{
  "session_id": "session_123",
  "bot_app_key": "YourAppKey",
  "visitor_biz_id": "visitor_123",
  "content": "解释量子计算",
  "model_name": "lke-deepseek-r1",
  "incremental": true
}'
```

### 带工作流参数

```bash
curl --location 'https://wss.lke.cloud.tencent.com/v1/qbot/chat/sse' \
--header 'Content-Type: application/json' \
--data '{
  "session_id": "session_123",
  "bot_app_key": "YourAppKey",
  "visitor_biz_id": "visitor_123",
  "content": "查询订单",
  "custom_variables": {
    "UserID": "10220022",
    "OrderType": "online"
  },
  "workflow_status": "enable"
}'
```

## SSE 响应格式详解

SSE流格式：

```
event:reply
data:{"type":"reply","payload":{...}}

event:token_stat
data:{"type":"token_stat","payload":{...}}
```

### 事件类型说明

| 事件名 | 方向 | 说明 |
|--------|------|------|
| reply | 后端>前端 | 回复内容 |
| token_stat | 后端>前端 | Token使用统计 |
| reference | 后端>前端 | 参考来源 |
| thought | 后端>前端 | 思考过程 (DeepSeek-R1) |
| error | 后端>前端 | 错误信息 |

## 工作流节点类型

| 值 | 节点类型 |
|----|----------|
| 1 | 开始节点 |
| 2 | 参数提取节点 |
| 3 | 大模型节点 |
| 4 | 知识问答节点 |
| 5 | 知识检索节点 |
| 6 | 标签提取节点 |
| 7 | 代码执行节点 |
| 8 | 工具节点 |
| 9 | 逻辑判断节点 |
| 10 | 回复节点/消息节点 |
| 11 | 选项卡节点 |
| 12 | 循环节点 |
| 13 | 意图识别节点 |
| 14 | 工作流节点 |
| 15 | 插件节点 |
| 16 | 结束节点 |
