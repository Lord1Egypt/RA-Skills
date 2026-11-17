---
name: "xueqiu"
description: "雪球数据API接口调用工具。当用户需要查询雪球组合、用户、行情、调仓历史等投资数据时调用此技能。"
---

# 雪球数据接口技能

## 概述

此技能用于调用雪球数据接口，获取股票组合、用户信息、行情数据等投资相关数据。

## 接口基础信息

- **Base URL**：
  - 本地环境：`http://localhost:8080/wxpublic_fetch`
  - 线上环境：`https://wxpub.aibana.art`
- **请求方式**：POST
- **请求体格式**：JSON
- **鉴权**：需要 `app_id` 和 `secure_key`（在「Skill 技能」页面创建）
- **计费**：每次成功调用扣 0.2 元；失败自动退款，余额不足返回 402
- **限速**：60秒内最多10次上游请求（所有用户共享）

## 公共请求字段

所有接口都必须包含以下字段：

| 字段 | 类型 | 说明 |
|---|---|---|
| `app_id` | string | 申请的 AppID |
| `secure_key` | string | 对应的 SecureKey |

### 凭证设置提醒

**如果用户未设置 AppID 及 SecureKey**：
> 请先前往 https://wxpub.aibana.art 注册账号，在「Skill 技能」页面获取 `app_id` 和 `secure_key`。

---

## 可用接口

### 一、搜索类接口

#### 1.1 searchUser — 搜索用户

**用途**：根据关键词搜索雪球用户

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "keyword": "天地侠影",
  "count": 10,
  "page": 1
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `keyword` | string | 必填 | 搜索关键词 |
| `count` | int | 10 | 每页条数 |
| `page` | int | 1 | 页码 |

**返回字段**：用户ID、昵称、粉丝数、简介等

---

#### 1.2 searchCube — 搜索组合

**用途**：根据关键词搜索投资组合

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "keyword": "实盘",
  "count": 10,
  "page": 1
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `keyword` | string | 必填 | 搜索关键词，如「实盘」「量化」 |
| `count` | int | 10 | 每页条数 |
| `page` | int | 1 | 页码 |

**返回字段**：组合ID、代码、名称、总收益、年化收益、净值等

---

#### 1.3 searchStatus — 搜索帖子

**用途**：根据关键词搜索雪球帖子

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "keyword": "散户老牛",
  "count": 10,
  "page": 1
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `keyword` | string | 必填 | 搜索关键词 |
| `count` | int | 10 | 每页条数 |
| `page` | int | 1 | 页码 |

**返回字段**：帖子ID、标题、摘要（HTML格式）、发布时间、作者信息、浏览数等

**注意**：
- `description` 为 HTML 格式（含 `<br/>` 等标签），展示前需自行处理
- `target` 拼完整 URL：`https://xueqiu.com{target}`

---

#### 1.4 searchCubeRanked — 组合排行

**用途**：搜索组合并按总收益降序排列，支持收益过滤

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "keyword": "实盘",
  "count": 30,
  "minTotalGain": 50,
  "minAnnualRate": 10,
  "topN": 10
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `keyword` | string | 必填 | 搜索关键词 |
| `count` | int | 30 | 拉取条数用于排序 |
| `page` | int | 1 | 页码 |
| `minTotalGain` | double | -1 | 最低总收益过滤(%) |
| `minAnnualRate` | double | -1 | 最低年化收益过滤(%) |
| `topN` | int | 10 | 返回前N名 |

---

### 二、行情类接口

#### 2.1 getCubeQuote — 组合实时行情

**用途**：获取组合的实时净值和收益数据

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "symbol": "ZH349701"
}
```

**参数说明**：
| 参数 | 类型 | 说明 |
|---|---|---|
| `symbol` | string | 组合代码，如 `ZH349701`、`SP1008279` |

---

#### 2.2 getCubeNavHistory — 组合净值历史

**用途**：获取组合的历史净值数据（日频）

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "cubeId": 349603,
  "count": 30
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `cubeId` | int | 必填 | 组合数字ID（从搜索结果的id字段获取） |
| `count` | int | 30 | 返回天数（最大约365） |

---

### 三、组合/用户信息接口

#### 3.1 getCubeInfo — 组合详情

**用途**：获取组合的详细信息，包括持仓、调仓记录等

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "symbol": "ZH012463"
}
```

**参数说明**：
| 参数 | 类型 | 说明 |
|---|---|---|
| `symbol` | string | 组合代码 |

**返回字段**：组合名称、描述、总收益、年化收益、最新持仓、主人信息等

**注意**：
- `SP`前缀的老组合只返回基础元数据，`total_gain`/`net_value`/`last_rebalancing` 等字段为 `null`，这是正常行为
- 部分新组合也可能因数据同步延迟出现字段为 `null` 的情况，建议调用时做好空值处理

---

#### 3.2 getUserCubes — 用户创建的所有组合

**用途**：获取某用户创建的所有组合列表

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "userId": 8601813520
}
```

**参数说明**：
| 参数 | 类型 | 说明 |
|---|---|---|
| `userId` | long | 用户数字ID |

---

#### 3.3 getUserTimeline — 用户原创发帖

**用途**：获取用户的原创帖子列表

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "userId": 8601813520,
  "page": 1
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `userId` | long | 必填 | 用户数字ID |
| `page` | int | 1 | 页码 |

---

### 四、调仓历史接口

#### 4.1 getCubeRebalancing — 调仓历史

**用途**：获取组合的历史调仓记录

**请求示例**：
```json
{
  "app_id": "your_app_id",
  "secure_key": "your_secure_key",
  "cubeId": 12363,
  "page": 1,
  "count": 10
}
```

**参数说明**：
| 参数 | 类型 | 默认 | 说明 |
|---|---|---|---|
| `cubeId` | int | 必填 | 组合数字ID |
| `page` | int | 1 | 页码 |
| `count` | int | 10 | 每页条数 |

**返回字段**：调仓时间、现金比例、股票变动明细（股票名称、代码、权重变化、价格等）

**注意**：每条调仓记录只包含当次变动的股票

---

## 错误处理

所有错误返回格式：`{"error": "..."}`

| 状态码 | 含义 | 处理建议 |
|---|---|---|
| 400 | 参数错误 | 检查必填参数是否完整 |
| 401 | 凭证无效 | 检查app_id和secure_key |
| 402 | 余额不足 | 前往 https://wxpub.aibana.art 充值后重试 |
| 404 | 方法不存在 | 检查接口路径 |
| 429 | 请求过多 | 稍后重试 |
| 500 | 服务器错误 | 联系管理员 |
| 502 | 上游雪球调用失败 | 稍后重试，自动退款 |
| 503 | 排队超时 | 稍后重试 |

---

## 调用频率建议

- 建议客户端控制节奏：每6秒一次请求最稳定
- 全局限速：60秒内最多10次上游请求
- 队列限制：同时排队超过20个请求返回429
- 超时限制：排队等待超过120秒返回503

---

## 使用场景

当用户提出以下需求时，应调用此技能：

1. **搜索雪球用户或组合**：使用 `searchUser` 或 `searchCube`
2. **搜索帖子内容**：使用 `searchStatus` 按关键词查找帖子
3. **查看组合排行**：使用 `searchCubeRanked` 筛选高收益组合
4. **获取实时行情**：使用 `getCubeQuote` 查看组合当前净值
5. **分析历史业绩**：使用 `getCubeNavHistory` 获取净值曲线
6. **查看组合详情和持仓**：使用 `getCubeInfo` 获取完整信息
7. **追踪用户组合**：使用 `getUserCubes` 查看某用户的所有组合
8. **阅读用户观点**：使用 `getUserTimeline` 获取用户帖子
9. **分析调仓记录**：使用 `getCubeRebalancing` 追踪调仓历史

---

## curl 调用示例

```bash
# 搜索帖子
curl -X POST https://wxpub.aibana.art/xueqiu/searchStatus \
  -H "Content-Type: application/json" \
  -d '{"app_id":"ak_xxx","secure_key":"yyy","keyword":"散户老牛","count":10,"page":1}'

# 搜索组合
curl -X POST https://wxpub.aibana.art/xueqiu/searchCube \
  -H "Content-Type: application/json" \
  -d '{"app_id":"ak_xxx","secure_key":"yyy","keyword":"实盘","count":10,"page":1}'

# 组合排行 Top 5
curl -X POST https://wxpub.aibana.art/xueqiu/searchCubeRanked \
  -H "Content-Type: application/json" \
  -d '{"app_id":"ak_xxx","secure_key":"yyy","keyword":"实盘","count":30,"topN":5}'

# 组合详情
curl -X POST https://wxpub.aibana.art/xueqiu/getCubeInfo \
  -H "Content-Type: application/json" \
  -d '{"app_id":"ak_xxx","secure_key":"yyy","symbol":"ZH012463"}'

# 调仓历史
curl -X POST https://wxpub.aibana.art/xueqiu/getCubeRebalancing \
  -H "Content-Type: application/json" \
  -d '{"app_id":"ak_xxx","secure_key":"yyy","cubeId":12363,"page":1,"count":5}'
```