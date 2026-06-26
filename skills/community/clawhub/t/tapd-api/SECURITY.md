# 配置安全说明

## ⚠️ 重要提醒

**本 skill 中的所有配置示例都是虚拟数据，请勿直接使用！**

## 🔐 真实配置存放位置

### 推荐方式：使用 tapd.json

真实的 TAPD API 配置应存放在：

```
tapd.json
```

**不要将此文件提交到 Git！**

配置格式：

```json
{
  "oauth": {
    "clientId": "your-client-id",
    "clientSecret": "your-client-secret"
  },
  "workspaces": [
    {
      "id": "12345678",
      "name": "项目A",
      "default": true
    },
    {
      "id": "87654321",
      "name": "项目B"
    }
  ]
}
```

**安全设置**:
```bash
chmod 600 tapd.json
```

### 备选方式：环境变量

如果不想使用配置文件，可以设置环境变量：

```bash
export TAPD_CLIENT_ID="your-real-client-id"
export TAPD_CLIENT_SECRET="your-real-client-secret"
export TAPD_WORKSPACE_ID="your-workspace-id"
```

**注意**：环境变量优先级高于 tapd.json

## 🚫 不要做的事情

1. **不要**将 tapd.json 提交到 Git
2. **不要**在代码中硬编码真实凭证
3. **不要**在日志中打印敏感信息
4. **不要**将配置文件分享给未授权人员

## ✅ 安全建议

1. **使用** tapd.json 或环境变量存储真实配置
2. **添加** tapd.json 到 .gitignore
3. **设置**文件权限 `chmod 600 tapd.json`
4. **避免**硬编码凭证到代码中
5. **定期**轮换 OAuth 密钥
6. **启用** IP 白名单（在 TAPD 开放平台）
7. **监控** API 调用日志

## 📝 .gitignore 配置

```gitignore
# TAPD 配置文件
tapd.json
tapd-*.json

# Token 缓存
.tapd_token_cache.json

# Python cache
__pycache__/
*.pyc
```

## 🔍 检测敏感信息

在提交代码前，检查是否包含敏感信息：

```bash
# 检测真实凭证
grep -rE "tapd-app-[0-9]+" . --include="*.md" --include="*.json"
grep -rE "[A-F0-9]{8}-[A-F0-9]{4}-" . --include="*.md" --include="*.json"

# 检测真实 workspace_id
grep -rE "[0-9]{8,}" . --include="*.md" --include="*.json"
```

## 🔄 定期轮换密钥

1. 登录 TAPD 开放平台: https://open.tapd.cn
2. 进入应用管理
3. 重置应用密钥
4. 更新 tapd.json 中的 clientSecret
5. 测试新密钥是否生效

## 📋 安全检查清单

在部署前检查：

- [ ] tapd.json 已添加到 .gitignore
- [ ] 文件权限设置为 600
- [ ] 没有硬编码凭证
- [ ] OAuth 应用权限最小化
- [ ] 已设置 IP 白名单（可选）
- [ ] 已启用审计日志
- [ ] 团队成员知道不要提交配置文件

## 🛡️ 防泄露措施

### 1. Git Hooks

创建 `.git/hooks/pre-commit`：

```bash
#!/bin/bash
# 防止提交敏感文件

if git diff --cached --name-only | grep -q "tapd.json"; then
    echo "❌ 错误: 不允许提交 tapd.json"
    echo "请将其添加到 .gitignore"
    exit 1
fi
```

```bash
chmod +x .git/hooks/pre-commit
```

### 2. 自动检测脚本

```bash
#!/bin/bash
# 检测敏感信息

echo "🔍 检测敏感信息..."

# 检测真实凭证模式
if grep -rE "tapd-app-[0-9]+" . --include="*.md" --include="*.json" --exclude-dir=node_modules; then
    echo "⚠️  发现真实 clientId"
fi

if grep -rE "[A-F0-9]{8}-[A-F0-9]{4}-" . --include="*.md" --include="*.json" --exclude-dir=node_modules; then
    echo "⚠️  发现真实 clientSecret"
fi

echo "✅ 检测完成"
```

---

**记住**: 安全第一！真实凭证永远不要提交到 Git。
