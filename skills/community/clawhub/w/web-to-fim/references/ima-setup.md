# 腾讯 ima 笔记 API 配置指南

> ⚠️ **重要说明**：ima 是腾讯提供的**云端笔记服务**，通过 API 接口创建和管理笔记，**不需要安装本地客户端**。只需获取 API 凭证即可使用。

## 获取凭证

### 步骤 1: 访问 ima 开放平台

打开 [ima.qq.com/agent-interface](https://ima.qq.com/agent-interface)

### 步骤 2: 登录并获取凭证

1. 使用 QQ 或微信扫码登录
2. 在「Agent 接口」页面获取凭证：
   - **Client ID**: 应用标识
   - **Api Key**: API 密钥

### 步骤 3: 复制凭证

登录后页面会显示你的凭证，格式类似：

```text
Client ID: xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
Api Key: ima_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx
```

## 本地配置

### 设置环境变量

```bash
# Windows PowerShell
$env:IMA_CLIENT_ID="your_client_id"
$env:IMA_API_KEY="your_api_key"

# Linux/macOS
export IMA_CLIENT_ID="your_client_id"
export IMA_API_KEY="your_api_key"
```

### 验证配置

```python
from scripts.ima_client import IMAClient

client = IMAClient()
if client.test_connection():
    print("✅ ima 连接成功")
else:
    print("❌ ima 连接失败，请检查凭证")
```

## ima API 功能概览

| 功能 | API 端点 | 说明 |
|------|----------|------|
| 测试连接 | `GET /v1/notebook/list` | 验证凭证是否有效 |
| 创建笔记 | `POST /v1/note/create` | 在默认笔记本创建新笔记 |
| 更新笔记 | `POST /v1/note/update` | 向现有笔记追加内容 |
| 读取笔记 | `GET /v1/note/get` | 获取笔记详情 |
| 搜索笔记 | `POST /v1/note/search` | 按关键词搜索笔记 |

## API 基础信息

- **API 地址**: `https://ima.im.qq.com/openapi`
- **认证方式**: Client-ID + Api-Key 请求头
- **数据格式**: JSON
- **无需本地客户端**: 所有操作通过云端 API 完成

## 安全注意事项

⚠️ **重要提示**：
- **Api Key 等同于密码**，不要泄露给他人
- 永远不要将真实凭证提交到 Git
- 已在 `.gitignore` 中添加 `.env` 规则
- 定期轮换 Api Key

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| `401 Unauthorized` | 检查 Client ID 和 Api Key 是否正确 |
| `403 Forbidden` | 确保 ima 开发者权限已开通 |
| `rate_limit_exceeded` | API 有调用频率限制，等待后重试 |
| 网络超时 | 检查网络连接，或使用代理 |
