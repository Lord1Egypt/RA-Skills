# 飞书云文档 API 配置指南

## 获取凭证

### 步骤 1: 创建飞书应用

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 登录后进入「开发者后台」
3. 点击「创建应用」，填写应用名称和描述
4. 获取 **App ID** 和 **App Secret**

### 步骤 2: 配置权限

在应用后台开启以下权限：

| 权限名称 | 权限说明 | 必要性 |
|---------|---------|--------|
| `docx.document:readonly` | 读取云文档 | 可选 |
| `docx.document:write` | 创建/编辑云文档 | 必须 |
| `drive:drive:folder` | 云文档文件夹操作 | 必须 |
| `sheets:Spreadsheet:readonly` | 读取表格 | 可选 |

### 步骤 3: 发布应用

1. 在「版本管理与发布」中创建版本
2. 选择「发布」并等待审核（或自建企业直接通过）

## 本地配置

### 设置环境变量

```bash
# Windows PowerShell
$env:FEISHU_APP_ID="your_app_id"
$env:FEISHU_APP_SECRET="your_app_secret"

# Linux/macOS
export FEISHU_APP_ID="your_app_id"
export FEISHU_APP_SECRET="your_app_secret"
```

### 验证配置

```python
from feishu_client import FeishuClient

client = FeishuClient()
if client.test_connection():
    print("✅ 飞书连接成功")
else:
    print("❌ 飞书连接失败，请检查凭证")
```

## 安全注意事项

⚠️ **重要提示**：
- **永远不要**将 `.env` 文件或包含真实凭证的文件提交到 Git
- 已在 `.gitignore` 中添加 `.env` 规则
- 生产环境建议使用密钥管理服务（如 AWS Secrets Manager）

## 故障排查

| 问题 | 解决方案 |
|------|---------|
| `invalid_app_id` | 检查 App ID 是否正确 |
| `app_secret` 错误 | 在飞书开放平台重置 App Secret |
| 权限不足 | 在应用后台添加所需权限并重新发布 |
| 签名校验失败 | 确保使用 HTTPS，检查时间戳是否正确 |
