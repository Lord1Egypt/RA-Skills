# 使用指南 — 通用内容审核 Skill

## 快速开始

```bash
# 1. 确保 VPN 已连接
ifconfig ppp0

# 2. 先 dry-run 验证
python review.py --config config.json --dry-run

# 3. 确认无误后正式运行
python review.py --config config.json
```

## 命令行参数

```
python review.py [选项]

选项：
  --config PATH       配置文件路径（默认: config.json）
  --rules PATH        规则文件路径（默认: 同目录下 rules.json）
  --dry-run           只判断不提交结果
  --max-pages N       最大处理页数
  --fetch-only        只拉取待审列表（不判断、不提交）
  --output PATH       拉取模式的输出路径（默认: pending_review.json）
  --decisions FILE    提交审核决定文件
```

## 使用模式

### 模式 1：自动审核（最常用）

直接运行，用内置规则自动判断并提交：

```bash
python review.py --config config.json
```

审核逻辑：
- 命中 `rules.json` 中的规则 → 自动拒绝
- 未命中任何规则 → 自动通过
- 如果配了技术部 API key → 本地规则通过后再过一遍 API 双重审核

### 模式 2：拉取 → 人工/AI判断 → 提交

适用于希望先看内容再决定的场景：

```bash
# 第1步：拉取待审内容
python review.py --config config.json --fetch-only
# → 生成 pending_review.json

# 第2步：审核判断（人工看 / 丢给 AI）
# 生成 decisions.json：
# [
#   {"id": 123, "verdict": "approved"},
#   {"id": 456, "verdict": "rejected", "reason": "包含广告"}
# ]

# 第3步：提交结果
python review.py --config config.json --decisions decisions.json
```

### 模式 3：自动审核 + 技术部 API 增强

在 `config.json` 中填入 `moderation.api_key` 后：

```bash
python review.py --config config.json
```

此时审核流程变为两层：
1. 本地规则先筛一遍（毫秒级）
2. 本地规则通过的，再送技术部 API 做 AI 深度审核

## 审核规则说明

### rules.json 结构

```json
{
  "rules": [
    {
      "id": "contact_keywords",        // 规则 ID（日志中显示）
      "name": "联系方式关键词",          // 规则名称
      "description": "检测微信/QQ等",    // 说明
      "enabled": true,                  // 是否启用
      "field": "_text",                 // 匹配哪个字段（_text = 全部送审字段拼接）
      "patterns": ["正则1", "正则2"],    // 正则表达式列表（命中任意一个即拒绝）
      "reason": "拒绝原因"              // 命中后的拒绝理由
    }
  ]
}
```

### field 字段说明

| 值 | 含义 |
|----|------|
| `_text` | 所有 `content_fields` 拼接的全文（默认） |
| `title` | 只匹配 title 字段 |
| `phone` | 只匹配 phone 字段 |
| `address` | 只匹配 address 字段 |
| `price` | 只匹配 price 字段（配合 `"type": "price_check"` 使用） |

### 特殊规则类型

**价格校验（`"type": "price_check"`）：**
```json
{
  "id": "price_range",
  "enabled": true,
  "field": "price",
  "type": "price_check",
  "min_price": 1500,
  "max_price": 5000,
  "must_be_multiple_of": 100,
  "reason": "价格不符合标准"
}
```

**标题格式校验（`"type": "title_format"`）：**
```json
{
  "id": "title_format",
  "enabled": true,
  "field": "title",
  "type": "title_format",
  "pattern": "^[^\\s]{1,20}(?:\\s*[-—~～·•|｜:：]\\s*|\\s+).+$",
  "reason": "标题格式不符"
}
```

### 如何自定义规则

**方法 1：手动编辑**
直接修改 `rules.json`，启用/禁用规则或调整正则。

**方法 2：让 AI 帮改**
把 `rules.json` 的内容发给 Claude，告诉它：
- "我们站点是做 xx 的，需要检测 xx 关键词"
- "把价格范围改成 2000-8000"
- "加一条规则：标题不能包含 xxx"

AI 会帮你生成修改后的规则文件。

## 各站点配置示例

### 示例 A：评论审核站点

```json
{
  "site": {
    "name": "Phob 评论",
    "base_url": "https://staff.phob.cc",
    "module": "comments",
    "vpn_interface": "ppp0",
    "endpoints": {
      "login_page": "/d.php?mod=login&code=login",
      "login_submit": "/d.php?mod=login&code=dologin",
      "fetch": "/d.php?mod={module}&code=listAjax",
      "submit": "/d.php?mod={module}&code=batchCheck"
    },
    "login_fields": {
      "username_field": "username",
      "password_field": "password",
      "totp_field": "card_num"
    }
  },
  "auth": { "username": "xxx", "password": "xxx", "totp_seed": "xxx" },
  "moderation": { "content_fields": ["comment"] },
  "fetch": { "pending_status": "0", "page_size": 90, "max_pages": 10 },
  "submit": { "approve_status": "2", "reject_status": "1" }
}
```

### 示例 B：资源帖审核站点

```json
{
  "site": {
    "name": "茶馆大厅",
    "base_url": "https://staff.tea123.me",
    "module": "info",
    "vpn_interface": "ppp0",
    "endpoints": {
      "login_page": "/d.php/admin/login/index",
      "login_submit": "/d.php/admin/login/doLogin",
      "fetch": "/d.php/admin/{module}/listAjax",
      "submit": "/d.php/admin/{module}/verifyStatus"
    },
    "login_fields": {
      "username_field": "user_name",
      "password_field": "password",
      "totp_field": "card_num"
    }
  },
  "auth": { "username": "xxx", "password": "xxx", "totp_seed": "xxx" },
  "moderation": { "content_fields": ["title", "content"] },
  "fetch": { "pending_status": "1", "page_size": 90, "max_pages": 10 },
  "submit": { "approve_status": "2", "reject_status": "3" }
}
```

### 示例 C：VIP 资源审核站点

```json
{
  "site": {
    "name": "茶馆雅间",
    "base_url": "https://staff.tea123.me",
    "module": "infovip",
    "vpn_interface": "ppp0",
    "endpoints": {
      "login_page": "/d.php/admin/login/index",
      "login_submit": "/d.php/admin/login/doLogin",
      "fetch": "/d.php/admin/{module}/listAjax",
      "submit": "/d.php/admin/{module}/verifyStatus"
    },
    "login_fields": {
      "username_field": "user_name",
      "password_field": "password",
      "totp_field": "card_num"
    }
  },
  "auth": { "username": "xxx", "password": "xxx", "totp_seed": "xxx" },
  "moderation": { "content_fields": ["title"] },
  "fetch": { "pending_status": "1", "page_size": 90, "max_pages": 10 },
  "submit": { "approve_status": "2", "reject_status": "3" }
}
```

> 示例 C 建议在 `rules.json` 中启用 `title_format` 和 `price_range` 规则。

## 审核结果说明

| 日志标记 | 含义 | 行为 |
|---------|------|------|
| `PASS` | 通过所有规则 | 自动提交"通过" |
| `REJECT [rule_id]` | 命中本地规则 | 自动提交"拒绝" + 原因 |
| `REJECT` | API 判定违规 | 自动提交"拒绝" + 原因 |
| `FLAG` | API 判定存疑 | **不提交**，留给人工 |

## decisions.json 格式

手动模式下的审核决定文件格式：

```json
[
  {"id": 123, "verdict": "approved"},
  {"id": 456, "verdict": "rejected", "reason": "包含广告联系方式"},
  {"id": 789, "verdict": "flagged"}
]
```

- `verdict` 为 `approved` → 提交通过
- `verdict` 为 `rejected` → 提交拒绝（附带 reason）
- `verdict` 为 `flagged` → 跳过，不提交

## 常见问题

**Q: 不装 requests 库能用吗？**
A: 能。只用本地规则审核不需要 requests。只有启用技术部 API 时才需要。

**Q: 如何确定 module 名？**
A: 登录后台 → 进审核页 → 看地址栏 `/admin/` 后面的部分。

**Q: 如何确定 content_fields？**
A: 浏览器 F12 → Network → 找 `listAjax` 请求 → 查看响应中 `data` 里的字段名。

**Q: 规则误判怎么办？**
A: 修改 `rules.json`，禁用或调整误判的规则。也可以把规则文件发给 Claude 让它帮你优化。

**Q: 同时跑多个站点会冲突吗？**
A: 不会。每次运行使用独立的 cookie 文件。

**Q: "不允许重复审核"是什么意思？**
A: 这条内容已被其他审核员处理了，脚本自动跳过。
