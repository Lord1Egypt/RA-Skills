---
name: umeng-cli-uapp-umini
version: 1.0.0
description: 友盟小程序统计查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 12 个只读接口，覆盖小程序应用概况、累计用户、留存、页面分析（受访/入口）、分享分析（概况/页面/用户）、自定义事件（列表/统计/属性/属性值分布）。当用户需要了解小程序的概况指标、留存表现、页面访问、分享效果、自定义事件数据时使用。触发词：小程序概况、小程序留存、小程序活跃用户、小程序累计用户、页面访问、入口页、分享概况、页面分享、分享用户、小程序事件、事件属性、属性值分布。仅适用于小程序 / H5 / 小游戏，不支持 Android/iOS App。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# umeng-cli-uapp-umini

基于 `umeng-cli call` 的友盟小程序统计查询 Skill，覆盖 `com.umeng.umini` 命名空间下的 12 个只读接口，与旧 `uapp-umini` 能力完全等价（零能力扩展；场景分析类接口已归 `umeng-cli-uapp-mini-channel`）。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-umini"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey（小程序 `dataSourceId`）的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-umini", "appkey":"<输入的Appkey>"}'
> ```
> 同一 Appkey 在同一会话中只打一次；若用户切换到新的 Appkey，需对新的 Appkey 再打一次。

## 适用范围（强制）

本 Skill **仅适用于小程序 / H5 / 小游戏**类应用：

| 平台（`platform`） | 是否适用 | 说明 |
|---|---|---|
| 小程序（`mini_wechat` / `mini_alipay` / `mini_bytedance` / `mini_baidu` / `mini_qq`） | ✅ | 完整适用 |
| 小游戏（`mini_game_wechat`） | ✅ | 完整适用 |
| H5（`html_5`） | ⚠️ 部分适用 | 多个指标字段不支持（详见「H5 局限汇总」小节） |
| Android App（`android`） | ❌ | **不适用**，请改用 `umeng-cli-uapp-core-index` / `umeng-cli-uapp-retention` / `umeng-cli-uapp-event` |
| iOS App（`iphone`） | ❌ | **不适用**，同上 |

> ⚠️ **本 Skill 全部接口为只读查询**，无写入风险；事件创建 / 小程序数据源创建 / 页面别名编辑等写入接口不在本 Skill 范围内（如需请用 `umeng-cli-uapp-event-manage`）。

当用户对 Android / iOS App 询问概况 / 留存 / 事件时，应明确告知：「本 Skill 仅限小程序 / H5 / 小游戏；App 的对应能力请用 `umeng-cli-uapp-core-index` / `umeng-cli-uapp-retention` / `umeng-cli-uapp-event`」。

## 前置安装 & 鉴权

```bash
# 1. 安装 umeng-cli（若未安装）
npm install -g @umengfe/umeng-cli

# 2. 登录（首次使用） —— AI Agent 请以「后台模式」(is_background: true) 运行
umeng-cli login --no-qr
# 登录后 AK/SK 自动加密缓存；后续调用无需手动配置

# 3. 验证（可选）
umeng-cli call '{"name":"umeng.umini.getAppList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getAppList","authType":"umeng-aksk"}}' '{}'
```

### 登录要求

当接口返回未登录或登录态过期时，需要执行 `umeng-cli login --no-qr` 进行登录。

**AI Agent 执行登录的正确方式：**

> `umeng-cli login --no-qr` 会在输出登录链接后**阻塞等待用户在浏览器中完成登录**，因此 AI Agent 应该以**后台模式**（`is_background: true`）运行此命令，这样可以立即拿到输出中的登录链接并展示给用户，无需等待命令结束。命令会在用户完成登录后自动退出并保存凭证。

如果终端不支持显示二维码（如 AI Agent 终端、SSH 远程终端等），可以使用 `--no-qr` 参数，仅输出可点击的登录链接：

```bash
umeng-cli login --no-qr

# 输出:
# 🔄 正在生成登录链接...
# ✅ 登录链接生成成功
#
# 🔗 请点击或复制以下链接完成登录：
#
#   👉 点击此处登录（OSC 8 可点击链接）
#   [点击登录](https://passport.umeng.com/login?redirectURL=...)
#   https://passport.umeng.com/login?redirectURL=...
#
# ⏳ 等待登录...
# ✅ 授权成功！
# ✅ 登录完成！
```

## 接口速查表（12 个，全只读）

| # | 接口 | 类型 | 典型用途 | H5 支持 |
|---|---|---|---|---|
| 1 | `umeng.umini.getOverview` | 📖 只读 | 应用概况（启动 / 活跃 / 新增 / 访次 / 停留时长） | ⚠️ 部分字段不支持 |
| 2 | `umeng.umini.getTotalUser` | 📖 只读 | 累计用户数 | ✅ |
| 3 | `umeng.umini.getRetentionByDataSourceId` | 📖 只读 | 留存（日 / 周，新增 / 活跃，留存率 / 人数，v1–v30 共 9 个窗口） | ✅ |
| 4 | `umeng.umini.getVisitPageList` | 📖 只读 | 受访页面列表（Top 页面） | ⚠️ `pageDuration` 不支持 |
| 5 | `umeng.umini.getLandingPageList` | 📖 只读 | 入口页面列表（带跳出率） | ⚠️ 整体不支持 |
| 6 | `umeng.umini.getShareOverview` | 📖 只读 | 分享概况（趋势：次数 / 人数 / 新增 / 回流） | ⚠️ `reflowRatio` 不支持 |
| 7 | `umeng.umini.getSharePageOverview` | 📖 只读 | 页面分享数据 | ⚠️ `reflowRatio` 不支持 |
| 8 | `umeng.umini.getShareUserList` | 📖 只读 | 分享用户列表 | ✅ |
| 9 | `umeng.umini.getEventList` | 📖 只读 | 自定义事件列表 | ✅ |
| 10 | `umeng.umini.getEventOverview` | 📖 只读 | 某事件统计（count / device 趋势） | ✅ |
| 11 | `umeng.umini.getEventProvertyList` | 📖 只读 | 某事件属性列表 | ✅ |
| 12 | `umeng.umini.getAllPropertyValueCount` | 📖 只读 | 某事件属性下属性值分布 | ✅ |

> 注意接口名 `getEventProvertyList` 中 **`Proverty`** 为官方文档原文拼写（非 Property），调用时须严格照用。

## 公共枚举

- **`dataSourceId`**：数据源 ID，等同于小程序 `appkey`，所有接口必填
- **`timeUnit`**（时间颗粒度，**各接口支持范围不同**，详见各接口说明）：
  - 接口 1 `getOverview`：`5min` / `hour` / `day` / `7day` / `30day`
  - 接口 3 `getRetentionByDataSourceId`：仅 `day` / `week`
  - 接口 4-8 列表类：`day` / `7day` / `30day`
  - 接口 10 `getEventOverview`：`day`（默认且唯一）
  - 接口 12 `getAllPropertyValueCount`：仅 `day`
- **`fromDate` / `toDate`**：`yyyy-MM-dd`
- **`pageIndex` / `pageSize`**：小程序命名空间统一使用 `pageIndex` / `pageSize`（⚠️ 与 App 接口的 `page` / `perPage` 不同），`pageSize` 默认 30
- **`direction`**：`desc`（降序，默认）/ `asc`（升序）
- **留存 `indicator`**：`newUser`（新增用户，默认）/ `activeUser`（活跃用户）——区分大小写
- **留存 `valueType`**：`rate`（留存率，默认）/ `num`（留存人数）

## H5 局限汇总

| 接口 | H5 不支持的字段 / 行为 |
|---|---|
| `getOverview` | `launch`、`onceDuration`、`dailyDuration` |
| `getVisitPageList` | `pageDuration`（平均页面访问时长） |
| `getLandingPageList` | **整体 H5 不支持**（官方文档标注） |
| `getShareOverview` | `reflowRatio`（回流比） |
| `getSharePageOverview` | `reflowRatio`（分享回流比） |

## 数据延迟提示（留存）

- **day 粒度**：昨日留存需**次日**才能生成，默认查询使用 `last_7_days` 避免空返
- **week 粒度**：某周的留存率需**该周结束后**才逐步生成，**未完成的周不会出现在结果中**

---

## 接口 1：`umeng.umini.getOverview` — 应用概况数据

查询小程序应用级概况指标：启动、活跃、新增、访次、次均停留时长、人均停留时长。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `fromDate` | String | 是 | 开始时间 `yyyy-MM-dd` |
| `toDate` | String | 是 | 结束时间 `yyyy-MM-dd` |
| `timeUnit` | String | 是 | `5min` / `hour` / `day` / `7day` / `30day` |
| `indicators` | String | 是 | 指标列表（逗号分隔）：`newUser` / `activeUser` / `launch`（H5❌）/ `visitTimes` / `onceDuration`（H5❌）/ `dailyDuration`（H5❌） |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页条数（默认 30） |

**调用示例：**

```bash
umeng-cli call '{"name":"umeng.umini.getOverview","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getOverview","authType":"umeng-aksk"}}' '{"dataSourceId":"<APPKEY>","fromDate":"2026-04-21","toDate":"2026-04-27","timeUnit":"day","indicators":"newUser,activeUser,visitTimes"}'
```

**返回要点：**

- `data.data[]`：`dateTime` / `newUser` / `activeUser` / `launch` / `visitTimes` / `onceDuration` / `dailyDuration`
- `data.data[]` 按 `dateTime` 降序排列（`data[0]`=末期，`data[-1]`=初期）

---

## 接口 2：`umeng.umini.getTotalUser` — 累计用户数

查询小程序截至某日期的累计用户数（历史总去重用户数）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `fromDate` | String | 是 | 开始时间 `yyyy-MM-dd` |
| `toDate` | String | 是 | 结束时间 `yyyy-MM-dd` |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页条数（默认 30） |

**调用示例：**

```bash
umeng-cli call '{"name":"umeng.umini.getTotalUser","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getTotalUser","authType":"umeng-aksk"}}' '{"dataSourceId":"<APPKEY>","fromDate":"2026-04-27","toDate":"2026-04-27"}'
```

**返回要点：** `data[]` 每项 `dateTime` + `totalUser`（Long，累计用户数）。

---

## 接口 3：`umeng.umini.getRetentionByDataSourceId` — 留存数据

查询小程序留存率或留存人数，一次返回 9 个留存窗口（v1/v2/v3/v4/v5/v6/v7/v14/v30）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `fromDate` | String | 是 | 开始时间 `yyyy-MM-dd` |
| `toDate` | String | 是 | 结束时间 `yyyy-MM-dd` |
| `timeUnit` | String | 是 | `day` / `week`（仅此两档） |
| `valueType` | String | 是 | `rate`（留存率）/ `num`（留存数） |
| `indicator` | String | 否 | `newUser`（默认）/ `activeUser` —— 区分大小写 |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页条数（默认 10，API 单页固定 10 条） |

**调用示例：**

```bash
# 新增用户日留存率（过去 7 天）
umeng-cli call '{"name":"umeng.umini.getRetentionByDataSourceId","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getRetentionByDataSourceId","authType":"umeng-aksk"}}' '{"dataSourceId":"<APPKEY>","fromDate":"2026-04-21","toDate":"2026-04-27","timeUnit":"day","valueType":"rate","indicator":"newUser"}'
```

**留存窗口字段映射：**

| 字段 | 含义（timeUnit=day） | 含义（timeUnit=week） |
|---|---|---|
| `value` | 当日新增 / 活跃用户基数 | 当周新增 / 活跃用户基数 |
| `v1` | 次 1 日留存 | 次 1 周留存 |
| `v2` | 次 2 日留存 | 次 2 周留存 |
| `v3` | 次 3 日留存 | 次 3 周留存 |
| `v4` | 次 4 日留存 | 次 4 周留存 |
| `v5` | 次 5 日留存 | 次 5 周留存 |
| `v6` | 次 6 日留存 | 次 6 周留存 |
| `v7` | 次 7 日留存 | 次 7 周留存 |
| `v14` | 次 14 日留存 | 次 14 周留存 |
| `v30` | 次 30 日留存 | 次 30 周留存 |

> ⚠️ **数据延迟陷阱**：day 粒度昨日留存需次日才生成；week 粒度未完成周不返回；**大范围查询需按 `pageIndex` 分页累加**（每页固定 10 条）。

---

## 接口 4：`umeng.umini.getVisitPageList` — 受访页面列表

查询 Top N 受访页面，返回页面访问次数 / 用户数 / 平均访问时长。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `timeUnit` | String | 是 | `day` / `7day` / `30day` |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `orderBy` | String | 否 | `visitTimes` / `visitUser` / `pageDuration`（H5❌） |
| `direction` | String | 否 | `desc`（默认）/ `asc` |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页记录数（默认 30） |

**返回要点：** `data.data[]`：`page`（URL）、`displayName`（备注）、`visitTimes`、`visitUser`、`pageDuration`（H5❌）。

---

## 接口 5：`umeng.umini.getLandingPageList` — 入口页面列表

查询 Top N 入口页面，带跳出率。⚠️ **H5 整体不支持**。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `timeUnit` | String | 是 | `day` / `7day` / `30day` |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `orderBy` | String | 否 | `visitTimes` / `visitUser` / `jumpRatio` |
| `direction` | String | 否 | `desc`（默认）/ `asc` |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页条数（默认 30） |

**返回要点：** `data.data[]`：`page`、`displayName`、`visitTimes`（入口页次数）、`visitUser`（入口页人数）、`jumpRatio`（跳出率）。

---

## 接口 6：`umeng.umini.getShareOverview` — 分享概况

查询分享趋势数据：分享次数 / 人数 / 分享新增 / 回流。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `timeUnit` | String | 是 | `day` / `7day` / `30day` |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页记录数（默认 30） |

**返回要点：** `data.data[]`：`dateTime`、`count`（分享次数）、`user`（分享人数）、`newUser`（分享新增）、`reflow`（分享回流量）、`reflowRatio`（回流比，H5❌）。

---

## 接口 7：`umeng.umini.getSharePageOverview` — 页面分享数据

查询按页面维度的分享指标排行。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `timeUnit` | String | 是 | `day` / `7day` / `30day` |
| `orderBy` | String | 否 | `user`（默认）/ `count` / `reflow` / `newUser` |
| `direction` | String | 否 | `desc`（默认）/ `asc` |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页记录数（默认 30） |

**返回要点：** `data.data[]`：`path`（页面 URL）、`count`、`user`、`newUser`、`reflow`、`reflowRatio`（H5❌）。

---

## 接口 8：`umeng.umini.getShareUserList` — 分享用户列表

查询 Top N 分享用户（含头像 / 昵称）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `timeUnit` | String | 是 | `day` / `7day` / `30day` |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `orderBy` | String | 否 | `count`（默认）/ `reflow` / `newUser` |
| `direction` | String | 否 | `desc`（默认）/ `asc` |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页记录数（默认 30） |

**返回要点：** `data.data[]`：`userId`、`nickName`、`avatarUrl`、`count`（分享次数）、`reflow`、`newUser`、`reflowRatio`。

---

## 接口 9：`umeng.umini.getEventList` — 自定义事件列表

查询小程序已定义的自定义事件清单（`eventName` + `displayName`）。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |

**调用示例：**

```bash
umeng-cli call '{"name":"umeng.umini.getEventList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getEventList","authType":"umeng-aksk"}}' '{"dataSourceId":"<APPKEY>"}'
```

**返回要点：** `data[]`：`eventName`、`displayName`。

> 💡 事件的**创建**（写入）归 `umeng-cli-uapp-event-manage`；本 Skill 只查询。

---

## 接口 10：`umeng.umini.getEventOverview` — 某事件统计数据

查询指定事件的触发次数与触发用户数趋势。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `eventName` | String | 是 | 事件名（从接口 9 获取） |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `timeUnit` | String | 是 | `day`（默认且唯一） |

**返回要点：** `data.data[]`：`dateTime`、`count`（触发次数）、`device`（触发用户数）。

---

## 接口 11：`umeng.umini.getEventProvertyList` — 事件属性列表

查询指定事件已定义的属性名清单。⚠️ 官方接口名拼写为 **`Proverty`**（非 Property），须严格照用。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `eventName` | String | 是 | 事件名 |

**返回要点：** `data[]` 每项仅 `propertyName` 一个字段（无显示名）。

---

## 接口 12：`umeng.umini.getAllPropertyValueCount` — 属性值分布

查询某事件某属性下全部属性值的触发次数分布。

**参数：**

| 参数 | 类型 | 必填 | 说明 |
|---|---|---|---|
| `dataSourceId` | String | 是 | 数据源 ID（AppKey） |
| `eventName` | String | 是 | 事件名 |
| `propertyName` | String | 是 | 属性名（从接口 11 获取） |
| `fromDate` | String | 是 | 开始时间 |
| `toDate` | String | 是 | 结束时间 |
| `timeUnit` | String | 是 | 仅 `day`（默认且唯一） |
| `pageIndex` | Integer | 否 | 页码（默认 1） |
| `pageSize` | Integer | 否 | 每页记录数（默认 30） |

**返回要点：** `data.data[]`：`propertyValue`（属性值）、`count`（次数）、`countRatio`（占比） + `totalCount` / `currentPage`。



---

## 工作流

### W1：查询小程序概况（"过去 7 天活跃怎么样？"）

1. 确认用户的小程序名称 → 通过 `umeng-cli-uapp-assets` 查到 `dataSourceId`
2. 判断 `platform` 是否为小程序 / H5 / 小游戏；若是 Android/iOS，退回 `umeng-cli-uapp-core-index`
3. 根据问法选择 `timeUnit`：
   - "昨天" → `day` + `fromDate=toDate=昨天`
   - "过去 7 天" → `day` + 7 日区间（按日逐条返回趋势）
4. 根据问法选择 `indicators`（H5 场景剔除 `launch` / `onceDuration` / `dailyDuration`）
5. 调 `getOverview`，`data.data[]` 为降序；用自然语言总结末期值 + 趋势

### W2：查询累计用户（"小程序总用户有多少？"）

1. 取 `dataSourceId`
2. 调 `getTotalUser`，`fromDate=toDate=目标日期`
3. 返回单点 `totalUser`

### W3：查询留存（"小程序新用户 7 日留存怎么样？"）

1. 取 `dataSourceId`
2. **默认使用 `last_7_days` 避免 day 粒度昨日空返**；周粒度需避开未完成周
3. 调 `getRetentionByDataSourceId`，一次返回 9 个窗口（v1–v30）
4. 按 `v1`（次日留存）最关键，解读为"v1 次日留存率 X%、v7 七日留存率 Y%"
5. 大范围需分页累加（API 单页固定 10 条）

**反例（常见误解）：**

- ❌ "v1" 理解为第 1 日留存（其实 v1 = **次 1 日**留存 = 次日留存）
- ❌ 周粒度问"本周留存"期望立即返回（实际需本周结束后才生成）

### W4：Top 页面分析（"哪些页面访问最多？"/"哪个入口页带来最多用户？"）

1. "受访排行" → `getVisitPageList`，`orderBy=visitTimes`（默认）/ `visitUser` / `pageDuration`（H5❌）
2. "入口排行" → `getLandingPageList`，`orderBy=visitTimes` / `visitUser` / `jumpRatio`
3. **⚠️ H5 应用询问入口页排行**：整体接口不支持，明确回复"`getLandingPageList` 整体 H5 不支持"
4. 取 Top 3 / Top 10，用 `displayName`（若有）否则 `page` 路径展示

### W5：分享分析（"分享数据怎么样？"）

1. 趋势："过去 7 天分享" → `getShareOverview`（按日返回 count/user/newUser/reflow）
2. 页面维度："哪些页面分享最多" → `getSharePageOverview`（`orderBy=user` 默认）
3. 用户维度："谁分享最多" → `getShareUserList`（`orderBy=count` 默认）
4. H5 场景提示 `reflowRatio` 字段不支持

### W6：自定义事件分析（三步链路）

**典型场景**：用户给事件**显示名**（如 "添加 AppKey 页按钮点击"）查询其趋势或属性值分布。

```text
Step 1：调 getEventList，遍历 data[] 匹配 displayName → 取 eventName
Step 2a（统计趋势）：调 getEventOverview，传 eventName + 日期区间
                    → 返回 dateTime/count/device 按日趋势
Step 2b（属性分析）：调 getEventProvertyList，传 eventName
                    → 返回 propertyName[] 清单
Step 3（属性值分布）：调 getAllPropertyValueCount，传 eventName + propertyName + 日期区间
                    → 返回 propertyValue/count/countRatio 分布
```

> ⚠️ 接口 11 名称拼写 `getEventProvertyList`（**Proverty** 非 Property），必须严格照用；接口 12 `timeUnit` 仅支持 `day`。

---

## 字段别名对照表（旧 `--xxx` → 新 CLI 参数）

| 旧 `uapp-umini` CLI 参数 | 对应新接口 + 参数 | 备注 |
|---|---|---|
| `--overview` | `getOverview` | 默认 `indicators` 传全部指标 |
| `--indicators visit,activeUser,newUser,launch,...` | `getOverview.indicators` | H5 剔除 `launch`/`onceDuration`/`dailyDuration` |
| `--total-user` | `getTotalUser` | 单日快照 `fromDate=toDate` |
| `--retention` | `getRetentionByDataSourceId` | 一次返回 v1–v30 共 9 窗口 |
| `--indicator newUser/activeUser` | `getRetentionByDataSourceId.indicator` | 区分大小写 |
| `--value-type rate/num` | `getRetentionByDataSourceId.valueType` | 默认 `rate` |
| `--time-unit day/week` | `getRetentionByDataSourceId.timeUnit` | 仅 2 档 |
| `--visit-pages` | `getVisitPageList` | |
| `--landing-pages` | `getLandingPageList` | H5 ❌ |
| `--order-by` / `--direction` | `orderBy` / `direction` | 直通 |
| `--page` / `--per-page` | `pageIndex` / `pageSize` | ⚠️ 小程序命名空间统一用 `pageIndex`/`pageSize`（非 App 的 `page`/`perPage`） |
| `--share-overview` | `getShareOverview` | |
| `--share-pages` | `getSharePageOverview` | |
| `--share-users` | `getShareUserList` | |
| `--list-events` | `getEventList` | |
| `--event-stats EVENT` | `getEventOverview` + `eventName` | |
| `--list-props EVENT` | `getEventProvertyList` + `eventName` | ⚠️ 注意 `Proverty` 拼写 |
| `--prop-values EVENT --prop PROP` | `getAllPropertyValueCount` + `eventName` + `propertyName` | `timeUnit=day` 唯一 |
| `--scene-stats` / `--list-scenes` / `--list-scenes-wx` | **已迁移** | 见「边界异常表」→ `umeng-cli-uapp-mini-channel` |

## 边界异常表

| 情形 | 处理方式 |
|---|---|
| 用户是 Android/iOS App 询问概况/留存/事件 | 拒绝执行并回复「本 Skill 仅限小程序 / H5 / 小游戏；App 请用 `umeng-cli-uapp-core-index` / `umeng-cli-uapp-retention` / `umeng-cli-uapp-event`」 |
| 询问"渠道来源排行 / 推广活动效果 / 场景值统计 / 微信场景值列表 wx_xxxx" | 改用 `umeng-cli-uapp-mini-channel`（覆盖 `getCustomerSourceOverview` / `getChannelOverview` / `getCampaignOverview` / `getSceneOverview` / `getSceneInfoList` 与微信 89 个场景值内置表） |
| 询问"创建推广链接" | 改用 `umeng-cli-uapp-campaign`（含 `createCampaign` 写入） |
| 询问"创建 / 批量创建小程序事件" | 改用 `umeng-cli-uapp-event-manage`（含 `batchCreateEvent` 写入） |
| 询问"H5 曝光元素 / H5 场景来源" | 本 Skill 未覆盖 `h5.getElementList` / `h5.getElementValueList` / `h5.getSceneOverview`；如需可直接 `umeng-cli call` 调用 |
| 询问"分组指标 / 层级分组树" | 本 Skill 未覆盖 `getMultiIndiceList` / `getMultiOverview` / `getMultiLevelTree`；如需可直接 `umeng-cli call` 调用 |
| H5 询问"入口页面排行" | `getLandingPageList` 整体 H5 不支持，回复该局限 |
| 昨日留存查询返回空 | 提示「day 粒度昨日留存次日才生成，建议改用 `last_7_days`」 |
| 周粒度留存某周空 | 提示「该周未完成，week 粒度需等该周结束后才返回」 |
| `eventName` / `propertyName` 输入为中文显示名 | 先走 W6 Step 1 → `getEventList`/`getEventProvertyList` 取得 `eventName`/`propertyName` 再调统计接口 |

## 与邻近 Skill 的边界

| 邻近 Skill | 分工 |
|---|---|
| `umeng-cli-uapp-mini-channel` | **小程序渠道 / 活动 / 场景分析**（5 只读接口）。场景值统计 / 微信 89 场景值内置表归该 Skill，本 Skill 不涉及 |
| `umeng-cli-uapp-campaign` | **小程序推广链接创建**（1 写 + 1 读）。推广链接**创建**归该 Skill；本 Skill 只做应用级查询，不涉及推广创建 |
| `umeng-cli-uapp-event-manage` | **小程序事件创建**（`batchCreateEvent` 写）。事件**定义/创建/编辑**归该 Skill；本 Skill **只做事件查询与统计**（列表 / 趋势 / 属性 / 属性值分布） |
| `umeng-cli-uapp-event` | **App 自定义事件查询**（`com.umeng.uapp.event.*` 命名空间）。与本 Skill 的 `com.umeng.umini.*` 事件接口**独立不冲突** |
| `umeng-cli-uapp-retention` | **App 留存查询**（`umeng.uapp.getRetentions`）。与本 Skill 的 `getRetentionByDataSourceId`（小程序）**独立不冲突** |
| `umeng-cli-uapp-core-index` | **App 核心指标**（DAU / 新增 / 启动 / 时长）。本 Skill 的 `getOverview` / `getTotalUser` 是其小程序对应版 |
| `umeng-cli-uapp-assets` | **应用资产列表**（`getAppCount` / `getAppList` / `umini.getAppList`）。从中取得 `dataSourceId` 后作为本 Skill 输入 |

## 历史产物说明

- 旧 `uapp-umini`（Python 脚本 + `umeng-config.json`）仍保留于 `skills/uapp-umini/` 及 `skills/uapp-umini-1.1.0.zip`，作为历史版兼容；
- 本 Skill 与旧 `uapp-umini` **能力完全等价**（零能力扩展）：覆盖旧 SKILL 的概况 / 累计用户 / 留存 / 页面分析 / 分享分析 / 自定义事件共 12 个接口，仅做调用形态（CLI 化）与鉴权（`umeng-aksk`）的升级；
- 场景分析类能力（`--scene-stats` / `--list-scenes` / `--list-scenes-wx`）已迁移至 `umeng-cli-uapp-mini-channel`，不在本 Skill 承载。

## 快速自检清单

- [ ] `platform` 属于小程序 / H5 / 小游戏？若为 Android/iOS App，已引导退回 `umeng-cli-uapp-core-index` / `umeng-cli-uapp-retention` / `umeng-cli-uapp-event`
- [ ] `dataSourceId`（= AppKey）已获取？
- [ ] `timeUnit` 符合所用接口的支持档位？（接口 3 仅 `day/week`；接口 10/12 仅 `day`）
- [ ] H5 场景已剔除 `launch` / `onceDuration` / `dailyDuration` / `pageDuration` / `reflowRatio` 等字段，且对 `getLandingPageList` 整体不支持做了处理？
- [ ] 留存查询范围已避开"昨日 day 粒度"与"未完成周"？
- [ ] 查询事件统计/属性值时已先走 `getEventList` / `getEventProvertyList` 拿到 `eventName` / `propertyName`？
- [ ] 分页参数使用 `pageIndex` / `pageSize`（非 App 的 `page` / `perPage`）？
