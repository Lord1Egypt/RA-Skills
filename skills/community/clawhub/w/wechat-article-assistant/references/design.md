# WeChat Article Assistant Design

## Directory Structure

```text
wechat-article-assistant/
├─ SKILL.md
├─ agents/
│  └─ openai.yaml
├─ references/
│  ├─ design.md
│  ├─ sqlite-schema.md
│  └─ interface-reference.md
└─ scripts/
   ├─ wechat_article_assistant.py
   ├─ wechat_article_openclaw.py
   ├─ cli.py
   ├─ log_utils.py
   ├─ config.py
   ├─ database.py
   ├─ schema.py
   ├─ utils.py
   ├─ session_store.py
   ├─ openclaw_messaging.py
   ├─ mp_client.py
   ├─ login_service.py
   ├─ account_service.py
   ├─ article_service.py
   ├─ sync_service.py
   └─ dev/
      └─ smoke_test.py
```

## SQLite Tables

当前设计默认只维护一个有效的公众号平台登录态，不支持多账号并行登录。

- `settings`: 通用配置项扩展位
- `login_session`: 当前唯一公众号平台登录态
- `login_qrcode_session`: 二维码登录临时会话
- `proxy_config`: 代理配置，支持文章抓取和同步独立开关
- `account`: 本地维护的公众号列表
- `sync_config`: 外部定时任务读取的同步计划
- `article`: 文章元数据
- `article_detail`: 文章正文详情缓存与导出路径
- `sync_log`: 同步任务日志

## Tool / Command Catalog

### 登录与会话

- `login-start`
- `login-poll`
- `login-wait`
- `login-import`
- `login-info`
- `login-clear`

### 代理配置

- `proxy-set`
- `proxy-show`

### 公众号管理

- `search-account`
- `resolve-account-url`
- `add-account`
- `add-account-by-keyword`
- `add-account-by-url`
- `list-accounts`
- `delete-account`

### 同步配置与同步执行

- `list-sync-targets`
- `set-sync-target`
- `sync`
- `sync-all`
- `sync-due`
- `sync-logs`

### 文章查询与导出

- `list-account-articles`
- `recent-articles`
- `article-detail`

### 诊断

- `doctor`

## Script Interfaces

### 登录二维码

```bash
python scripts/wechat_article_assistant.py login-start \
  --channel telegram \
  --target telegram:5747692163 \
  --account 8606699467 \
  --inbound-meta-file meta.json \
  --json
```

### 导入旧登录文件

```bash
python scripts/wechat_article_assistant.py login-import \
  --file path/to/cookie.json \
  --validate true \
  --json
```

### 配置代理

```bash
python scripts/wechat_article_assistant.py proxy-set \
  --url http://127.0.0.1:7890 \
  --enabled true \
  --apply-article-fetch true \
  --apply-sync true \
  --json
```

### URL 反查公众号

```bash
python scripts/wechat_article_assistant.py resolve-account-url \
  --url https://mp.weixin.qq.com/s/example \
  --json
```

### 外部定时入口

```bash
python scripts/wechat_article_assistant.py sync-due --json
python scripts/wechat_article_assistant.py sync-due --grace-minutes 5 --json
```

说明：

- `sync-due` 支持按分钟补跑窗口，避免计划任务晚触发 1~几分钟时直接错过。
- `sync_account` 在首次命中本地已有文章后，默认继续多抓 1 页做冗余。

### 抓取文章详情

```bash
python scripts/wechat_article_assistant.py article-detail \
  --aid 2247493916_1 \
  --download-images true \
  --include-html false \
  --save true \
  --json
```

### 调试与联调

```bash
python scripts/wechat_article_assistant.py --debug doctor --json
python scripts/dev/smoke_test.py --cookie-file path/to/cookie.json --steps doctor,login-import,search
```
