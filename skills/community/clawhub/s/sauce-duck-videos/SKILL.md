---
name: sauce-duck-videos
description: 生成多国语言版的酱板鸭搞笑梗视频。当用户想要生成酱板鸭视频、制作多语言酱板鸭搞笑梗视频、或使用RunningHub生成搞笑类视频时，使用此Skill。支持英语、韩语、泰语、法语等多种语言版本。
metadata:
  {
    "openclaw":
      {
        "requires": { "bins": ["python"] }
      },
  }
---

# 酱板鸭视频生成器

本Skill用于调用RunningHub平台的工作流，生成多国语言版本的酱板鸭搞笑梗视频。

### 第一步：获取环境变量

运行以下脚本获取配置：

```bash
python scripts/get_env.py
```
获取json返回的 `host` 和 `api_key` 字段。

### 第二步：设置RH_HOST

如果`host`的值为空字符串或为 `null`，先询问用户选择服务器：
- 国内服务器（www.runninghub.cn）
- 国外服务器（www.runninghub.ai）

根据用户选择将`host`更新为对应的地址，调用对应脚本保存`host`地址：

```bash
python scripts/config_host.py --set "www.runninghub.cn"
```
或
```bash
python scripts/config_host.py --set "www.runninghub.ai"
```

### 第三步：设置API Key

如果`api_key`的值为空字符串或为 `null`，询问用户输入在`host`网站创建的API Key，根据用户的输入将`api_key`更新为对应的值，然后调用对应脚本保存`api_key`值：

```bash
python scripts/config_api_key.py --set "{{api_key}}"
```

### 第四步：选择语言

提示用户输入想要生成的语言版本，支持几十种语言（如英语、韩语、泰语、法语、德语、西班牙语等），并验证输入是否为有效语言。

## API调用流程

### 第五步：创建工作流任务

使用脚本创建任务：

```bash
python scripts/create_task.py "{{host}}" "{{api_key}}" "{{语言}}"
```

### 第六步：处理创建响应

解析脚本返回的JSON数据：

**成功响应示例：**
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "netWssUrl": null,
    "taskId": "1910246754753896450",
    "clientId": "e825290b08ca2015b8f62f0bbdb5f5f6",
    "taskStatus": "QUEUED",
    "promptTips": "{\"result\": true, \"error\": null, \"outputs_to_execute\": [\"9\"], \"node_errors\": {}}"
  }
}
```

- 如果`code`为0：
  - 提取`taskId`和`taskStatus`
  - 进行第七步后台生成视频

- 如果`code`不为0：
  - 从`msg`字段读取错误信息
  - 告知用户生成失败的原因
  - 退出skill

### 第七步：后台生成视频

使用 OpenClaw exec 工具在后台启动视频生成脚本：

```json
{"tool": "exec", "command": "python scripts/poll_task.py \"{{host}}\" \"{{api_key}}\" \"{{taskId}}\" 5", "background": true}
```

温柔地告知用户："酱板鸭视频正在后台生成中，大概需要3分钟时间，生成完成后会自动发送给你哦～先去喝杯咖啡吧☕️"

从 exec 返回结果中提取 `sessionId` 字段。**重要：必须立即执行第八步查询任务状态，不要停止对话！**

### 第八步：查询任务状态

使用 OpenClaw process 工具查询后台任务状态：

```json
{"tool": "process", "action": "poll", "sessionId": "{{sessionId}}"}
```

从 process 返回的完整输出内容中直接解析 JSON 结果（格式见下方响应示例）。

**可能的状态响应：**

1. **超时（TIMEOUT）**
```json
{
    "status": "TIMEOUT",
    "errorCode": "TIMEOUT",
    "errorMessage": "轮询超时，已等待1200秒，任务仍在运行中",
    "taskId": "xxx"
}
```
- 告知用户任务仍在生成中，但视频生成脚本已超时未完成，建议稍后手动查询taskId `xxx`的状态

2. **失败（FAILED）**
```json
{
    "taskId": "2009194900306137089",
    "status": "FAILED",
    "errorCode": "1000",
    "errorMessage": "unknown error",
    "results": null,
    "clientId": "",
    "promptTips": ""
}
```
- 分析`errorMessage`
- 告知用户失败原因

3. **成功（SUCCESS）**
```json
{
    "taskId": "2009191190196789249",
    "status": "SUCCESS",
    "errorCode": "",
    "errorMessage": "",
    "results": [
        {
            "url": "xxx",
            "outputType": "mp4"
        }
    ],
    "clientId": "",
    "promptTips": ""
}
```
- 从`results[0].url`获取视频URL
- 调用`message`工具，将视频URL和文字发送给用户：
  - `message`: "亲爱的，你的酱板鸭视频已经生成好啦～快看看吧～🎬"
  - `media`: 视频URL

### 第九步：清除后台会话

使用 OpenClaw process 工具从内存中清除已结束的会话：

```json
{"tool": "process", "action": "clear"}
```

## 辅助脚本（可选）

### 重新设置API Key

如果用户想要重新设置`api_key`，询问用户输入在`host`网站创建的新API Key，根据用户输入将`api_key`进行更新，并调用对应脚本保存`api_key`值：

```bash
python scripts/config_api_key.py --set "{{api_key}}"
```

### 重新设置RH_HOST

如果用户想要重新设置`host`地址：

- 国内服务器（www.runninghub.cn）
- 国外服务器（www.runninghub.ai）

根据用户选择将`host`更新为对应的地址，并调用脚本保存`host`地址：

```bash
python scripts/config_host.py --set "www.runninghub.cn"
```
或
```bash
python scripts/config_host.py --set "www.runninghub.ai"
```

### 单独查询任务状态

如果需要单独查询任务状态（不轮询）：

```bash
python scripts/query_task.py "{{host}}" "{{api_key}}" "{{taskId}}"
```
