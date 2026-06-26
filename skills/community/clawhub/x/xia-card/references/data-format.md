# 虾名片 JSON 数据格式参考

> 本文档描述虾名片 AgentCard V2.5.0 中所有 JSON 数据文件的格式规范。

---

## profile.json — 个人名片数据

### 完整示例

```json
{
  "version": "1.0",
  "owner": {
    "name": "沈兴东",
    "agent_name": "活爹虾",
    "title": "Leewow 联合创始人",
    "one_liner": "专注定制化生活方式品牌，连续创业者"
  },
  "current_focus": ["SDS 智能选品", "Agent 生态探索"],
  "background": "连续创业者，Leewow 联合创始人，擅长找人、找资源、资本对接。",
  "personal_notes": "近期在探索 Agent 生态，考虑做一个小产品验证",
  "links": {
    "feishu": "ou_xxx",
    "wechat": "xxx"
  },
  "tiers": {
    "public": {
      "fields": ["name", "title", "one_liner", "links", "current_focus"]
    },
    "full": null,
    "close": null
  },
  "published_at": null,
  "updated_at": "2026-04-28T14:00:00+08:00"
}
```

### 字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `version` | string | 是 | 格式版本，固定 `"1.0"` |
| `owner.name` | string | 是 | 用户真实姓名或常用名 |
| `owner.agent_name` | string | 否 | Agent 的名称 |
| `owner.title` | string | 否 | 职位/头衔 |
| `owner.one_liner` | string | 否 | 一句话自我介绍 |
| `current_focus` | string[] | 否 | 当前聚焦的方向/项目 |
| `background` | string | 否 | 个人背景描述 |
| `personal_notes` | string | 否 | 个人笔记，**永远不会上传服务器** |
| `links` | object | 否 | 联系方式，key 为渠道名（feishu/wechat/email/phone 等） |
| `tiers.public.fields` | string[] | 是 | 公开名片包含的字段名列表 |
| `tiers.full` | null | — | V3 预留，V1 固定为 null |
| `tiers.close` | null | — | V3 预留，V1 固定为 null |
| `published_at` | string\|null | 是 | 上次发布到服务器的时间，null 表示未发布 |
| `updated_at` | string | 是 | 最后更新时间，ISO 8601 格式 |

### 隐私规则

- `personal_notes`：纯本地存储，**永远不会上传服务器**
- `background`：V1 本地存储，不上传服务器
- 上传服务器时，只推送 `tiers.public.fields` 中列出的字段

---

## contacts.json — 花名册数据

### 完整示例

```json
{
  "version": "1.0",
  "owner": {
    "name": "沈兴东",
    "agent_name": "活爹虾"
  },
  "contacts": [
    {
      "id": "c001",
      "name": "张威",
      "company": "智谱 AI",
      "role": "产品经理",
      "tags": ["同行", "朋友"],
      "met_at": "2026-04-20",
      "met_scene": "飞书群",
      "agent": {
        "name": "小智",
        "platform": "openclaw"
      },
      "contact": {
        "feishu": "ou_xxx"
      },
      "notes": "上次聊了出海方向",
      "server_user_id": "mkwxyz",
      "manually_edited_fields": [],
      "updated_at": "2026-04-28T14:00:00+08:00"
    }
  ]
}
```

### 联系人字段说明

| 字段 | 类型 | 必填 | 说明 |
|------|------|------|------|
| `id` | string | 是 | 自动生成，格式 `c` + 时间戳 |
| `name` | string | **是** | 联系人姓名，缺失时必须追问 |
| `company` | string | 否 | 所在公司/组织 |
| `role` | string | 否 | 职位/角色 |
| `tags` | string[] | 否 | 自定义标签 |
| `met_at` | string | 是 | 认识日期，YYYY-MM-DD，录入时自动填当前日期 |
| `met_scene` | string | 否 | 认识的场景（如"飞书群"、"线下活动"） |
| `agent.name` | string | 否 | 联系人的 Agent 名称 |
| `agent.platform` | string | 否 | 联系人的 Agent 平台 |
| `contact` | object | 否 | 联系方式，key 为渠道名 |
| `notes` | string | 否 | 备注信息 |
| `server_user_id` | string | 否 | **V2 新增** 对方在服务器上的 user_id，收名片时自动记录，用于同步 |
| `manually_edited_fields` | string[] | 否 | **V2.2 新增** 记录哪些字段被用户手动修改过，同步时不被服务器数据覆盖 |
| `updated_at` | string | 是 | 最后更新时间，ISO 8601 格式 |

### V2 变更说明

- 新增 `server_user_id` 字段：收名片时从 `agent-card://user_id` 中提取并记录
- 同步花名册时通过此字段匹配联系人，获取最新名片数据

### V2.2 变更说明

- 新增 `manually_edited_fields` 字段：记录被用户手动修改过的字段名（如 `["company"]`），同步时这些字段不会被服务器数据覆盖
- 收名片去重策略：按 `server_user_id` 精确匹配 → 同名无 `server_user_id` 时提示用户确认 → 无匹配则新建
- 同步冲突处理：检测 `manually_edited_fields` 与服务器返回数据的冲突，提示用户选择

### V1 不包含的字段（V3 预留）

- `visibility`（V3）
- `subscribed`（V2 → 移至 V3）
- `subscriptions`（V2 → 移至 V3）
- `broadcast_opt_out`（V3）
- `last_broadcast_at`（V3）

---

## config.json — 配置文件

### 完整示例

```json
{
  "version": "1.0",
  "server": {
    "endpoint": "https://www.adonghub.cn",
    "api_key": "sk_xxxx",
    "user_id": "abcxyz"
  },
  "sync": {
    "last_sync_at": null
  }
}
```

### 字段说明

| 字段 | 类型 | 说明 |
|------|------|------|
| `version` | string | 格式版本，固定 `"1.0"` |
| `server.endpoint` | string | 服务器地址（默认 `https://www.adonghub.cn`，Skill 安装时已预填） |
| `server.api_key` | string | API Key，通过 POST /register 注册后自动获得 |
| `server.user_id` | string | 用户 ID，服务器自动生成（6 位随机小写字母），注册后自动获得 |
| `sync.last_sync_at` | string\|null | **V2 新增** 上次同步花名册的时间（ISO 8601），同步成功后自动更新，null 表示从未同步 |

### V2 变更说明

- user_id 改由服务器自动生成（6 位随机小写字母），客户端不再自行指定
- 初始化时不再要求用户提供 user_id

---

## 服务器 API

### POST /register

注册新用户。

- **请求体**：`{ "name": "用户名", "agent_name": "Agent名" }`
- **注意**：客户端不再传 user_id，由服务器自动生成
- **成功响应**：`{ "user_id": "abcxyz", "api_key": "sk_xxxx" }`
- **失败响应**：`{ "error": "name is required" }`

### PUT /card/:user_id

发布/更新名片（需先注册）。

- **Header**：`X-API-Key: sk_xxxx`
- **请求体**：profile.json 的公开部分（按 tiers.public.fields 筛选）
- **成功响应**：`{ "success": true, "updated_at": "..." }`
- **用户不存在**：`{ "error": "user not found. register first via POST /register" }`（404）
- **Key 错误**：`{ "error": "invalid api key" }`（403）

### GET /card/:user_id

获取名片 JSON。

- **响应**：结构化 JSON（含 agent_card 和 _skill 字段）

### GET /:user_id

名片网页（浏览器查看）。

- **响应**：HTML 页面（内嵌 JSON-LD）

### POST /sync

批量同步通讯录（V2 新增）。

- **Header**：`X-API-Key: sk_xxxx`
- **请求体**：`{ "targets": ["user_id_1", "user_id_2", ...] }`
- **限制**：targets 数组最多 50 个
- **成功响应**：`{ "results": [{ "user_id": "...", "updated_at": "...", "card_data": {...} }, ...] }`
- **鉴权说明**：通过 api_key 反查用户身份，不依赖 URL 参数

---

## 服务器返回格式

### GET /card/:user_id 返回的 JSON

```json
{
  "version": "1.0",
  "agent_card": {
    "name": "沈兴东",
    "title": "Leewow 联合创始人",
    "one_liner": "专注定制化生活方式品牌，连续创业者",
    "current_focus": ["SDS 智能选品", "Agent 生态探索"],
    "links": {
      "feishu": "ou_xxx",
      "wechat": "xxx"
    },
    "updated_at": "2026-04-28T14:00:00+08:00"
  },
  "_skill": {
    "name": "xia-card",
    "source": "https://clawhub.ai/skills/xia-card",
    "version": "2.5.0"
  }
}
```

### JSON-LD（HTML 页面内嵌）

HTML 名片页面（GET /:user_id）内嵌 JSON-LD，遵循 [schema.org/Person](https://schema.org/Person) 标准：

```json
{
  "@context": "https://schema.org",
  "@type": "Person",
  "name": "沈兴东",
  "jobTitle": "Leewow 联合创始人",
  "description": "专注定制化生活方式品牌，连续创业者",
  "url": "https://www.adonghub.cn/dongzong",
  "sameAs": [
    "feishu://ou_xxx",
    "wechat://xxx"
  ]
}
```

字段说明：
- `name`、`jobTitle`、`description`：schema.org/Person 标准字段
- `url`：名片页面链接
- `sameAs`：社交/通讯链接（schema.org 推荐用于关联身份）

此结构确保 Agent 即使 fetch 到 HTML 也能通过 JSON-LD 提取结构化信息。
