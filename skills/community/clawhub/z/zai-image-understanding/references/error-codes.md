# Z.ai API 错误码对照表

## HTTP 状态码映射

| HTTP 状态码 | 错误类型 | 说明 | 是否可重试 | 处理建议 |
|------------|----------|------|-----------|----------|
| 200 | - | 成功 | - | 正常处理响应 |
| 400 | BAD_REQUEST | 请求参数错误 | 否 | 检查请求参数格式、图片 URL、提示词长度 |
| 401 | UNAUTHORIZED | 未授权/Token 无效 | 否 | 检查 API Key 是否正确、是否过期 |
| 403 | FORBIDDEN | 权限不足 | 否 | 检查账户余额、模型调用权限、IP 白名单 |
| 429 | RATE_LIMIT | 请求过于频繁 | **是** | 读取 Retry-After 头，等待后重试 |
| 500 | INTERNAL_ERROR | 服务器内部错误 | **是** | 指数退避重试，记录请求 ID 联系支持 |
| 502 | BAD_GATEWAY | 网关错误 | **是** | 指数退避重试 |
| 503 | SERVICE_UNAVAILABLE | 服务暂不可用 | **是** | 指数退避重试，关注状态页 |
| 504 | GATEWAY_TIMEOUT | 网关超时 | **是** | 增加客户端超时时间，重试 |

## 业务错误码（error.code 字段）

| 错误码 | 含义 | 原因 | 处理建议 |
|--------|------|------|----------|
| `INVALID_API_KEY` | API Key 无效 | Key 错误、已撤销、格式错误 | 重新生成 API Key，检查复制粘贴 |
| `API_KEY_EXPIRED` | API Key 过期 | Key 超过有效期 | 在控制台生成新 Key |
| `INSUFFICIENT_BALANCE` | 余额不足 | 账户余额为 0 或负数 | 充值账户余额 |
| `MODEL_NOT_FOUND` | 模型不存在 | model 参数错误 | 确认使用 `glm-4.1v-thinking-flash` |
| `MODEL_UNAVAILABLE` | 模型暂不可用 | 模型维护、下线、配额用尽 | 稍后重试，关注公告 |
| `INVALID_IMAGE_URL` | 图片 URL 无效 | URL 格式错误、不可访问、需登录 | 检查 URL 可公网访问、格式正确 |
| `IMAGE_TOO_LARGE` | 图片过大 | 超过 5MB 限制 | 压缩图片或使用更小分辨率 |
| `IMAGE_RESOLUTION_EXCEEDED` | 分辨率超限 | 超过 6000×6000 像素 | 调整图片尺寸 |
| `IMAGE_FORMAT_UNSUPPORTED` | 格式不支持 | 非 JPG/PNG/JPEG 格式 | 转换为支持格式 |
| `IMAGE_COUNT_EXCEEDED` | 图片数量超限 | 单次请求超过 1 张图片 | 每次请求仅发送 1 张图片 |
| `BASE64_NOT_SUPPORTED` | 不支持 Base64 | 使用了 data URI 或 Base64 编码 | **必须使用公网 URL** |
| `PROMPT_TOO_LONG` | 提示词过长 | 超过模型上下文限制 | 精简提示词，分批处理 |
| `CONTEXT_LENGTH_EXCEEDED` | 上下文长度超限 | 图片+文本 token 超过模型最大值 | 减小图片分辨率、缩短提示词 |
| `CONTENT_FILTER` | 内容安全过滤 | 图片或提示词触发安全策略 | 调整内容，避免敏感内容 |
| `RATE_LIMIT_EXCEEDED` | 超过速率限制 | QPS/TPM/并发超配额 | 实施客户端限流、排队重试 |
| `QUOTA_EXHAUSTED` | 配额耗尽 | 日/月调用量超套餐限制 | 升级套餐或等待配额重置 |
| `INTERNAL_SERVER_ERROR` | 内部服务错误 | 模型推理服务异常 | 记录 request_id，重试，联系技术支持 |
| `TIMEOUT` | 处理超时 | 模型推理耗时过长 | 增加超时设置，简化任务 |

## 客户端错误处理策略

### 重试策略

```python
import time
import random

def retry_with_backoff(
    func,
    max_retries: int = 2,
    base_delay: float = 1.0,
    max_delay: float = 30.0,
    retryable_codes: set = None
):
    """
    指数退避重试装饰器
    
    Args:
        max_retries: 最大重试次数
        base_delay: 基础延迟秒数
        max_delay: 最大延迟秒数
        retryable_codes: 可重试的错误码集合
    """
    if retryable_codes is None:
        retryable_codes = {
            "RATE_LIMIT_EXCEEDED",
            "INTERNAL_SERVER_ERROR", 
            "TIMEOUT",
            "SERVICE_UNAVAILABLE",
            "BAD_GATEWAY"
        }
    
    for attempt in range(max_retries + 1):
        try:
            return func()
        except APIError as e:
            if attempt == max_retries:
                raise
            
            if e.code not in retryable_codes:
                raise
            
            # 计算退避时间（指数退避 + 抖动）
            delay = min(base_delay * (2 ** attempt), max_delay)
            jitter = random.uniform(0, delay * 0.1)
            time.sleep(delay + jitter)
```

### 错误分类处理

```python
def handle_api_error(error: APIError) -> dict:
    """统一错误处理，返回用户友好的错误信息"""
    
    # 认证类错误 - 不可重试，需用户干预
    if error.code in {"INVALID_API_KEY", "API_KEY_EXPIRED"}:
        return {
            "user_message": "API Key 无效或已过期，请在 Z.ai 控制台重新生成",
            "action": "update_api_key",
            "retryable": False
        }
    
    # 余额/权限类 - 不可重试，需用户充值/升级
    if error.code in {"INSUFFICIENT_BALANCE", "QUOTA_EXHAUSTED", "MODEL_UNAVAILABLE"}:
        return {
            "user_message": f"账户问题：{error.message}，请前往控制台处理",
            "action": "check_account",
            "retryable": False
        }
    
    # 图片相关 - 不可重试，需用户更换图片
    if error.code in {
        "INVALID_IMAGE_URL", "IMAGE_TOO_LARGE", "IMAGE_RESOLUTION_EXCEEDED",
        "IMAGE_FORMAT_UNSUPPORTED", "IMAGE_COUNT_EXCEEDED", "BASE64_NOT_SUPPORTED"
    }:
        return {
            "user_message": f"图片问题：{error.message}，请检查图片 URL、大小、格式",
            "action": "fix_image",
            "retryable": False
        }
    
    # 参数错误 - 不可重试，需修正请求
    if error.code in {"PROMPT_TOO_LONG", "CONTEXT_LENGTH_EXCEEDED", "MODEL_NOT_FOUND"}:
        return {
            "user_message": f"请求参数错误：{error.message}",
            "action": "fix_request",
            "retryable": False
        }
    
    # 安全过滤 - 不可重试，需调整内容
    if error.code == "CONTENT_FILTER":
        return {
            "user_message": "内容触发安全过滤，请调整图片或提示词",
            "action": "adjust_content",
            "retryable": False
        }
    
    # 可重试错误 - 系统层面自动重试
    if error.code in {"RATE_LIMIT_EXCEEDED", "INTERNAL_SERVER_ERROR", "TIMEOUT"}:
        return {
            "user_message": "服务暂时繁忙，正在自动重试...",
            "action": "auto_retry",
            "retryable": True
        }
    
    # 未知错误 - 记录日志，允许重试
    return {
        "user_message": f"未知错误：{error.message} (code: {error.code})",
        "action": "contact_support",
        "retryable": True
    }
```

## 调试建议

### 必须记录的请求信息
- `request_id` (响应头 `X-Request-ID` 或响应体 `id`)
- 完整请求 payload（脱敏 API Key）
- 响应状态码、响应体
- 客户端时间戳、耗时

### 常见问题排查清单

| 现象 | 排查项 |
|------|--------|
| 401 Unauthorized | API Key 正确性、复制完整性、账户状态 |
| 403 Forbidden | 余额>0、模型权限、IP 白名单、企业认证状态 |
| 400 Bad Request | JSON 格式、字段名拼写、图片 URL 可访问性、Base64 误用 |
| 429 Too Many Requests | 并发数、QPS 限制、是否有批量任务未限流 |
| 图片分析失败 | URL 公网可访问、<5MB、<6000×6000、JPG/PNG、非 Base64 |
| 结果质量差 | 提示词明确性、输出格式指定、few-shot 示例、任务分解 |
| 超时 | 客户端 timeout≥60s、图片下载速度、模型负载高峰期 |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.0 | 2026-07-29 | 初始版本 |

---

> **注意**：错误码以官方文档为准，本表为常见错误码汇总。实际集成时请以 API 返回的 `error.code` 为准，并实现兜底的未知错误处理。