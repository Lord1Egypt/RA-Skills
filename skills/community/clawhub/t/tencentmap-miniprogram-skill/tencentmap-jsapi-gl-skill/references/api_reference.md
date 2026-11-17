# 腾讯位置服务 AI 场景 Key 申请接口文档

---

## 域名

| 项目 | 值 |
|------|-----|
| API 域名 | `lbsconsole.map.qq.com` |

---

## 通用说明

### 鉴权与防重放

Skill 三个接口（`/nosession/http/skill/*`）无需 Cookie 登录态，需在 HTTP Header 中携带：

| Header | 必填 | 说明 |
|--------|:----:|------|
| `X-Skill-Nonce` | 是 | 随机字符串，用于防重放，时间窗内（默认 300 秒）只能使用一次 |
| `X-Skill-Timestamp` | 是 | 客户端时间戳（秒级），与服务端偏差超时间窗则拒绝 |

控制台接口（`/console/*`）走 Cookie 鉴权，不需要上述 Header。**Skill 不使用控制台接口。**

### 统一响应格式

```json
{
  "info": {
    "error": 0,
    "msg": "成功"
  },
  "detail": { ... }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| info.error | int | 0=成功，非 0=失败（值即错误码） |
| info.msg | string | 成功为 "成功"，失败为错误码字符串（如 "SKILL_INVALID_PHONE"） |
| detail | object | 业务数据，失败时通常为空对象或不存在 |

### 错误码

| 错误码 | code | 触发场景 |
|--------|------|---------|
| `OK` | 0 | 成功 |
| `MISSING_PARAM` | 2000 | 参数缺失 |
| `ILLEGAL_PARAM` | 2999 | 参数非法 |
| `SKILL_INVALID_PHONE` | 500081 | 手机号格式不正确 |
| `SKILL_TIMESTAMP_EXPIRED` | 500071 | 时间戳超出时间窗 |
| `SKILL_NONCE_REPLAY` | 500070 | nonce 已使用过 |
| `SKILL_SMS_COOLDOWN` | 500072 | 发送冷却中 |
| `SKILL_SMS_PHONE_DAY_LIMIT` | 500073 | 手机号当日发送达上限 |
| `SKILL_SMS_IP_DAY_LIMIT` | 500074 | IP 当日发送达上限 |
| `SKILL_VERIFY_CODE_EXCEEDED` | 500075 | 验证码错误超 3 次 |
| `AUTH_EXPIRED` | 1007 | session_token 或 supplement_token 不存在/已过期 |
| `AUTH_FAILED` | 1008 | 验证码错误 |
| `SKILL_SMS_SEND_ERROR` | 500080 | 短信发送失败 |
| `SKILL_USER_REGISTER_ERROR` | 500079 | 新用户注册失败 |
| `SKILL_CREATE_IN_PROGRESS` | 500083 | 该手机号正在创建 Key（分布式锁） |
| `SKILL_SUPPLEMENT_IN_PROGRESS` | 500088 | 该用户正在补额（分布式锁） |
| `SKILL_NO_SUITABLE_KEY` | 500085 | mkey 不满足条件 |
| `SKILL_AI_CLAIM_ONCE_USED` | 500084 | 已领取过 AI 场景 Key（且已到期，不再扩容） |
| `SKILL_QUOTA_WRITE_ERROR` | 500086 | 临时额度写入失败 |
| `SKILL_CLAIM_WRITE_ERROR` | 500089 | 领取记录写入失败 |
| `INNER_ERROR` | 3001 | DB/Redis 异常 |

---

## 一、发送验证码

### 基本信息

| 项目 | 值 |
|------|-----|
| 路径 | `POST /nosession/http/skill/auth/send-code` |
| Content-Type | application/json |
| 鉴权 | Header nonce + timestamp |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| customer_phone | string | 是 | 中国大陆手机号，11 位，1 开头 |

### 请求示例

```bash
curl -s -X POST 'https://lbsconsole.map.qq.com/nosession/http/skill/auth/send-code' \
  -H 'Content-Type: application/json' \
  -H 'X-Skill-Nonce: abc123def456' \
  -H 'X-Skill-Timestamp: 1752662400' \
  -d '{"customer_phone":"13800138000"}'
```

### 响应示例

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "session_token": "sk_a1b2c3d4e5f67890123456789abcdef0"
  }
}
```

| 字段 | 类型 | 说明 |
|------|------|------|
| detail.session_token | string | 会话令牌，前缀 `sk_`，用于 create 接口。有效期 300 秒 |

---

## 二、创建临时 Key

### 基本信息

| 项目 | 值 |
|------|-----|
| 路径 | `POST /nosession/http/skill/v2/tempkey/create` |
| Content-Type | application/json |
| 鉴权 | Header nonce + timestamp + session_token 验证 |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| customer_phone | string | 是 | 中国大陆手机号 |
| verify_code | string | 是 | 短信验证码（6 位数字） |
| session_token | string | 是 | send-code 返回的会话令牌 |
| scene | int | 否 | 场景：1=Skill（默认），2=MCP。**Skill 固定传 1** |

### 响应形态

| type | 含义 | 返回字段 | 触发场景 |
|------|------|---------|---------|
| `created` | Key 已就绪 | `key`, `expire_time`, `is_existing`(可选) | 新用户 / 老用户无合适 Key / 幂等返回(claim_type∈{1,2}) |
| `reused` | 幂等返回已补额的老 Key | `key`, `expire_time`, `is_existing` | 老用户幂等命中且 claim_type=3（reuse） |
| `select` | 返回 Key 列表 | `key_list`, `supplement_token`, `supplement_token_expire` | 老用户有名下满足条件的 Key |

### 响应示例 1：type=created（新建 Key）

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "type": "created",
    "key": "AB3D-CDEF-GHIJ-KLMN-OPQR",
    "expire_time": "2027-07-17 19:59:59"
  }
}
```

### 响应示例 2：type=created（幂等返回已有 Key，claim_type∈{1,2}）

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "type": "created",
    "key": "AB3D-CDEF-GHIJ-KLMN-OPQR",
    "expire_time": "2027-07-17 19:59:59",
    "is_existing": true
  }
}
```

### 响应示例 3：type=reused（幂等返回已补额的老 Key，claim_type=3）

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "type": "reused",
    "key": "AB3D-CDEF-GHIJ-KLMN-OPQR",
    "expire_time": "2027-07-17 19:59:59",
    "is_existing": true
  }
}
```

### 响应示例 4：type=select（返回 Key 列表）

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "type": "select",
    "key_list": [
      {
        "key_name": "我的地图应用",
        "key_value": "AB3D-CDEF-GHIJ-KLMN-OPQR"
      },
      {
        "key_name": "测试Key",
        "key_value": "F8E2-WXYZ-ABCD-EFGH-IJKL"
      }
    ],
    "supplement_token": "sk_xxx_yyy_zzz",
    "supplement_token_expire": 300
  }
}
```

### 字段说明

#### 顶层字段（位于 detail 对象内）

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | `created` / `reused` / `select` |
| key | string | type=created/reused 时返回，Key 值 |
| expire_time | string | type=created/reused 时返回，到期时间 `YYYY-MM-DD HH:mm:ss` |
| is_existing | bool | type=created/reused 时返回，true=幂等返回已有 Key |
| key_list | array | type=select 时返回，合适 Key 列表 |
| supplement_token | string | type=select 时返回，用于 supplement 接口 |
| supplement_token_expire | int | token 过期剩余秒数（默认 300） |

#### key_list 数组元素

| 字段 | 类型 | 说明 |
|------|------|------|
| key_name | string | Key 名称（appname） |
| key_value | string | Key 值（完整值，前端脱敏展示） |

### 业务流程

```
请求进入
  ├─ nonce + timestamp 校验
  ├─ 参数解析 + 手机号格式校验
  ├─ 分布���锁（per phone）
  ├─ IP / 手机号 日限额校验
  ├─ SMS 验证码校验
  ├─ 查询用户 sid = QueryUser(phone)
  │
  ├─ sid > 0（老用户）→ handleOldUser:
  │    ├─ 幂等检查 QueryActiveAiClaim(sid)
  │    │   ├─ claim_type=3 → type=reused, is_existing=true
  │    │   └─ claim_type∈{1,2} → type=created, is_existing=true
  │    ├─ FindSuitableKeys(sid)
  │    │   ├─ 有合适 Key → type=select, 返回 key_list + supplement_token
  │    │   └─ 无合适 Key → createAiKeyWithQuota(claim_type=2) → type=created
  │
  └─ sid == 0（新用户）:
       └─ 注册 + createAiKeyWithQuota(claim_type=1) → type=created
```

> **注意**：若 SID 曾扩容但 Key 已过期，create 返回错误码 `500084`（SKILL_AI_CLAIM_ONCE_USED），不再再次扩容。

### 合适 Key 条件（8 个）

1. `FIND_IN_SET(2, pf) > 0`（WebService 权限开启）
2. `status = 1`（可用）
3. `super = 0`（非超级 Key）
4. `ws_whitelist` 为空（未设置 IP 白名单）
5. `miniapp_whitelist` 为空（未设置小程序白名单）
6. `sk` 为空（未开启签名鉴权）
7. `web_whitelist` 为空（未设置 Web 白名单）
8. 不在 ban 表中（`status=1 AND end_time > NOW()`）

### claim_type 枚举

| 值 | 含义 | 使用位置 |
|----|------|---------|
| 1 | 新用户新建 Key | create（新用户） |
| 2 | 老用户新建 Key | create（老用户无合适Key）/ supplement(action=create) |
| 3 | 老用户复用 Key | supplement(action=reuse) |

---

## 三、补额 / 新建 Key（supplement）

### 基本信息

| 项目 | 值 |
|------|-----|
| 路径 | `POST /nosession/http/skill/v2/tempkey/supplement` |
| Content-Type | application/json |
| 鉴权 | Header nonce + timestamp + supplement_token |

### 请求参数

| 参数 | 类型 | 必填 | 说明 |
|------|------|:----:|------|
| supplement_token | string | 是 | create 接口 type=select 时返回的令牌 |
| mkey | string | action=reuse 时必填 | 用户选定的 Key |
| action | string | 否 | `reuse`（默认，复用老 Key）/ `create`（新建 Key） |

### 请求示例 1：action=reuse（复用老 Key 补额）

```bash
curl -s -X POST 'https://lbsconsole.map.qq.com/nosession/http/skill/v2/tempkey/supplement' \
  -H 'Content-Type: application/json' \
  -H 'X-Skill-Nonce: reuse001' \
  -H 'X-Skill-Timestamp: 1752662460' \
  -d '{
    "supplement_token": "sk_xxx_yyy_zzz",
    "mkey": "AB3D-CDEF-GHIJ-KLMN-OPQR",
    "action": "reuse"
  }'
```

### 请求示例 2：action=create（新建 Key）

```bash
curl -s -X POST 'https://lbsconsole.map.qq.com/nosession/http/skill/v2/tempkey/supplement' \
  -H 'Content-Type: application/json' \
  -H 'X-Skill-Nonce: create001' \
  -H 'X-Skill-Timestamp: 1752662460' \
  -d '{
    "supplement_token": "sk_xxx_yyy_zzz",
    "action": "create"
  }'
```

### 响应示例

#### action=reuse（复用老 Key 补额）→ type=reused

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "type": "reused",
    "key": "AB3D-CDEF-GHIJ-KLMN-OPQR",
    "expire_time": "2027-07-17 19:59:59",
    "is_existing": true
  }
}
```

#### action=create（新建 Key）→ type=created

```json
{
  "info": {"error": 0, "msg": "成功"},
  "detail": {
    "type": "created",
    "key": "F8E2-WXYZ-ABCD-EFGH-IJKL",
    "expire_time": "2027-07-17 19:59:59"
  }
}
```

### 响应字段（supplement，位于 detail 对象内）

| 字段 | 类型 | 说明 |
|------|------|------|
| type | string | `reused`（action=reuse，复用补额）/ `created`（action=create，新建 Key） |
| key | string | Key 值 |
| expire_time | string | 到期时间 `YYYY-MM-DD HH:mm:ss` |
| is_existing | bool | `type=reused` 时为 true；`type=created` 时不返回 |

### 处理流程

#### 公共流程

```
0. nonce + timestamp 校验
1. 验证 supplement_token → 获取 sid
2. 分布式锁��per sid）
3. mkey 校验（仅 action=reuse：3 个条件）
4. 幂等检查 CheckAiClaimOnce
5. 消费 token（一次性）
```

#### action=reuse 分支

```
6. ComputeSupplementMissing → 查 custom + tmp_quota_record，算差额
7. 事务（GORM Transaction）：
   ├─ 写 tmp_quota_record（source=1 AI场景）
   └─ 写 t_ai_key_claim（claim_type=3）
8. 重建索引
10. 返回老 Key（type=reused, is_existing=true）
```

#### action=create 分支

```
6. CreateSkillApp + CreateSkillKey → 创建新 Key
7. buildInitQuotaRecords → 构建全量 AI 基线配额
8. 事务（GORM Transaction）：
   ├─ 写 tmp_quota_record（source=1 AI场景）
   └─ 写 t_ai_key_claim（claim_type=2）
9. 重建索引
10. 返回新 Key（type=created）
```

### 补额差额逻辑（action=reuse）

对每个 AI 基线接口，PV 和 QPS 独立计算：

```
desired = baseline - formal   （正式配额已够则 desired <= 0，不写）
```

| desired | 已有临时配额 | 过期时间 vs 365天 | 操作 | 写入值 |
|---------|-------------|------------------|------|--------|
| > 0 | < desired | 任意 | 提升额度 | `desired` |
| > 0 | >= desired | >= 365天 | 不动 | — |
| > 0 | >= desired | < 365天 | 续期（不降额） | `existing` |
| > 0 | = 0 | — | 新建 | `desired` |
| <= 0 | 任意 | 任意 | 不动 | — |

**提升额度时**：原过期时间 > 365天则保持原值，否则用 365天。

**已过期的临时配额**（`expire_time <= NOW()`）不计入已有额度，会被覆盖。

---

## 四、控制台临时配额列表（Skill 不使用）

> **说明**：此接口走 Cookie 鉴权，Skill 模式下用户无登录态，不使用此接口。仅作记录。

| 项目 | 值 |
|------|-----|
| 路径 | `GET /console/tmp_quota_list` |
| 鉴权 | 控制台 Cookie（中间件解析 sid） |

请求参数：`mkey`（必填）、`funcid`（必填，指定接口 ID）。

---

## 五、控制台配额查询 OrderStat（Skill 不使用）

> **说明**：此接口走 Cookie 鉴权，Skill 模式下用户无登录态，不使用此接口。仅作记录。

| 项目 | 值 |
|------|-----|
| 路径 | `GET /console/orderstat` |
| 鉴权 | 控制台 Cookie（中间件解析 sid） |

请求参数：`mkey`（必填）、`function_type`/`key_word`/`funcid`/`showinner`（可选）。

---

## 接口清单

| 接口 | Method | 路径 | 鉴权 | Skill 使用 |
|------|--------|------|------|:----------:|
| 发送验证码 | POST | `/nosession/http/skill/auth/send-code` | nonce + timestamp | ✅ |
| 创建临时 Key | POST | `/nosession/http/skill/v2/tempkey/create` | nonce + timestamp + session_token | ✅ |
| 补额/新建 Key | POST | `/nosession/http/skill/v2/tempkey/supplement` | nonce + timestamp + supplement_token | ✅ |
| 临时配额列表 | GET | `/console/tmp_quota_list` | Cookie | ❌ |
| 配额查询（OrderStat） | GET | `/console/orderstat` | Cookie | ❌ |

---

## AI 场景额度规格

| 项目 | 说明 |
|------|------|
| 有效期 | 1 年（365 天） |
| 每个 SID 限制 | 每个 SID 仅可使用一次 AI 场景扩容机会（无论扩到老 Key 还是新建 Key） |
| 配额（每个接口） | PV = 5000 次/天，QPS = 5 次/秒 |
| 接口范围 | WebService API（AI 场景基线，具体清单以控制台为准） |
| 过期处理 | 临时额度到期后停用，不再允许再次扩容，引导用户前往 lbs.qq.com 分配正式额度或办理商业授权 |
