# 规则目录与匹配说明（yotta-secret 元钥）

本引擎用「正则 + 熵 + 格式校验」三层判定识别疑似密钥。本文档是规则目录与已知取舍，
源码实现见 scripts/yotta_secret.py 的 LINE_RULES / BLOCK_RULES。

## 判定流程

1. **正则命中**：按行（块级规则按全文）匹配候选密钥；
2. **值级校验**：
   - generic（高熵长 token）：排除纯十六进制哈希（32/40/64/128 位）、UUID、熵 < 4.0；
   - credential（凭据赋值）：排除占位符 / 示例值 / 环境变量引用；中等置信 key（token / auth_token）需更长或更高熵；
   - url_userinfo：排除 user / username / login 等占位账号；
   - basic_auth：base64 解码后必须含冒号（user:pass 形态）；
3. **去重**：同一文件同一行同一密钥只保留一条（严重度优先）；generic 与更具体规则重叠时让位。

## 类别与规则

### cloud（云厂商 / SaaS 密钥）

| rule_id | 名称 | 匹配示例 | 格式说明 |
|---|---|---|---|
| aws_access_key | AWS 访问密钥 ID | AKIA… / ASIA… | A3T/AKIA/AGPA/AIDA/AROA/AIPA/ANPA/ANVA/ASIA + 16 位大写字母数字 |
| aws_secret | AWS 秘密访问密钥 | aws_secret_access_key = … | 40 位 base64 形态值 |
| google_api | Google API Key | AIza… | AIza + 35 位 [0-9A-Za-z_-] |
| openai | OpenAI API Key | sk-… | sk- + 20+ 位（排除 sk-ant- 前缀） |
| anthropic | Anthropic API Key | sk-ant-… | sk-ant- + 20+ 位 |
| stripe | Stripe API Key | sk_live_… / pk_test_… | (sk|rk|pk)_(live|test)_ + 16+ 位 |
| slack | Slack Token | xoxb-… / xoxp-… | xox[baprs]- + 10+ 位 |
| github | GitHub Token | ghp_… / github_pat_… | gh[pousr]_ + 36+ 位；github_pat_ + 20+ 位 |
| gitlab | GitLab Token | glpat-… | glpat- + 20+ 位 |
| npm_token | npm Token | npm_… | npm_ + 36 位 |
| pypi_token | PyPI Token | pypi-AgEIcHlwaS5vcmc… | 固定前缀 + 50+ 位 |
| telegram_bot | Telegram Bot Token | 123456789:AA… | 8-10 位数字 + 冒号 + 35 位 |
| jwt | JWT | eyJ… | 三段 base64url（header.payload.signature） |
| huggingface | HuggingFace Token | hf_… | hf_ + 30+ 位 |
| notion | Notion Token | secret_… / ntn_… | secret_ + 40+ 位；ntn_ + 24+ 位 |
| shopify | Shopify Token | shpat_… | shpat_ + 32 位十六进制 |
| sendgrid | SendGrid API Key | SG.… | SG. + 22 位 + . + 43 位 |
| twilio | Twilio API Key | SK… | SK + 32 位十六进制 |
| mailgun | Mailgun API Key | key-… | key- + 32 位字母数字 |
| sendinblue | Sendinblue API Key | xkeysib-… | xkeysib- + 64 位十六进制 + - + 16 位 |
| digitalocean | DigitalOcean Token | dop_v1_… | dop_v1_ + 64 位十六进制 |
| pagerduty | PagerDuty Token | pdus_… | pdus_ + 20+ 位 |
| azure_storage | Azure 存储账户密钥 | AccountKey=… | 连接串中 AccountKey= + 80+ 位 base64 |
| bearer | Bearer Token | Authorization: Bearer … | bearer + 20+ 位 |
| basic_auth | HTTP Basic 认证 | Authorization: Basic … | base64 解码含冒号（user:pass） |

### private_key（私钥，severity = critical）

| rule_id | 名称 | 匹配形态 |
|---|---|---|
| pem_private | PEM 私钥块 | -----BEGIN (RSA |EC |DSA |OPENSSH |ENCRYPTED )?PRIVATE KEY----- … -----END …-----（跨行） |
| pgp_private | PGP 私钥块 | -----BEGIN PGP PRIVATE KEY BLOCK----- … -----END PGP PRIVATE KEY BLOCK----- |
| putty_ppk | PuTTY 私钥 | PuTTY-User-Key-File-2/3 + Private-Lines 段 |

### credential（凭据赋值，severity = high）

- 直接 key：password / passwd / pwd / secret / api_key / apikey / access_key / accesskey /
  auth_token / client_secret / client_key / private_key / consumer_key / consumer_secret /
  refresh_token / app_secret / secret_key / signing_key / session_token / db_password /
  root_password / admin_password / user_password / smtp_password / smtp_pass / ftp_password /
  redis_password / mysql_password / pg_password / mongo_password / proxy_password /
  encryption_key / master_key / webhook_secret / webhook_token / oauth_client_secret /
  id_token / access_token / _authToken / _password / auth_token / token
- 后缀式 key（MYAPP_SECRET= / GOOGLE_CLIENT_SECRET= 等）：<名字>_<key>，key ∈ password /
  passwd / pwd / secret / token / pass / key / api_key / access_key / auth_token /
  client_secret / private_key / refresh_token
- 值过滤：占位符 / 示例值 / 环境变量引用不算（见 entropy-and-verification.md）；
  值长度默认 >= 8（--min-length 可调）；token / auth_token 需 >= 16 位或熵 >= 3.5。

### url_userinfo（URL 内嵌凭据，severity = high）

- 协议：http / https / ftp / smtp / imap / imaps / pop3 / pop3s / ldap / ldaps /
  mongodb / mongodb+srv / redis / rediss / mysql / postgres / postgresql / mssql /
  amqp / amqps / jdbc:<子协议>
- 形态：scheme://user:password@host（报告 password；user 为 user/username/login 时跳过）。

### generic（高熵长 token，severity = medium）

- 匹配：32+ 位 [A-Za-z0-9+/=_-]；
- 值级校验：排除纯十六进制哈希（32/40/64/128 位）、UUID、熵 < 4.0；
- 与更具体规则重叠时让位（如 JWT 三段、ghp_ 前缀）。

## 已知取舍

- **可能漏报**：自定义前缀的私有密钥（可先用 verify 校验）；跨行拼接的长 token；
  加密密钥（无法靠正则识别的内容加密）。
- **可能误报**：base64 长文本块（medium 级，人工复核）；示例代码里的测试 key（已被占位符过滤大部分）。
- **不做**：不联网验证密钥是否有效、不查泄露库、不自动轮换、不做内容解密。
