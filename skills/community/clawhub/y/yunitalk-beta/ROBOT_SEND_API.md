# Talk Robots 机器人消息发送接口

本文档说明 OpenClaw 通过 Talk Robots `/robot/send` 向与你聊聊机器人投递消息的方式，覆盖文本消息和文件消息两类请求。

`/robot/send` 的语义是把事件投递给目标机器人；机器人是否最终向会话回复，由机器人脚本决定。

## 推荐调用方式

优先使用本 Skill 内置脚本 `shell/robot_send.sh`。脚本会自动生成 `msg_id`、`noncestr`、`timestamp` 和 HMAC-SHA256 `sign`，避免业务侧重复实现签名逻辑。

### 发送文本

```bash
./shell/robot_send.sh text \
  --base-url "$TALK_ROBOT_ENDPOINT" \
  --robot-id "$TALK_ROBOT_ID" \
  --robot-key "$TALK_ROBOT_KEY" \
  --content "你好，任务已经处理完成。"
```

### 发送文件

```bash
./shell/robot_send.sh file \
  --base-url "$TALK_ROBOT_ENDPOINT" \
  --robot-id "$TALK_ROBOT_ID" \
  --robot-key "$TALK_ROBOT_KEY" \
  --content "请查看附件" \
  --file "./report.pdf"
```

### 发送前预检

使用 `--dry-run` 可以查看签名 URL 和请求体，不会实际发送消息。

```bash
./shell/robot_send.sh text \
  --base-url "$TALK_ROBOT_ENDPOINT" \
  --robot-id "$TALK_ROBOT_ID" \
  --robot-key "$TALK_ROBOT_KEY" \
  --content "测试消息" \
  --dry-run
```

脚本常用参数：

| 参数 | 必填 | 说明 |
|------|------|------|
| `--base-url` | 是 | Talk Robots `/v1/robot/send` 地址，即 `TALK_ROBOT_ENDPOINT` |
| `--robot-id` | 是 | 机器人 ID |
| `--robot-key` | 是 | 机器人 Key，用于签名 |
| `--cvs-id` | 否 | 可选目标会话 ID，应保持大小写原样；不传时默认投递到机器人与创建者的点对点会话 |
| `--content` | 文本必填，文件可选 | 文本消息内容，或文件说明文本 |
| `--file` | 文件必填 | 待上传文件路径 |
| `--refer-msg-id` | 否 | 引用的消息 ID |
| `--msg-id` | 否 | 指定消息 ID；不传时脚本自动生成 |
| `--noncestr` | 否 | 指定随机串；不传时脚本自动生成 |
| `--timestamp` | 否 | 指定 Unix 秒级时间戳；不传时脚本自动生成 |
| `--at` | 否 | 文本消息的 `at_uid_list`，多个 UID 用英文逗号分隔 |
| `--mentioned` | 否 | 文本消息的 `mentioned_list`，多个 UID 用英文逗号分隔 |
| `--dry-run` | 否 | 只打印请求信息，不实际发送 |

## 直接使用 curl

不使用 `shell/robot_send.sh` 时，可以直接用 `curl` 调用 `/robot/send`。完整的签名生成、文本消息和文件消息示例见：

- [ROBOT_SEND_CURL_API.md](./ROBOT_SEND_CURL_API.md) - 机器人消息 curl 调用示例

## 接口总览

**请求方法**：`POST`

**基础地址**：`{robot_endpoint}`

`robot_endpoint` 通常来自 `TALK_ROBOT_ENDPOINT`，例如：

```text
https://api-talk.yuniapp.cn/v1/robot/send
```

**鉴权参数**放在 URL 查询参数中：

| 参数 | 必填 | 说明 |
|------|------|------|
| `robot_id` | 是 | 机器人 ID |
| `noncestr` | 是 | 请求随机串 |
| `timestamp` | 是 | Unix 秒级时间戳 |
| `msg_id` | 是 | 消息 ID；请求体或表单中的 `msg_id` 必须与 URL 中一致 |
| `sign` | 是 | 使用 `robot_key` 计算得到的 HMAC-SHA256 签名 |

完整 URL 形态：

```text
{robot_endpoint}?robot_id={robot_id}&noncestr={nonce}&timestamp={timestamp}&msg_id={msg_id}&sign={sign}
```

## 签名规则

签名参数为 `msg_id`、`noncestr`、`robot_id`、`timestamp`。生成 `sign` 时：

1. 按参数 key 字典序排序。
2. 每个 value 使用 URL encode。
3. 按 `key=value` 拼接，并用 `&` 连接。
4. 使用 `robot_key` 对签名原文做 HMAC-SHA256。
5. 将结果编码为小写十六进制字符串。

签名原文示例：

```text
msg_id=<msg_id>&noncestr=<noncestr>&robot_id=<robot_id>&timestamp=<timestamp>
```

Shell 示例：

```bash
signing_text="msg_id=${msg_id}&noncestr=${noncestr}&robot_id=${robot_id}&timestamp=${timestamp}"
sign="$(printf '%s' "$signing_text" | openssl dgst -sha256 -hmac "$robot_key" | awk '{print $2}')"
```

实际实现时，`signing_text` 里的 value 需要先 URL encode。推荐直接使用 `shell/robot_send.sh`。

## 发送文本消息

文本消息使用 `application/json`，请求体是完整 `imx.Msg` JSON 结构，`cmd` 固定为 `msg`，文本内容放在 `body.content`。

```http
POST {robot_endpoint}?robot_id={robot_id}&noncestr={nonce}&timestamp={timestamp}&msg_id={msg_id}&sign={sign}
Content-Type: application/json

{
  "cmd": "msg",
  "head": {
    "msg_id": "消息ID，需与 URL 中 msg_id 一致",
    "cvs_id": "可选，目标会话ID",
    "refer_msg_id": "可选，引用消息ID"
  },
  "body": {
    "content": "消息内容",
    "at_uid_list": ["可选，被 @ 的用户 ID"],
    "mentioned_list": ["可选，兼容企业微信类命名"]
  }
}
```

字段说明：

| 字段 | 必填 | 说明 |
|------|------|------|
| `cmd` | 是 | 固定为 `msg` |
| `head.msg_id` | 是 | 消息 ID，需与 URL 查询参数 `msg_id` 一致 |
| `head.cvs_id` | 否 | 可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话 |
| `head.refer_msg_id` | 否 | 引用消息 ID |
| `body.content` | 是 | 文本、Markdown 或文件说明 |
| `body.at_uid_list` | 否 | @ 用户列表 |
| `body.mentioned_list` | 否 | 兼容企业微信类命名的提及列表 |

`curl` 示例：

```bash
curl -X POST "$request_url" \
  -H "Content-Type: application/json" \
  --data-binary '{
    "cmd": "msg",
    "head": {
      "msg_id": "'"$msg_id"'"
    },
    "body": {
      "content": "你好，任务已经处理完成。"
    }
  }'
```

## 发送文件消息

文件消息使用 `multipart/form-data`，文件内容必须通过 `file` 字段上传，不要用 JSON 传文件二进制内容。

```http
POST {robot_endpoint}?robot_id={robot_id}&noncestr={nonce}&timestamp={timestamp}&msg_id={msg_id}&sign={sign}
Content-Type: multipart/form-data

msg_id: 消息ID，需与 URL 中 msg_id 一致
cvs_id: 可选，目标会话ID
file: <二进制文件内容>
content: <可选，文件说明文本>
refer_msg_id: <可选，引用消息ID>
```

表单字段说明：

| 字段 | 必填 | 说明 |
|------|------|------|
| `msg_id` | 是 | 消息 ID，需与 URL 查询参数 `msg_id` 一致 |
| `cvs_id` | 否 | 可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话 |
| `file` | 是 | 待上传文件 |
| `content` | 否 | 文件说明文本 |
| `refer_msg_id` | 否 | 引用消息 ID |

`curl` 示例：

```bash
curl -X POST "$request_url" \
  -F "msg_id=$msg_id" \
  -F "content=请查看附件" \
  -F "file=@./report.pdf"
```

服务端会把 multipart 文件转换为机器人消息中的 `file_list`，并把文件内容编码为 `data:<content-type>;base64,<payload>` 后投递给目标机器人脚本。

## 响应

成功响应：

```json
{
  "success": true,
  "message": "ok"
}
```

常见失败响应：

| HTTP 状态码 | message | 说明 |
|-------------|---------|------|
| `400` | `签名参数错误` | 缺少签名查询参数 |
| `400` | `签名错误` | `sign` 校验失败 |
| `400` | `msg_id 错误` | 请求体或表单中的 `msg_id` 与 URL 中不一致 |
| `400` | `参数格式错误` | JSON 结构或字段格式不合法 |
| `400` | `文件处理错误` | multipart 文件读取失败 |
| `400` | `参数错误` | 投递给机器人时参数不符合要求 |
| `404` | `机器人不存在` | `robot_id` 不存在 |
| `500` | `内部错误` | 服务端处理异常 |

## 注意事项

1. `TALK_ROBOT_KEY` 是敏感信息，不要写入日志、提交到仓库或回显给用户。
2. `cvs_id` 是可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话，传入时保持大小写不变。
3. 文本消息使用 JSON，文件消息使用 multipart，不要混用。
4. `msg_id` 是本次投递的幂等标识之一，URL 和请求体中的值必须一致。
5. `/robot/send` 只表示事件已投递给目标机器人，不保证机器人脚本一定会回复。
