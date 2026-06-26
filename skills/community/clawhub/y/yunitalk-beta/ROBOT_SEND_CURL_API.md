# Talk Robots 机器人消息 curl 调用示例

本文档说明不使用 `shell/robot_send.sh` 时，如何直接用 `curl` 调用 Talk Robots `/robot/send` 投递文本消息和文件消息。

示例依赖 `curl`、`openssl` 和 `python3`。

## 准备公共变量

```bash
TALK_ROBOT_ENDPOINT="https://api-talk.yuniapp.cn/v1/robot/send"
TALK_ROBOT_ID="your-robot-id"
TALK_ROBOT_KEY="your-robot-key"
# 可选：指定目标会话；不设置时默认投递到机器人与创建者的点对点会话
TALK_ROBOT_CVS_ID=""
```

字段说明：

| 变量 | 说明 |
|------|------|
| `TALK_ROBOT_ENDPOINT` | Talk Robots `/v1/robot/send` 地址 |
| `TALK_ROBOT_ID` | 机器人 ID |
| `TALK_ROBOT_KEY` | 机器人 Key，用于 HMAC-SHA256 签名 |
| `TALK_ROBOT_CVS_ID` | 可选目标会话 ID，传入时必须保持大小写原样；不传时默认投递到机器人与创建者的点对点会话 |

## 生成签名 URL

```bash
timestamp="$(date +%s)"
msg_id="msg_${timestamp}_$(python3 -c 'import uuid; print(uuid.uuid4().hex)')"
noncestr="nonce_${timestamp}_$(python3 -c 'import uuid; print(uuid.uuid4().hex)')"

urlencode() {
  python3 -c 'import sys, urllib.parse; print(urllib.parse.quote_plus(sys.argv[1]))' "$1"
}

signing_text="msg_id=$(urlencode "$msg_id")&noncestr=$(urlencode "$noncestr")&robot_id=$(urlencode "$TALK_ROBOT_ID")&timestamp=$(urlencode "$timestamp")"
sign="$(printf '%s' "$signing_text" | openssl dgst -sha256 -hmac "$TALK_ROBOT_KEY" | awk '{print $2}')"

request_url="${TALK_ROBOT_ENDPOINT}?robot_id=$(urlencode "$TALK_ROBOT_ID")&noncestr=$(urlencode "$noncestr")&timestamp=$(urlencode "$timestamp")&msg_id=$(urlencode "$msg_id")&sign=$(urlencode "$sign")"
```

签名原文由 `msg_id`、`noncestr`、`robot_id`、`timestamp` 按 key 字典序排序后拼接，且每个 value 都需要先 URL encode：

```text
msg_id=<msg_id>&noncestr=<noncestr>&robot_id=<robot_id>&timestamp=<timestamp>
```

## curl 发送文本消息

文本消息使用 `application/json`，请求体是完整 `imx.Msg` JSON 结构，`cmd` 固定为 `msg`，文本内容放在 `body.content`。

```bash
curl -sS -X POST "$request_url" \
  -H "Content-Type: application/json" \
  --data-binary "$(python3 - <<PY
import json

payload = {
    "cmd": "msg",
    "head": {
        "msg_id": "${msg_id}"
    },
    "body": {
        "content": "你好，任务已经处理完成。"
    }
}
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
PY
)" \
  -w '\nHTTP_STATUS=%{http_code}\n'
```

带引用消息的文本请求：

```bash
REFER_MSG_ID="source-msg-id"

curl -sS -X POST "$request_url" \
  -H "Content-Type: application/json" \
  --data-binary "$(python3 - <<PY
import json

payload = {
    "cmd": "msg",
    "head": {
        "msg_id": "${msg_id}",
        "refer_msg_id": "${REFER_MSG_ID}"
    },
    "body": {
        "content": "这是引用回复。"
    }
}
print(json.dumps(payload, ensure_ascii=False, separators=(",", ":")))
PY
)" \
  -w '\nHTTP_STATUS=%{http_code}\n'
```

## curl 发送文件消息

文件消息使用 `multipart/form-data`，文件内容必须通过 `file` 字段上传，不要用 JSON 传文件二进制内容。

```bash
curl -sS -X POST "$request_url" \
  -F "msg_id=$msg_id" \
  -F "content=请查看附件" \
  -F "file=@./report.pdf" \
  -w '\nHTTP_STATUS=%{http_code}\n'
```

带引用消息的文件请求：

```bash
curl -sS -X POST "$request_url" \
  -F "msg_id=$msg_id" \
  -F "refer_msg_id=source-msg-id" \
  -F "content=请查看附件" \
  -F "file=@./report.pdf" \
  -w '\nHTTP_STATUS=%{http_code}\n'
```

## 响应示例

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
| `404` | `机器人不存在` | `robot_id` 不存在 |
| `500` | `内部错误` | 服务端处理异常 |

## 注意事项

1. `TALK_ROBOT_KEY` 是敏感信息，不要写入日志、提交到仓库或回显给用户。
2. `msg_id` 必须同时出现在 URL 查询参数和请求体或表单中，并保持一致。
3. `cvs_id` 是可选目标会话 ID；不传时默认投递到机器人与创建者的点对点会话，传入时保持大小写不变。
4. 文本消息使用 JSON，文件消息使用 multipart，不要混用。
5. `/robot/send` 只表示事件已投递给目标机器人，不保证机器人脚本一定会回复。
