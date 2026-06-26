# API Key 配置

## 获取 API Key

1. 访问 [image.open-idea.net](https://image.open-idea.net)
2. 注册并登录账号
3. 进入「API Key」页面创建新的 Key
4. 复制 Key 并配置到客户端

## 配置环境变量

```bash
IMAGE_GATEWAY_API_KEY=你的APIKey
```

## 验证 Key

```bash
curl -X POST https://image.open-idea.net/api/v1/image \
  -H "Authorization: Bearer <YOUR_API_KEY>" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "一只在草地上打滚的柯基",
    "width": 2048,
    "height": 2048
  }'
```

返回图片生成结果或计费错误即为 Key 生效。

## Key 管理

- 每个用户可创建多个 API Key
- 可在后台撤销不再使用的 Key
- 新注册用户赠送免费额度
