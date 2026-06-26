# 部署指南 — 通用内容审核 Skill

## 系统要求

| 项目 | 要求 |
|------|------|
| 操作系统 | macOS / Linux |
| Python | >= 3.9 |
| curl | 系统自带即可 |
| VPN | L2TP/IPsec 已配置（参考 `共用工具/vpn-l2tp`） |

## 快速部署

### 1. 配置 VPN

参考 `共用工具/vpn-l2tp` 的部署指南，确保 VPN 已连接且 `ppp0` 接口可用。

```bash
# 验证 VPN 接口
ifconfig ppp0

# 验证站点可达
curl --interface ppp0 -4 -sS -o /dev/null -w "%{http_code}" https://staff.你的站点.com
# 应返回 200 或 302
```

### 2. 安装 Python 依赖

```bash
# 基本使用（仅用本地规则）— 无需额外安装，Python 标准库即可

# 如果要启用技术部审核 API（可选）
pip install requests
```

### 3. 准备凭据

| 需要什么 | 从哪里获取 | 说明 |
|----------|-----------|------|
| **后台地址** | 你们组的后台管理员 | 如 `https://staff.xxx.com` |
| **用户名/密码** | 后台管理员分配 | 你登录后台用的账号密码 |
| **TOTP seed** | 后台管理员分配账号时提供 | Base32 格式字符串（如 `JBSWY3DPEHPK3PXP`）。就是你第一次绑定验证器（Google Authenticator 等）时扫的那个密钥。如果只有手机验证器里的动态码，需要找给你开账号的管理员要原始 seed |
| **模块名** | 自己从浏览器地址栏获取 | 登录后台 → 进入审核页面 → 看 URL（见下方说明） |

> **关于 TOTP seed：** 这是一串 Base32 编码的密钥，你绑定手机验证器时用过它。如果当时没有单独保存，需要找后台管理员重新获取或重置。脚本需要这个原始密钥来自动生成验证码，只有手机 App 里的6位动态码是不够的。

### 4. 创建配置文件

```bash
cp config.example.json config.json
```

编辑 `config.json`，填入必填项：

| 字段 | 必填 | 说明 | 示例 |
|------|------|------|------|
| `site.base_url` | 是 | 后台地址 | `https://staff.xxx.com` |
| `site.module` | 是 | 审核模块名 | `info` / `infovip` / `post` |
| `auth.username` | 是 | 后台用户名 | `admin` |
| `auth.password` | 是 | 后台密码 | `123456` |
| `auth.totp_seed` | 是 | TOTP 密钥 | `JBSWY3DPEHPK3PXP` |
| `moderation.content_fields` | 否 | 送审字段 | `["title", "content"]` |
| `moderation.api_key` | 否 | 技术部 API 密钥（不填也能用） | `sk-proj-xxx` |

### 5. 确定你的模块名

登录后台，进入审核页面，观察浏览器地址栏：

```
https://staff.xxx.com/d.php/admin/info/list
                                    ^^^^
                                    这就是模块名
```

常见模块名：

| 模块名 | 对应业务 |
|--------|---------|
| `info` | 资源/帖子审核 |
| `infovip` | VIP 资源审核 |
| `post` | 动态/帖子审核 |
| `comments` | 评论审核 |
| `memberupdatelog` | 用户资料变更审核 |

### 6. 确定送审字段

在后台审核页面，用浏览器 DevTools（F12 → Network）查看 `listAjax` 接口返回的数据，找到包含内容的字段名：

```json
{
  "data": [
    {
      "id": 123,
      "title": "这是标题",
      "content": "这是内容",
      "status": 1
    }
  ]
}
```

将字段名填入 `moderation.content_fields`：

```json
"content_fields": ["title", "content"]
```

### 7. 适配审核规则（可选）

`rules.json` 内置了通用审核规则，开箱即用。如果需要调整：

- **启用/禁用规则**：修改 `"enabled": true/false`
- **修改匹配词**：编辑 `"patterns"` 中的正则
- **添加新规则**：按现有格式添加新条目
- **让 AI 帮改**：把 `rules.json` 内容发给 Claude，说明你们的审核标准，让它帮你改

### 8. 验证安装

```bash
# dry-run 模式：拉取、判断，但不提交结果
python review.py --config config.json --dry-run

# 检查输出：
#   - 登录成功
#   - 待审总量显示
#   - 每条内容有 PASS/REJECT 判定
```

确认无误后，去掉 `--dry-run` 正式运行。

## 接口风格适配

大多数站点使用路径风格（默认配置已适配）：

```
/d.php/admin/{module}/listAjax
/d.php/admin/{module}/verifyStatus
```

如果你的站点使用查询参数风格，修改 `endpoints`：

```json
"endpoints": {
  "login_page": "/d.php?mod=login&code=login",
  "login_submit": "/d.php?mod=login&code=dologin",
  "fetch": "/d.php?mod={module}&code=listAjax",
  "submit": "/d.php?mod={module}&code=verifyStatus"
}
```

同时检查登录字段名：

```json
"login_fields": {
  "username_field": "username",
  "password_field": "password",
  "totp_field": "card_num"
}
```

## 故障排查

| 问题 | 原因 | 解决 |
|------|------|------|
| `curl 失败` | VPN 未连接或 ppp0 不存在 | 检查 VPN 连接：`ifconfig ppp0` |
| `登录失败` | 用户名/密码/TOTP 错误 | 检查 auth 配置；确认系统时钟准确（TOTP 有30秒窗口） |
| `非 JSON 响应` | 站点返回 HTML（未登录或接口不对） | 检查 endpoints 是否匹配站点风格 |
| `不允许重复审核` | 条目已被其他人处理 | 正常现象，自动跳过 |
| 误判太多 | 规则太严或太松 | 修改 rules.json 调整规则 |
