# 服务商对比

## 百炼（Bailian）

**服务商：** 阿里云  
**适用场景：** 国内搜索  
**环境变量：** `BAILIAN_API_KEY`（或 `DASHSCOPE_API_KEY`）  
**特点：**
- 中文优化，搜索速度快
- 支持时效筛选、站点限定
- 策略模式：turbo（快速）、max（平衡）、agent（深度）
- answer 质量高，但 sources 列表当前测试中未返回

**获取密钥：** https://dashscope.aliyun.com/

---

## Tavily

**服务商：** Tavily AI  
**适用场景：** 海外搜索  
**环境变量：** `TAVILY_API_KEY`  
**特点：**
- 专为 AI 设计，结果质量高
- 自动提取答案和来源
- 支持 30 天时效筛选
- 自带 answer 摘要和 sources

**获取密钥：** https://tavily.com/

---

## 火山引擎联网搜索（Volcengine Search）

**服务商：** 字节跳动  
**适用场景：** 国内搜索  
**环境变量：** `WEB_SEARCH_API_KEY`  
**API 端点：** `https://open.feedcoopapi.com/search_api/web_search`  
**特点：**
- 每月 500 次免费额度（Agent Plan 用户）
- 支持权威过滤（`auth_level`）、时间范围（`time_range`）
- 返回来源站点名称、权威度信息
- 同时支持 API Key 和 AK/SK 认证

**获取密钥：**
- 个人用户：[联网搜索控制台](https://console.volcengine.com/search-infinity/api-key)
- Agent Plan 用户：[Agent Plan 控制台](https://console.volcengine.com/ark/region:ark+cn-beijing/openManagement?LLM=%7B%7D&advancedActiveKey=agentPlan)

### ⚠️ 密钥不通用

火山引擎有三种 key，互不通用：

| Key 类型 | 格式示例 | 用途 | 能否用于本 skill |
|----------|----------|------|-----------------|
| **联网搜索 API Key** | `<web-search-token>` | 联网搜索专用 | ✅ |
| **agentplan key** | `ark-<agentplan-token>` | Agent Plan 聊天 | ❌ |
| **通用 ARK API Key** | `ark-<token>` | 模型推理 + 搜索工具 | ❌ |

> v1.x 版本曾尝试通过 `/api/v3/responses` 端点使用 Ark API Key 调用搜索，但该端点需要通用 ARK API Key（非 agentplan），且不支持联网搜索专用 Key。v2.0 改用 `open.feedcoopapi.com` 专用搜索 API，兼容性更好。

---

## 搜索强度对比

| 强度 | 国内搜索 | 海外搜索 | 耗时 |
|------|----------|----------|------|
| quick | 火山引擎 | Tavily | ~2s |
| normal | 百炼 + 火山引擎 | Tavily + 火山引擎 | ~4s |
| deep | 百炼 + 火山引擎 + Tavily | 百炼 + 火山引擎 + Tavily | ~6s |
