# Remnawave 账号创建工具

快速创建 Remnawave 账号并自动发送开通邮件。

## 快速开始

### 1. 配置

确保以下配置文件已正确设置：

- `~/.openclaw/workspace/config/remnawave.json` - Remnawave API 配置
- `~/.openclaw/workspace/config/smtp.json` - SMTP 邮件配置
- `~/.openclaw/workspace/config/remnawave-squads.json` - 内部组映射
- `~/.openclaw/workspace/config/email-templates/remnawave-account-created.md` - 邮件模板

### 2. 使用

```bash
cd ~/.openclaw/workspace/skills/remnawave-account-creator
node create-account.js \
  --username jim_pc \
  --email jim@codeforce.tech \
  --device-limit 1 \
  --traffic-gb 100 \
  --traffic-reset WEEKLY \
  --expire-days 365 \
  --squad "Ops Debugging" \
  --cc crads@codeforce.tech
```

### 3. 输出

```
🚀 开始创建 Remnawave 账号...

📋 账号信息:
  用户名：jim_pc
  邮箱：jim@codeforce.tech
  设备限制：1 台
  流量限制：100GB
  流量重置：WEEKLY
  过期时间：2027-03-08
  内部分组：Ops Debugging
  邮件抄送：crads@codeforce.tech

📡 调用 Remnawave API...
✅ 账号创建成功!

📋 账号详情:
  UUID: 2c337f97-968d-4a8a-a4a5-0715757df933
  短 UUID: J1RQJo3uq72bFb6k
  状态：ACTIVE
  VLESS UUID: 56764a35-173a-4707-871a-ac42c8e7b95f
  Trojan 密码：3YVP8Um3tAnH8j5EvtmE9cAtyd8sZQNc
  SS 密码：Masr7aHPFHkMZhP3-sdzSvWweokfyt4X
  订阅地址：https://46force235a-6cb1-crypto-link.datat.cc/api/sub/J1RQJo3uq72bFb6k

📧 准备发送开通邮件...
✅ 发送成功!
Message ID: <5efa5cfc-e978-dccf-ca64-5b3fc52fa363@codeforce.tech>

✅ 全部完成!
```

## 参数说明

| 参数 | 必填 | 默认值 | 说明 |
|------|------|--------|------|
| `--username` | ✅ | - | 账号用户名 |
| `--email` | ✅ | - | 用户邮箱 |
| `--device-limit` | ❌ | 1 | 设备限制数量 |
| `--traffic-gb` | ❌ | 100 | 流量限制 (GB) |
| `--expire-days` | ❌ | 365 | 过期天数 |
| `--squad` | ❌ | - | 内部分组名称 |
| `--cc` | ❌ | - | 邮件抄送地址 |

**注意：** Remnawave API 当前版本不支持流量重置策略，如需设置请在管理后台手动配置。

## ⚠️ 流量重置策略

**重要提示：** Remnawave API 当前版本不支持通过 API 设置流量重置策略。

如需设置流量重置，请在创建账号后：
1. 登录 Remnawave 管理后台
2. 找到对应用户
3. 手动编辑流量重置策略

或者运行更新命令（如果后续 API 支持）：
```bash
curl -k -X PATCH "https://8.212.8.43/api/users/{uuid}" \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"trafficResetInterval": "WEEKLY"}'
```

## 内部组名称

可用组名称（在 `remnawave-squads.json` 中配置）：

- `Default-Squad`
- `xray-default`
- `QA Engineer`
- `Front-end Developer`
- `TW`
- `Back-end Developer`
- `Ops Debugging`

## 邮件模板

邮件包含以下内容：

1. 证书安装教程链接
2. 订阅地址
3. 账号名称
4. 客户端下载地址
5. 单设备限制提醒

## 故障排查

### API 连接失败

检查 `remnawave.json` 配置：
- `apiBaseUrl` 是否正确
- `apiToken` 是否有效
- `sslRejectUnauthorized` 是否设置为 `false`（自签名证书）

### 邮件发送失败

检查 `smtp.json` 配置：
- SMTP 服务器地址和端口
- 邮箱账号和密码
- TLS 配置

### 组找不到

运行以下命令获取最新组列表：
```bash
curl -k -s "https://8.212.8.43/api/internal-squads" \
  -H "Authorization: Bearer YOUR_TOKEN" | jq '.'
```

## 许可证

私密技能 - 仅限作者使用

## 支持

联系：crads@codeforce.tech
