# Token 配置指南

本文档详细说明如何获取和配置大虾皮 API Token。

## 获取 Token

### 步骤 1：注册账号

1. 访问 [daxiapi.com](https://daxiapi.com)
2. 注册并登录账号

### 步骤 2：获取 Token

1. 登录后进入「会员中心」
2. 找到「API 管理」或「API Token」入口
3. 开通 API Token 功能
4. 复制生成的 Token

---

## 配置 Token

### 方式一：CLI 配置（推荐）

```bash
# 设置 Token
npx daxiapi-cli@latest config set token YOUR_TOKEN_FROM_DAXIAPI

# 验证配置
npx daxiapi-cli@latest config get token
```

**优点**：
- 配置持久化存储
- 无需每次设置环境变量
- 适合长期使用

---

### 方式二：环境变量

```bash
# Linux/macOS
export DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI

# Windows
set DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI
```

**优点**：
- 无需本地文件存储
- 适合 CI/CD 环境
- 适合临时使用

---

### 方式三：.env 文件

在项目根目录创建 `.env` 文件：

```
DAXIAPI_TOKEN=YOUR_TOKEN_FROM_DAXIAPI
```

---

## 验证配置

```bash
# 测试命令
npx daxiapi-cli@latest zdt --type zt
```

**成功标志**：返回正常的涨停股数据

**失败标志**：
- `401 Unauthorized`：Token 无效或未配置
- `Authentication failed`：认证失败

---

## 常见问题

### Q: Token 在哪里查看？

A: 登录 [daxiapi.com](https://daxiapi.com) 个人主页，在「会员中心」→「API 管理」中查看。

### Q: Token 有效期多久？

A: 根据订阅方案不同，请参考大虾皮官网说明。

### Q: Token 泄露怎么办？

A: 立即在大虾皮官网重新生成 Token，并更新本地配置。

### Q: 多台电脑如何使用？

A: 在每台电脑上执行相同的配置步骤即可。

---

## 安全建议

1. **不要提交 Token 到 Git 仓库**
   - 将 `.env` 添加到 `.gitignore`
   - 不要在代码中硬编码 Token

2. **定期更换 Token**
   - 建议每隔一段时间重新生成 Token

3. **权限最小化**
   - 只授予必要的 API 访问权限

---

## 相关文档

- [CLI 命令参考](cli-commands.md)
- [字段说明](field-descriptions.md)
