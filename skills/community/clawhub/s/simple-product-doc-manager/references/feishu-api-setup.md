# 飞书文档 API 配置完整指南：从 0 到可编辑

> 本文档记录 LReview 项目配置飞书文档管理的完整流程，供团队新人参考

---

## 一、背景与目标

### 1.1 为什么要配置飞书文档 API？

在 AI 时代，我们希望 OpenClaw 能够：
- **自动创建**项目文档（需求文档、技术文档、配置文档等）
- **自动更新**文档内容（同步代码变更、记录会议纪要等）
- **统一管理**产品文档（版本控制、权限管理、协作编辑）

### 1.2 核心挑战

飞书开放平台提供了丰富的 API，但配置过程涉及多个环节，容易踩坑：
- 应用创建与权限配置
- OAuth 授权流程
- Token 获取与管理
- 文档所有权与编辑权限

### 1.3 两种身份模式

| 维度 | 应用身份（tenant_access_token） | 用户身份（user_access_token） |
|-----|-------------------------------|------------------------------|
| **文档所有者** | 应用本身（机器人账号） | 用户本人 |
| **用户能否编辑** | ❌ 不能，需要申请权限 | ✅ 能，直接编辑 |
| **使用场景** | 团队共享文档、自动化流程 | **个人知识库、需要人工编辑** |
| **权限开通** | 应用身份权限 | 用户身份权限 |

**关键决策**：如果希望用户能在飞书客户端直接编辑文档，必须使用 **user_access_token** 模式。

---

## 二、前置准备

### 2.1 注册飞书开放平台账号

1. 访问 [飞书开放平台](https://open.feishu.cn/)
2. 使用企业邮箱注册开发者账号
3. 完成实名认证（个人或企业）

### 2.2 创建自建应用

1. 登录飞书开放平台
2. 点击右上角 **"开发者后台"**
3. 点击 **"创建企业自建应用"**
4. 填写应用信息：
   - 应用名称：例如 "OpenClaw 助手"
   - 应用描述：AI 助手用于管理项目文档
   - 应用头像：上传一个图标

5. 记录 **App ID** 和 **App Secret**
   - 位置：开发配置 → 凭证与基础信息
   - **App Secret 只会显示一次，务必保存好**

---

## 三、权限配置（关键步骤）

### 3.1 开通用户身份权限

进入应用后台 → **权限管理** → **API 权限** → 搜索并添加以下权限：

| 权限名称 | 权限标识 | 说明 |
|---------|---------|------|
| 访问新版文档 | `docx:document` | 读取文档内容 |
| 创建新版文档 | `docx:document:create` | 创建新文档 |
| 编辑新版文档 | `docx:document:write_only` | 修改文档内容 |
| 访问云空间 | `drive:drive` | 管理云空间文件 |
| 访问知识库 | `wiki:wiki` | 读取知识库内容 |
| 创建知识空间 | `wiki:space` | 创建知识库（可选）|

**重要**：
- 必须选择 **"用户身份"** 类型的权限
- 不要选择 "应用身份" 权限（除非有特殊需求）
- 每个权限点击后选择 **"申请权限"**

### 3.2 配置网页授权（OAuth）

进入 **安全设置** → **网页授权配置**：

1. **添加重定向 URL**：
   ```
   http://localhost:3000/callback
   ```
   - 这是 OAuth 授权后的回调地址
   - 开发阶段使用 localhost，生产环境使用实际域名

2. **配置 IP 白名单**（可选）：
   - 添加你的服务器 IP，提高安全性

### 3.3 添加测试用户

**重要**：未发布的应用只能被测试用户授权使用。

1. 进入 **应用发布** → **版本管理与发布**
2. 创建测试版本（填写版本号、更新说明）
3. 点击 **"测试授权"** → **"添加测试用户"**
4. 输入你的飞书账号（手机号或邮箱）
5. 确认添加

---

## 四、获取 user_access_token

### 4.1 构造授权链接

使用以下格式构造授权链接（注意 scope 用**空格**分隔）：

```
https://open.feishu.cn/open-apis/authen/v1/authorize?
  app_id=cli_你的AppID
  &redirect_uri=http://localhost:3000/callback
  &response_type=code
  &scope=docx:document docx:document:create drive:drive
```

**参数说明**：
- `app_id`：你的应用 ID
- `redirect_uri`：必须与后台配置完全一致
- `response_type`：固定值 `code`
- `scope`：申请的权限列表，**用空格分隔**

**常见错误**：
- ❌ `scope=docx:document,docx:document:create`（用逗号）
- ✅ `scope=docx:document docx:document:create`（用空格）

### 4.2 用户授权获取 code

1. **打开授权链接**：在浏览器中访问构造好的链接
2. **登录飞书账号**：使用你的个人飞书账号登录
3. **确认授权**：查看申请的权限列表，点击"授权"
4. **获取 code**：授权后会跳转到：
   ```
   http://localhost:3000/callback?code=xxxxxxxx&state=...
   ```
   从 URL 中提取 `code` 参数（只取 code 值，不要后面的 &state）

**注意**：code 有效期很短（几分钟），获取后要立即使用。

### 4.3 换取 user_access_token

使用以下 API 调用换取 token：

```bash
curl -X POST "https://open.feishu.cn/open-apis/authen/v1/access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_你的AppID",
    "app_secret": "你的AppSecret",
    "grant_type": "authorization_code",
    "code": "上一步获取的code",
    "redirect_uri": "http://localhost:3000/callback"
  }'
```

**重要**：`app_id` 和 `app_secret` 放在请求 body 中，不是放在 Header 的 Basic Auth 中。

**返回示例**：
```json
{
  "code": 0,
  "data": {
    "access_token": "u-7YAewM3Y12bVmJ9rIPQGlBkl1.ugg5WXOwEaFQA02ASb",
    "refresh_token": "ur-71UTe8a0N3QWCQLyFIR4L7kl1YYgg5gjMgEaZMM02BCe",
    "expires_in": 6900,
    "refresh_expires_in": 2591700,
    "open_id": "ou_cbcc27fa7979db72b850c0cf97c03ca6",
    "user_id": "bc955bb2",
    "name": "尹世超",
    "mobile": "+8615982402562"
  }
}
```

**关键字段**：
- `access_token`：用户访问令牌，用于调用 API（有效期约 2 小时）
- `refresh_token`：刷新令牌，用于获取新的 access_token（有效期 30 天）
- `expires_in`：access_token 有效期（秒）
- `open_id`：用户在应用内的唯一标识

---

## 五、使用 user_access_token

### 5.1 创建文档

```bash
curl -X POST "https://open.feishu.cn/open-apis/docx/v1/documents" \
  -H "Authorization: Bearer u-你的access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "文档标题"
  }'
```

**返回示例**：
```json
{
  "code": 0,
  "data": {
    "document": {
      "document_id": "Gd8idaE9EoEx2SxuMLwcBD7knQg",
      "revision_id": 1,
      "title": "文档标题"
    }
  }
}
```

### 5.2 访问文档

文档链接格式：
```
https://你的域名.feishu.cn/docx/文档ID
```

例如：
```
https://f7z3q8b5lu.feishu.cn/docx/Gd8idaE9EoEx2SxuMLwcBD7knQg
```

**特点**：
- 文档所有者是你的个人账号
- 可以在飞书客户端直接编辑
- 可以分享给其他人协作

---

## 六、Token 刷新与管理

### 6.1 为什么要刷新？

- `access_token` 有效期只有 2 小时（6900 秒）
- 过期后需要重新获取，频繁授权体验差
- 使用 `refresh_token` 可以静默刷新，无需用户操作

### 6.2 刷新 access_token

```bash
curl -X POST "https://open.feishu.cn/open-apis/authen/v1/refresh_access_token" \
  -H "Content-Type: application/json" \
  -d '{
    "app_id": "cli_你的AppID",
    "app_secret": "你的AppSecret",
    "grant_type": "refresh_token",
    "refresh_token": "ur-你的refresh_token"
  }'
```

**返回**：新的 `access_token` 和 `refresh_token`

### 6.3 自动刷新策略

建议实现自动刷新机制：
- 在 token 过期前（如过期前 10 分钟）自动刷新
- 或者定期刷新（如每 7 天刷新一次）
- 保存新的 `refresh_token`，因为每次刷新都会生成新的

---

## 七、常见问题与解决方案

### 7.1 错误码 20043 - scope 有误

**原因**：scope 参数格式错误
**解决**：使用空格分隔，不要用逗号

### 7.2 错误码 20025 - missing app id or app secret

**原因**：API 调用方式错误
**解决**：将 `app_id` 和 `app_secret` 放在请求 body 中，不要用 Basic Auth

### 7.3 错误码 99991663 - Invalid access token

**原因**：token 过期或格式错误
**解决**：重新获取 user_access_token

### 7.4 错误码 99991672 - Access denied

**原因**：权限未开通或类型不匹配
**解决**：检查权限管理，确保开通了正确的用户身份权限

### 7.5 授权后无法跳转到 localhost

**原因**：本地服务未启动
**解决**：
- 方案 1：先启动本地服务（如 Python Flask），再授权
- 方案 2：直接从浏览器地址栏复制 code，手动换取 token

---

## 八、最佳实践总结

### 8.1 配置 checklist

- [ ] 创建应用并记录 App ID 和 App Secret
- [ ] 开通用户身份权限（docx:document 等）
- [ ] 配置网页授权重定向 URL
- [ ] 创建测试版本并添加测试用户
- [ ] 构造授权链接（scope 用空格分隔）
- [ ] 获取 code 并换取 user_access_token
- [ ] 测试创建文档，确认所有者是个人账号

### 8.2 安全建议

- **妥善保管 App Secret**：不要硬编码在代码中，使用环境变量
- **定期刷新 token**：避免使用过期的 access_token
- **权限最小化原则**：只开通必要的权限
- **生产环境使用 HTTPS**：重定向 URL 使用 https 协议

### 8.3 团队协作建议

- 将配置流程文档化（本文档）
- 使用共享的测试应用，避免每个人重复配置
- 建立 token 管理机制（如使用密钥管理服务）

---

## 九、参考资源

- [飞书开放平台文档](https://open.feishu.cn/document/)
- [获取 user_access_token](https://open.feishu.cn/document/server-docs/authentication-management/access-token/obtain-user_access_token)
- [创建文档 API](https://open.feishu.cn/document/server-docs/docs/docs/docx-v1/document/create)
- [OAuth 错误码说明](https://open.feishu.cn/document/server-docs/authentication-management/access-token/faq)

---

## 十、实际案例：LReview 项目配置

### 应用信息
- **App ID**: `cli_a948e3ca9fb99bcc`
- **App Secret**: `1UakAZzxnrcp17qhH9R1FcRKOYJTp28S`

### 用户凭证（尹世超）
- **user_access_token**: `u-7YAewM3Y12bVmJ9rIPQGlBkl1.ugg5WXOwEaFQA02ASb`
- **refresh_token**: `ur-71UTe8a0N3QWCQLyFIR4L7kl1YYgg5gjMgEaZMM02BCe`
- **open_id**: `ou_cbcc27fa7979db72b850c0cf97c03ca6`

### 已创建文档
- 需求思考：https://f7z3q8b5lu.feishu.cn/docx/Gd8idaE9EoEx2SxuMLwcBD7knQg
- 项目地址和代码逻辑记录：https://f7z3q8b5lu.feishu.cn/docx/OcGPdIyIRo9Tg0xJZVzc8NP8nQf
- 配置信息记录：https://f7z3q8b5lu.feishu.cn/docx/Oa1VdsUaToayJKxXT41czJEanKf
- 产品需求文档索引：https://f7z3q8b5lu.feishu.cn/docx/Efw6dDOYIoJE7zxDw7Cc1twNn3d

---

*文档版本：v1.0*
*创建时间：2026-03-26*
*适用对象：团队新人*
