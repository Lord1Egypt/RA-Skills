# 安全策略

## Cookie 安全

知乎自动化 Skill 使用知乎账号 Cookie 进行操作，Cookie 的安全性至关重要。

### 加密存储

所有导出的 Cookie 使用 **AES-256-GCM** 算法加密存储：

```
加密流程：
  明文 Cookie
      ↓
  + AES-256-GCM 加密（随机 12 字节 IV）
      ↓
  密文 + IV + GCM 认证标签
      ↓
  写入 ~/.hermes/credentials/zhihu-cookies.enc（权限 0600）
```

- **加密算法**：AES-256-GCM（认证加密，防篡改）
- **密钥长度**：256 位（64 字符 hex）
- **IV**：每次加密生成随机 12 字节 IV
- **认证标签**：16 字节 GCM 认证标签
- **文件权限**：`0600`（仅文件所有者可读写）

### 密钥管理

```bash
# 生成密钥（建议添加到 ~/.zshrc 或 ~/.bashrc）
export ZHIHU_COOKIE_KEY="$(openssl rand -hex 32)"

# 密钥轮换
node -e "
const { rotateCookieKey } = require('./scripts/zhihu-core.js');
rotateCookieKey('新的_64字符_hex密钥').then(console.log);
"
```

### 安全注意事项

- **永远不要**将未加密的 Cookie 提交到版本控制系统
- **永远不要**将 `ZHIHU_COOKIE_KEY` 写在代码、提交信息或公开场合
- 不要在共享或公共计算机上长期保存 Cookie
- Cookie 有效期约 30 天，过期后应重新导出
- 如果怀疑密钥泄露，立即执行密钥轮换

---

## 环境变量管理建议

### 必需变量

| 变量 | 说明 |
|------|------|
| `ZHIHU_COOKIE_KEY` | Cookie AES-256-GCM 加密密钥（32 字节 hex） |

### 可选变量

| 变量 | 说明 | 安全级别 |
|------|------|:--------:|
| `ZHIHU_APP_KEY` | 知乎 OpenAPI app_key | 敏感 |
| `ZHIHU_APP_SECRET` | 知乎 OpenAPI app_secret | 敏感 |
| `ZHIHU_PROXY` | 代理地址（反爬场景） | 低 |
| `CAPTCHA_API_KEY` | 打码平台 API Key | 敏感 |

### 环境变量管理建议

1. **不要硬编码**：所有敏感配置通过环境变量传入，不要写在代码中
2. **使用 dotenv**：本地开发可用 `.env` 文件（已加入 `.gitignore`），切勿提交
3. **密钥轮换**：定期更换 `ZHIHU_COOKIE_KEY`，尤其是团队协作场景
4. **最小权限**：只赋予必要的环境变量，不要使用万能密钥

---

## 报告安全漏洞

如果你发现了安全漏洞，**请不要公开提交 Issue**。

请通过以下方式私下报告：

1. **GitHub Security Advisory**：
   访问 https://github.com/liuboacean/zhihu-automation-skill/security/advisories/new

2. **直接联系维护者**：
   通过 [GitHub Issues](https://github.com/liuboacean/zhihu-automation-skill/issues) 联系项目维护者

### 报告内容建议

- 漏洞类型和影响范围
- 复现步骤
- 受影响版本
- 建议的修复方案（可选）

### 响应承诺

- 收到报告后 **48 小时内**回复确认
- 评估后 **7 天内**给出修复时间计划
- 修复完成后公开致谢（征得报告人同意）

---

## 依赖供应链安全

- 核心依赖仅 3 个：`playwright`、`playwright-extra`、`puppeteer-extra-plugin-stealth`
- 所有依赖通过 `package-lock.json` 锁定版本
- 建议定期运行 `npm audit` 检查已知漏洞

---

## 安全更新

安全更新会标注 `security` 标签：

```
security(xxx): 修复 Cookie 泄露风险
```

建议开启 GitHub 仓库的 Watch → Custom → Security alerts 以接收安全更新通知。
