# HTTP 请求参考

## 生成图片

```bash
curl -X POST https://image.open-idea.net/api/v1/image \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一幅宁静的草原风景",
    "width": 2048,
    "height": 2048,
    "style": "写实摄影，电影级光影",
    "image_count": 1
  }'
```

**响应（成功 201）：**

```json
{
  "success": true,
  "data": {
    "images": [
      "<base64 PNG data>"
    ],
    "width": 2048,
    "height": 2048,
    "style": "写实摄影，电影级光影",
    "image_count": 1,
    "points_used": 56
  },
  "billing": {
    "charged": 0.56,
    "balance": 0.44,
    "currency": "CNY"
  }
}
```

**响应头：**
- `X-Mengguyu-Billing-Currency: CNY`
- `X-Mengguyu-Billing-Charged: 0.560000`
- `X-Mengguyu-Billing-Balance: 0.440000`

## 错误响应

| HTTP 状态码 | 说明 |
|---|---|
| 400 | 参数错误（如 prompt 为空） |
| 401 | 未授权（API Key 无效） |
| 403 | API Key 权限不足 |
| 402 | 余额不足 |
| 429 | 超出日限额 |
| 502 | 上游服务错误 |

## 尺寸错误响应

当尺寸不在支持列表中时，接口返回 `422`：

```json
{
  "error": {
    "message": "当前模型仅支持 2K 及以上的推荐尺寸组合，例如 2048x2048、2304x1728、2848x1600。",
    "type": "invalid_request_error",
    "code": "invalid_image_size"
  }
}
```
