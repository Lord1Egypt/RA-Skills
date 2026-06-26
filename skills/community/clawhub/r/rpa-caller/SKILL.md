---
name: rpa-caller
description: 通过 HTTP 请求调用 RPA 自动化功能，让机器人完成指定任务。
  当用户提到「RPA」「自动化」「机器人执行」「让机器人帮我」「自动填表」「自动点击」
  「批量处理」「自动化流程」「运行任务」「触发流程」等词时，必须使用此 skill。
  适用场景：触发 RPA 任务、查询任务状态、停止任务、传参数给 RPA 流程。
---

# RPA HTTP 调用 Skill

本 Skill 让 Claude 能够通过 HTTP 请求调用 RPA 系统，完成各类自动化任务。
RPA 功能清单和对应 API 定义在 `references/rpa-api-map.xlsx` 中，使用前必须先读取。

---

## 核心工作流程

### Step 1：理解用户意图
明确用户想让 RPA 完成什么任务，例如：
- "帮我自动填写报销单"
- "批量下载这些文件"
- "打开系统并录入数据"

### Step 2：查找对应 RPA 功能
从 Excel 功能清单（`references/rpa-api-map.xlsx`）中查找：
- 匹配用户意图的功能名称
- 对应的 HTTP Method 和 Endpoint
- 必填参数 / 可选参数
- 预期返回结果

如果找不到匹配功能，告知用户并列出所有可用功能供其选择。

### Step 3：收集必填参数
根据功能清单，向用户确认所有必填参数。例如：
- 目标文件路径
- 要填写的数据内容
- 时间范围
- 目标系统账号（如需要）

对于敏感参数（密码、token），提示用户注意安全，避免明文存储。

### Step 4：构建 HTTP 请求
```
Method: [GET / POST / PUT / DELETE]
URL: {BASE_URL}{endpoint}
Headers:
  Content-Type: application/json
  Authorization: Bearer {API_KEY}   ← 如功能清单中有鉴权要求
Body (JSON):
{
  "task_id": "唯一任务ID（可用时间戳）",
  "params": {
    // 根据功能清单填入具体参数
  }
}
```

### Step 5：展示请求并确认
在执行前，以结构化方式展示完整的请求内容，请用户确认后再发送。

示例展示格式：
```
📋 即将调用 RPA 功能：【批量下载文件】

接口：POST http://localhost:8088/api/rpa/download-files
参数：
  - source_dir: /data/reports/2024/
  - file_pattern: *.pdf
  - dest_dir: /output/

是否确认执行？
```

### Step 6：发起请求并处理响应
发起请求后，根据响应状态给出反馈：

| 响应状态 | 处理方式 |
|---------|---------|
| 200 / 任务提交成功 | 告知任务ID，提示如何查询状态 |
| 202 Accepted | 异步任务已接受，等待执行 |
| 400 参数错误 | 列出错误字段，引导用户修正 |
| 401 / 403 鉴权失败 | 提示检查 API_KEY 或权限 |
| 404 接口不存在 | 检查 BASE_URL 和 endpoint 是否正确 |
| 500 服务端错误 | 建议检查 RPA 服务是否正常运行 |
| 超时 / 无响应 | 建议检查 RPA 服务的连接状态 |

### Step 7：任务状态追踪（如支持）
如果功能清单中有状态查询接口，主动提示用户可以查询执行进度：
```
任务已提交！Task ID: rpa_20240315_143022
可以告诉我「查询任务状态」来追踪执行进度 🤖
```

---

## 全局配置（首次使用时设置）

使用本 Skill 前，需要确认以下配置信息：

```
BASE_URL:  http://your-rpa-server:8088   ← RPA 服务地址
API_KEY:   your-api-key-here             ← 鉴权 Token（如有）
```

如果用户没有提供，主动询问这两个值，并在对话中记住它们。

---

## 常用功能速查

> 以下为示例，实际功能以 Excel 功能清单为准

| 用户说 | 对应功能 |
|--------|---------|
| 帮我填表 / 录入数据 | data-entry |
| 下载文件 / 批量下载 | file-download |
| 截图 / 截取屏幕 | screenshot |
| 打开网页 / 访问系统 | open-browser |
| 查询任务进度 | task-status |
| 停止任务 | task-stop |

---

## 注意事项

1. **安全**：不要在对话中明文显示完整的密码或高权限 Token
2. **幂等性**：每次请求使用唯一 task_id（建议用时间戳）避免重复执行
3. **异步任务**：大多数 RPA 任务是异步的，提交后需要轮询状态接口
4. **错误重试**：网络错误可以重试，但业务逻辑错误需要修正参数后再试
5. **日志**：建议用户在 RPA 系统侧开启日志，便于排查问题

---

## 参考文件

- `references/rpa-api-map.xlsx` — RPA 功能清单，包含所有接口定义和参数说明
- 如需新增功能，按 Excel 模版格式填写后告知 Claude 重新加载
