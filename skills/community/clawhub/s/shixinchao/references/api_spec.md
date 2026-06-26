# 测试-史新超 API 接口规范

## 概览

测试-史新超 提供的 API 接口，支持流式对话

## 接口定义

### 1. 文件上传接口（可选）

如果需要在对话中使用文件，需要先通过此接口上传文件。

#### 基本信息

- **请求方法**：POST
- **请求路径**：`https://developer.jointpilot.com/v1/api/async_chat/api_upload_file/`
- **内容类型**：multipart/form-data
- **授权方式**：Bearer Token

#### 请求头

```text
Authorization: Bearer xxx
Content-Type: multipart/form-data
```

#### 请求参数

| 参数名 | 位置 | 类型 | 必选 | 说明 |
|--------|------|------|------|------|
| Authorization | header | string | 是 | Bearer xxx |
| file | form-data | file | 是 | 要上传的文件 |

#### 请求示例

```json
POST https://developer.jointpilot.com/v1/api/async_chat/api_upload_file/
Authorization: Bearer xxx
Content-Type: multipart/form-data

{
    "file": "<binary file data>"
}
```

#### 响应格式

```json
{
    "error_code": 0,
    "data": {
        "file_url": "https://chat-web-cdn.jfh.com/doc/api_upload_file/file.docx"
    }
}
```

上传成功后，将返回的 `file_url` 和 `file_name` 组成 JSON 对象，在对话接口的 `variables.api_file` 参数中使用：

```json
{
    "file_url": "https://example.com/path/to/uploaded/file.pdf",
    "file_name": "file.pdf"
}
```

---

### 2. 对话接口

#### 基本信息

- **请求方法**：POST
- **请求路径**：`https://developer.jointpilot.com/v1/api/async_chat/completions/`
- **内容类型**：application/json
- **授权方式**：Bearer Token

### 请求头

```text
Authorization: Bearer xxx
Content-Type: application/json
```

## 请求参数

### 参数说明

| 参数名 | 位置 | 类型 | 必选 | 说明 |
|--------|------|------|------|------|
| Authorization | header | string | 是 | Bearer xxx |
| chatId | body | string | 是 | 会话ID，使用随机生成的字符串 |
| stream | body | boolean | 是 | 是否流式输出，建议 true |
| detail | body | boolean | 是 | 是否返回中间值，建议 false |
| variables | body | object | 是 | 执行变量对象 |
| messages | body | array | 是 | 消息数组 |

### 完整请求示例

```json
{
    "chatId": "n517lJ90hXbYnyyv7G",
    "stream": true,
    "detail": false,
    "variables": {},
    "messages": [
        {
            "dataId": "n517lJ90hjY5aGSXbYnyyv7G",
            "role": "user",
            "content": [
                {
                    "type": "text",
                    "text": {
                        "content": "问题"
                    }
                }
            ]
        }
    ]
}
```

## 响应格式

### 流式响应

响应采用 Server-Sent Events (SSE) 格式，每行格式为：

```text
data: {json_data}
```

### 响应数据结构

```json
{
    "id": "example-id",
    "object": "",
    "created": 1726041710,
    "model": "",
    "choices": [
        {
            "delta": {
                "role": "assistant",
                "content": "答案内容"
            },
            "index": 0,
            "finish_reason": null
        }
    ],
    "type": "str"
}
```

## 错误处理

### 常见错误码

- **400**：请求参数错误
- **401**：认证失败（API Key 无效）
- **403**：权限不足
- **500**：服务器内部错误

### 错误响应格式

```json
{
    "error": {
        "code": "invalid_request_error",
        "message": "错误描述信息"
    }
}
```

## 注意事项

1. chatId 必须使用随机生成的字符串
2. stream 模式下需要正确处理 SSE 格式
3. 建议设置合理的超时时间（如 60 秒）
4. 凭证通过 Authorization 头传递，格式为 `Bearer xxx`
