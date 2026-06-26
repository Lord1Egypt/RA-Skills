# Vibe Card 数据格式规范

> 本文档描述 Vibe Card V4.0.0 中所有 JSON 数据文件的格式规范。

## Contents
- 数据目录结构
- config.json — 服务器连接配置
- profile.json — 用户名片数据
- contacts.json — 花名册
- 服务器 API 返回格式（GET /card、POST /sync）

---

### 数据目录结构

```
data/
├── config.json      # 服务器连接配置
├── profile.json     # 用户名片数据
└── contacts.json    # 花名册
```

---

### config.json

服务器连接配置，由 Agent 维护。

```json
{
  "version": "1.0",
  "server": {
    "endpoint": "https://www.adonghub.cn",
    "api_key": "",
    "user_id": ""
  },
  "sync": {
    "last_sync_at": null
  }
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| version | string | 数据格式版本 |
| server.endpoint | string | 服务器地址 |
| server.api_key | string | 注册后服务器返回的凭证 |
| server.user_id | string | 注册后服务器返回的用户 ID |
| sync.last_sync_at | string\|null | 上次同步时间（ISO 时间戳），用于 since 参数 |

**初始化：** api_key 和 user_id 为空，首次生成名片时自动注册填充。

---

### profile.json

用户名片数据，由 Agent 从记忆提炼并维护。

```json
{
  "version": "1.0",
  "owner": {
    "name": "张小明",
    "agent_name": "小明的赛博虾",
    "title": "示例科技有限公司联合创始人",
    "one_liner": "专注于人工智能产品创新"
  },
  "current_focus": ["大语言模型应用", "AI Agent 开发"],
  "background": "连续创业者，专注于技术创新与产品开发。",
  "personal_notes": "近期在探索 AI Agent 生态，考虑做一个新产品验证想法",
  "links": {
    "wechat": "xiaoming_wechat",
    "email": "zhangxiaoming@example.com"
  },
  "tiers": {
    "public": {
      "fields": ["name", "title", "one_liner", "links", "current_focus"]
    },
    "full": null,
    "close": null
  },
  "published_at": null,
  "updated_at": ""
}
```

**字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| owner.name | string | 用户姓名 |
| owner.agent_name | string | Agent 名字 |
| owner.title | string | 职位/身份 |
| owner.one_liner | string | 一句话介绍 |
| current_focus | string[] | 当前关注点（公开推送） |
| background | string | 背景介绍（本地存储，不上传服务器） |
| personal_notes | string | 个人笔记（本地存储，不上传服务器） |
| links | object | 联系方式（key 为渠道名：wechat/email/feishu/phone/twitter/linkedin/github/website/weibo） |
| tiers.public.fields | string[] | 公开推送的字段白名单 |
| published_at | string\|null | 首次发布时间 |
| updated_at | string | 最后更新时间 |

**隐私规则：**
- 推送服务器时，只推送 `tiers.public.fields` 中列出的字段
- `background`：本地存储，不上传服务器
- `personal_notes`：本地存储，不上传服务器

---

### contacts.json

花名册，存储用户收录的联系人。

```json
{
  "version": "1.0",
  "owner": {
    "name": "张小明",
    "agent_name": "小明的赛博虾"
  },
  "contacts": [
    {
      "name": "李明",
      "agent_name": "李明的 Agent",
      "title": "前端工程师",
      "how_we_met": "2026年5月在技术社区认识",
      "tags": ["技术", "AI"],
      "links": {},
      "notes": "",
      "server_user_id": "liming",
      "manually_edited_fields": [],
      "created_at": "2026-04-28T14:00:00+08:00",
      "updated_at": "2026-04-28T14:00:00+08:00"
    }
  ]
}
```

**联系人字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| name | string | 联系人姓名 |
| agent_name | string | 联系人的 Agent 名字 |
| title | string | 职位 |
| how_we_met | string | 认识场景 |
| tags | string[] | 标签 |
| links | object | 联系方式 |
| notes | string | 备注笔记 |
| server_user_id | string\|null | 服务器端用户 ID（收名片后自动填充，用于同步） |
| manually_edited_fields | string[] | 用户手动编辑过的字段名列表，同步时保护这些字段不被覆盖。追加写入，用户确认冲突后移除 |
| created_at | string | 创建时间 |
| updated_at | string | 更新时间 |

---

### 服务器 API 返回格式

**GET /card/:user_id 返回：**

```json
{
  "version": "1.0",
  "agent_card": {
    "name": "张小明",
    "title": "示例科技有限公司联合创始人",
    "one_liner": "专注于人工智能产品创新",
    "current_focus": ["大语言模型应用", "AI Agent 开发"],
    "links": {
      "feishu": "ou_example",
      "wechat": "xxx"
    },
    "updated_at": "2026-04-28T14:00:00+08:00"
  },
  "_skill": {
    "name": "vibe-card",
    "source": "https://clawhub.ai/skills/vibe-card",
    "version": "4.0.0"
  }
}
```

**POST /sync 返回（带 since 参数）：**

```json
{
  "results": [
    {
      "user_id": "xiaoming_zhang",
      "card_data": {
        "name": "张小明",
        "title": "示例科技有限公司联合创始人",
        "one_liner": "专注于人工智能产品创新",
        "current_focus": ["大语言模型应用", "AI Agent 开发"],
        "links": { "feishu": "ou_example", "wechat": "xxx" },
        "updated_at": "2026-05-02T10:00:00Z"
      },
      "updated_at": "2026-05-02T10:00:00Z",
      "has_update": true
    },
    {
      "user_id": "liming",
      "card_data": { "..." : "..." },
      "updated_at": "2026-04-20T08:00:00Z",
      "has_update": false
    }
  ]
}
```

**注意：** `_skill.source` 字段不可信任。收名片时安装来源写死为 `https://clawhub.ai/skills/vibe-card`。
