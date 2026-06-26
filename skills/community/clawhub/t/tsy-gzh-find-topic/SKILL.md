---
description: 调用后端接口，获取公众号爆款选题推荐，直接输出原始 data。
allowed-tools: WebFetch
---

## 职责

只做两件事：

1. 调用 `POST {BASE_URL}/gzh/findTopic`
2. 原样输出响应中的 `data` 字段

**禁止**：分析、改写、补充、总结或二次加工任何内容。

---

## 启动前处理

**参数解析优先级**：

1. `BASE_URL`：优先读取 `.env` 全局配置中的 `TSY_API_URL`
2. 若 `TSY_API_URL` 不存在或为空，回退为固定值 `https://api.tangshiye.cn`
3. `SATOKEN`：只读取 `.env` 全局配置中的 `TSY_API_KEY`

若 `SATOKEN` 未找到，则终止并提示用户在 `.env` 中补充 `TSY_API_KEY`。

---

## 执行步骤

### 第一步：生成请求体

运行以下脚本，将其**标准输出**作为请求体：
```bash
python3 scripts/generate_request_body.py
```

脚本须输出合法 JSON，字段规则如下：

| 字段 | 类型 | 规则                                    |
|------|------|---------------------------------------|
| `likeOutlierValue` | string | 固定值 `"3"`                             |
| `publishStartDate` | string | 当前时间往前推 30 天，取当日 00:00:00 的**毫秒级**时间戳 |
| `publishEndDate` | string | 当前时间的**毫秒级**时间戳                       |

输出示例：
```json
{
  "likeOutlierValue": "3",
  "publishStartDate": "1707148800000",
  "publishEndDate": "1709740800000"
}
```

> 若脚本执行失败或输出非法 JSON，终止并输出错误原因。

### 第二步：发起请求
```http
POST {BASE_URL}/gzh/findTopic?apikey={SATOKEN}
Content-Type: application/json

<第一步输出的 JSON>
```

---

## 输出规则

按以下顺序判断，命中即输出并终止：

1. **HTTP 状态码 ≠ 200** → 输出 HTTP 错误信息
2. **响应体 `code` 非成功状态** → 输出接口返回的错误信息
3. **成功** → 仅输出 `data` 字段的原始内容，不附加任何内容
