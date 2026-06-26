---
name: umeng-cli-uapp-channel-version
description: 友盟 U-App 渠道/版本分析技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 5 个只读查询接口，涵盖渠道/版本单日快照与渠道/版本的启动次数、活跃用户、新增用户趋势分析。当用户需要查询各渠道或版本表现对比、单个渠道/版本的趋势时使用。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟 U-App 渠道/版本分析技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

查询友盟 U-App（移动统计）在**渠道维度**与**版本维度**的统计数据，覆盖两个场景：

- **单日快照**：指定日期的渠道/版本表现排名（活跃/新增/启动/总用户占比等）
- **趋势分析**：指定渠道/版本在一段时间内的启动次数、活跃用户、新增用户趋势

共 **5 个只读查询接口**。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-channel-version"}'
> ```
>
> **Appkey 维度打点：** 当本轮任务中出现 Appkey 的输入操作时，在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-channel-version", "appkey":"<输入的Appkey>"}'
> ```
> 同一 Appkey 在同一会话中只打一次；若用户切换到新的 Appkey，需对新的 Appkey 再打一次。

## 前置条件：安装 umeng-cli

本 Skill 的所有调用都依赖 `umeng-cli` 命令行工具。使用本 Skill 前，请先确保已在本机安装。

### 检查是否已安装

```bash
umeng-cli --version
```

若提示 `command not found` 或类似错误，按下述方式安装。

### 安装方式

```bash
# 方式一：通过 npm 安装（推荐，自动安装 CLI + 内置 Skills）
npm install -g @umengfe/umeng-cli

# 方式二：通过官方安装脚本（仅安装 CLI 二进制 + Skills）
curl -fsSL https://raw.githubusercontent.com/umeng/umeng-cli/main/scripts/install.sh | sh
```

安装完成后再次运行 `umeng-cli --version` 验证。

> 更多安装说明、卸载、账号管理等参考 [umeng-cli SKILL](../../../umeng-cli/SKILL.md) 或项目主页 https://github.com/umeng/umeng-cli

## 适用场景与触发词

- 用户询问各渠道或版本的单日表现对比（Top N、排名）
- 用户询问某个渠道/版本过去 N 天的趋势
- 用户询问新版本上线后用户表现
- 关键词：渠道分析、版本分析、渠道对比、版本对比、哪个渠道、哪个版本、渠道排名、版本表现、渠道趋势、版本趋势、新版本对比

## 鉴权方式

- **authType**: `umeng-aksk`（友盟 OpenAPI AK/SK 签名，HMAC-SHA1）
- **baseUrl**: `https://gateway.open.umeng.com/openapi`
- **endpoint 路径规则**: `param2/1/com.umeng.uapp/<接口名>`
- AK/SK 由 `umeng-cli login` 自动获取并加密缓存，无需手动配置 `apiKey` / `apiSecurity`

### 登录状态检查

```bash
umeng-cli whoami
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

### 获取 appkey

所有接口均以 `appkey` 作为应用维度标识。

**获取路径**：
1. 直接要求用户提供 `appkey`
2. 若用户不知道，引导至友盟官网 https://www.umeng.com/ 登录后在应用管理后台复制
3. （进阶）可调用同 namespace 的 `umeng.uapp.getAppList` 搜索获取

## 通用调用格式

```bash
umeng-cli call '{
  "name": "umeng.uapp.<接口名>",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.<接口名>",
    "authType": "umeng-aksk"
  }
}' '<参数JSON>'
```

- 本 Skill 的 5 个接口均为 `GET` 方法
- `endpoint` 路径遵循统一格式 `param2/1/com.umeng.uapp/<接口名>`

## 接口路由表

### 单日快照（渠道/版本当日排名）

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getChannelData` | `param2/1/com.umeng.uapp/umeng.uapp.getChannelData` | 获取渠道维度单日统计数据（含分页） |
| `umeng.uapp.getVersionData` | `param2/1/com.umeng.uapp/umeng.uapp.getVersionData` | 获取版本维度单日统计数据（无分页） |

### 趋势分析（按时间范围 + 渠道/版本过滤）

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getLaunchesByChannelOrVersion` | `param2/1/com.umeng.uapp/umeng.uapp.getLaunchesByChannelOrVersion` | 按渠道/版本条件获取启动次数趋势 |
| `umeng.uapp.getActiveUsersByChannelOrVersion` | `param2/1/com.umeng.uapp/umeng.uapp.getActiveUsersByChannelOrVersion` | 按渠道/版本条件获取活跃用户数趋势 |
| `umeng.uapp.getNewUsersByChannelOrVersion` | `param2/1/com.umeng.uapp/umeng.uapp.getNewUsersByChannelOrVersion` | 按渠道/版本条件获取新增用户数趋势 |

> 💡 **服务端无排序参数**：5 个接口均不支持 `sort-by` / `top`，排序与 Top N 由客户端（LLM 侧）在返回数据上完成。

---

## 操作

### 1. 获取渠道维度单日统计数据 (getChannelData)

获取指定 App 按照分发渠道维度的单日统计数据，支持分页。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| date | string | 是 | - | 查询日期，格式 `yyyy-MM-dd` |
| page | integer | 否 | 1 | 页号，从 1 开始 |
| perPage | integer | 否 | 10 | 每页显示数量（最大 100） |

**调用示例：**

```bash
# 查询 2025-04-27 各渠道前 50 条
umeng-cli call '{
  "name": "umeng.uapp.getChannelData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getChannelData",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","date":"2025-04-27","perPage":50,"page":1}'
```

**返回格式：**

```json
{
  "channelInfos": [
    {
      "date": "2025-04-27",
      "channel": "Umeng",
      "id": "xxx",
      "activeUser": 311,
      "newUser": 15,
      "totalUser": 928529,
      "totalUserRate": 0.62,
      "launch": 2579,
      "duration": "xxx"
    }
  ],
  "totalPage": 3,
  "page": 1
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `channelInfos[].date` | string | 日期 |
| `channelInfos[].channel` | string | 渠道名称 |
| `channelInfos[].id` | string | 渠道 ID |
| `channelInfos[].activeUser` | integer | 活跃用户 |
| `channelInfos[].newUser` | integer | 新增用户 |
| `channelInfos[].totalUser` | integer | 当前渠道总用户数 |
| `channelInfos[].totalUserRate` | double | 当前渠道总用户数占总用户数的比例 |
| `channelInfos[].launch` | integer | 启动数（昨日及以前可查询） |
| `channelInfos[].duration` | string | 使用时长（昨日及以前可查询） |
| `page` | integer | 当前页数 |
| `totalPage` | integer | 总页数 |

---

### 2. 获取版本维度单日统计数据 (getVersionData)

获取指定 App 按照版本维度的单日统计数据。

**参数说明：**

| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| appkey | string | 是 | 应用 ID |
| date | string | 是 | 查询日期，格式 `yyyy-MM-dd` |

> ⚠️ **本接口不支持分页参数**（`page` / `perPage`），官方文档仅定义 `appkey` 与 `date` 两个必填。

**调用示例：**

```bash
umeng-cli call '{
  "name": "umeng.uapp.getVersionData",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getVersionData",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","date":"2025-04-27"}'
```

**返回格式：**

```json
{
  "versionInfos": [
    {
      "date": "2025-04-27",
      "version": "2.0.11001",
      "activeUser": 261,
      "newUser": 2,
      "totalUser": 306487,
      "totalUserRate": 0.18
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `versionInfos[].date` | string | 统计日期 |
| `versionInfos[].version` | string | 版本号 |
| `versionInfos[].activeUser` | integer | 活跃用户 |
| `versionInfos[].newUser` | integer | 新增用户 |
| `versionInfos[].totalUser` | integer | 当前版本总用户数 |
| `versionInfos[].totalUserRate` | double | 当前版本总用户数占总用户数的比例 |

> ⚠️ **版本单日快照无启动次数**：`VersionInfo` 结构中**不含** `launch` / `duration` 字段（与 `ChannelInfo` 不同）。如需"按版本看启动趋势"，请改用 `getLaunchesByChannelOrVersion` + `versions` 参数。

---

### 3. 按渠道/版本获取启动次数趋势 (getLaunchesByChannelOrVersion)

获取指定 App 某个时间范围内按渠道或版本的启动次数。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 查询起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 查询截止日期 `yyyy-MM-dd` |
| periodType | string | 是 | `daily` | `daily`（按日）/ `weekly`（按周）/ `monthly`（按月） |
| channels | string | 否 | - | 渠道名称，**仅一个**；含特殊字符时需 urlEncode |
| versions | string | 否 | - | 版本名称，**仅一个**；含特殊字符时需 urlEncode |

**调用示例：**

```bash
# 示例 A：全渠道/全版本按日启动趋势
umeng-cli call '{
  "name": "umeng.uapp.getLaunchesByChannelOrVersion",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getLaunchesByChannelOrVersion",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2025-04-21","endDate":"2025-04-27","periodType":"daily"}'

# 示例 B：查询 "App Store" 渠道近 7 天启动趋势（渠道名 urlEncode）
umeng-cli call '{
  "name": "umeng.uapp.getLaunchesByChannelOrVersion",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getLaunchesByChannelOrVersion",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2025-04-21","endDate":"2025-04-27","periodType":"daily","channels":"App%20Store"}'
```

**返回格式：**

```json
{
  "launchInfo": [
    {
      "date": "2025-04-21",
      "value": 2579,
      "dailyValue": [
        {"name": "App Store", "value": 1200}
      ],
      "hourValue": []
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `launchInfo[].date` | string | 统计日期 |
| `launchInfo[].value` | integer | 无渠道/无版本按天、按周、按月汇总值 |
| `launchInfo[].dailyValue[]` | NameValue[] | 指定 channels/versions 时按渠道/版本的明细（`name` + `value`） |
| `launchInfo[].hourValue[]` | integer[] | 按小时查询时返回（本 Skill 不使用） |

---

### 4. 按渠道/版本获取活跃用户数趋势 (getActiveUsersByChannelOrVersion)

获取指定 App 某个时间范围内按渠道或版本的活跃用户数。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 查询起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 查询截止日期 `yyyy-MM-dd` |
| periodType | string | 是 | `daily` | `daily` / `weekly` / `monthly` |
| channels | string | 否 | - | 渠道名称，**仅一个**；**需 urlEncode 转义** |
| versions | string | 否 | - | 版本名称，**仅一个**；**需 urlEncode 转义** |

**调用示例：**

```bash
# 查询 "华为" 渠道近 7 天活跃用户趋势
umeng-cli call '{
  "name": "umeng.uapp.getActiveUsersByChannelOrVersion",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getActiveUsersByChannelOrVersion",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2025-04-21","endDate":"2025-04-27","periodType":"daily","channels":"%E5%8D%8E%E4%B8%BA"}'
```

**返回格式：**

```json
{
  "activeUserInfo": [
    {
      "date": "2025-04-21",
      "value": 0,
      "dailyValue": [
        {"name": "华为", "value": 311}
      ],
      "hourValue": []
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `activeUserInfo[].date` | string | 统计日期 |
| `activeUserInfo[].value` | integer | 无渠道/无版本汇总值 |
| `activeUserInfo[].dailyValue[]` | NameValue[] | 指定渠道/版本时的明细 |
| `activeUserInfo[].hourValue[]` | integer[] | 按小时查询时返回 |

---

### 5. 按渠道/版本获取新增用户数趋势 (getNewUsersByChannelOrVersion)

获取指定 App 某个时间范围内按渠道或版本的新增用户数。

**参数说明：**

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| appkey | string | 是 | - | 应用 ID |
| startDate | string | 是 | - | 查询起始日期 `yyyy-MM-dd` |
| endDate | string | 是 | - | 查询截止日期 `yyyy-MM-dd` |
| periodType | string | 是 | `daily` | `daily` / `weekly` / `monthly` |
| channels | string | 否 | - | 渠道名称，**仅一个**；**需 urlEncode 转义** |
| versions | string | 否 | - | 版本名称，**仅一个**；**需 urlEncode 转义** |

**调用示例：**

```bash
# 查询 3.5 版本近 30 天新增用户趋势
umeng-cli call '{
  "name": "umeng.uapp.getNewUsersByChannelOrVersion",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getNewUsersByChannelOrVersion",
    "authType": "umeng-aksk"
  }
}' '{"appkey":"你的appkey","startDate":"2025-03-29","endDate":"2025-04-27","periodType":"daily","versions":"3.5"}'
```

**返回格式：**

```json
{
  "newUserInfo": [
    {
      "date": "2025-03-29",
      "value": 0,
      "dailyValue": [
        {"name": "3.5", "value": 15}
      ],
      "hourValue": []
    }
  ]
}
```

**返回字段说明：**

| 字段 | 类型 | 说明 |
|------|------|------|
| `newUserInfo[].date` | string | 统计日期 |
| `newUserInfo[].value` | integer | 无渠道/无版本汇总值 |
| `newUserInfo[].dailyValue[]` | NameValue[] | 指定渠道/版本时的明细 |
| `newUserInfo[].hourValue[]` | integer[] | 按小时查询时返回 |

---

## 公共枚举与约束

### periodType 枚举

| 值 | 含义 |
|----|------|
| `daily` | 按日（默认，可省略显式传入） |
| `weekly` | 按周 |
| `monthly` | 按月 |

> 对于三个 `ByChannelOrVersion` 趋势接口，`periodType` 官方标注为必填且默认 `daily`。实际调用中建议显式传入以避免歧义。

### 日期格式

- `date` / `startDate` / `endDate` 统一使用 `yyyy-MM-dd`
- "今日"数据请改用 `umeng.uapp.getTodayData`（不在本 Skill 范围内）

### channels / versions 单值限制

- 三个趋势接口的 `channels` 与 `versions` 参数**每次仅能传一个值**
- 如需对比多个渠道/版本，需多次调用后由客户端聚合

### urlEncode 规则

- 含空格、中文、特殊字符的渠道名/版本号需做 URL 编码（percent-encoding）
- 例：`App Store` → `App%20Store`；`华为` → `%E5%8D%8E%E4%B8%BA`
- 纯英文字母/数字/点号（如 `Umeng`、`3.5`、`1.0.0`）**无需**编码
- 三个 `ByChannelOrVersion` 接口统一按此规则处理

### 分页

- `getChannelData` 支持 `page`（默认 1）+ `perPage`（默认 10，最大 100），响应含 `totalPage`
- `getVersionData` **不支持分页**
- 三个趋势接口不支持分页

## 时间范围换算参考

| 常用语义 | startDate | endDate |
|----------|-----------|---------|
| `yesterday` | 昨天 | 昨天 |
| `last_7_days` | 今天 - 7 | 昨天 |
| `last_30_days` | 今天 - 30 | 昨天 |
| `last_90_days` | 今天 - 90 | 昨天 |

## 典型工作流

### 场景 1：单日渠道 Top N 对比

```
需求："各渠道昨天的新增用户对比？"
1. getChannelData(appkey, date=yesterday, perPage=100)
   → 拿到当日所有渠道的 channelInfos[]
2. 客户端（LLM）按 newUser 字段降序排序
3. 取 Top N（默认 5），输出表格：排名 / 渠道 / 新增 / 活跃 / 启动 / 总用户
```

### 场景 2：单日版本表现

```
需求："各版本活跃用户排名？"
1. getVersionData(appkey, date=yesterday)
   → 拿到所有版本的 versionInfos[]
2. 客户端按 activeUser 降序排序，取 Top N
3. 提醒：版本维度单日快照无启动数；如需启动趋势请走场景 4
```

### 场景 3：某渠道近 7 日趋势

```
需求："华为渠道过去一周的活跃用户怎样？"
1. 计算 startDate = today - 7, endDate = yesterday
2. 渠道名 urlEncode：华为 → %E5%8D%8E%E4%B8%BA
3. getActiveUsersByChannelOrVersion(
     appkey, startDate, endDate, periodType=daily,
     channels="%E5%8D%8E%E4%B8%BA"
   )
4. 读取 activeUserInfo[].dailyValue[0].value（渠道日值），绘制/输出趋势
5. 如需同时看新增：再调 getNewUsersByChannelOrVersion（参数一致）
   如需启动：再调 getLaunchesByChannelOrVersion（参数一致）
```

### 场景 4：新版本上线后对比

```
需求："3.5 版本上线后用户表现如何？"
1. 确认上线日期 → 设置 startDate = 上线日, endDate = yesterday
2. getNewUsersByChannelOrVersion(
     appkey, startDate, endDate, periodType=daily, versions="3.5"
   )
   → 观察新增用户增长曲线
3. getActiveUsersByChannelOrVersion(... versions="3.5") → 观察活跃走势
4. getLaunchesByChannelOrVersion(... versions="3.5") → 观察启动走势
5. 横向对比上一版本（例如 versions="3.4"），评估升级迁移效果
```

## 边界条件与错误处理

- **未说 App 名 / appkey**：先询问用户 appkey；若用户不知道，引导至友盟后台查询或调用 `umeng.uapp.getAppList`
- **appkey 无效**：响应非成功，提示「找不到该应用，请确认 appkey 是否正确或是否已开通 U-App」
- **渠道/版本名不存在**：`dailyValue` 为空数组；建议先不加 channels/versions 查全量，再挑选实际存在的名称
- **返回数据为空**：`channelInfos` / `versionInfos` 为空数组代表该日期暂无数据，提示「该日期暂无数据，建议换近期日期查询」
- **渠道/版本名含特殊字符忘记 urlEncode**：可能返回空结果或签名错误，要求对参数值做 URL 编码
- **服务端无排序参数**：5 个接口均不提供 `sort-by` / `top`，排序与 Top N 由客户端完成
- **`channels` / `versions` 传多个值**：接口仅接受单个值，多值请分多次调用
- **日期跨度过大**：服务端对返回数量有上限，如有限制按官方文档分段查询
- **未登录 / 登录态过期**：执行 `umeng-cli login --no-qr`（AI Agent 以后台模式运行并将链接展示给用户）

## 典型问法 → 接口/参数映射

| 典型问法 | 接口 | 关键参数 |
|----------|------|----------|
| "各渠道昨天的新增用户对比？" | `getChannelData` | `date=yesterday`，客户端按 `newUser` 排序 |
| "各版本活跃用户排名？" | `getVersionData` | `date=yesterday`，客户端按 `activeUser` 排序 |
| "华为渠道过去一周的活跃用户怎样？" | `getActiveUsersByChannelOrVersion` | `startDate/endDate` 最近 7 天，`periodType=daily`，`channels=%E5%8D%8E%E4%B8%BA` |
| "3.5 版本上线后用户表现如何？" | `getNewUsersByChannelOrVersion` + `getActiveUsersByChannelOrVersion` | 对应时间范围，`versions=3.5` |
| "Top 5 渠道的启动次数对比" | `getChannelData` | `date=yesterday`，客户端按 `launch` 降序取 5 |
| "Umeng 渠道昨天表现如何？" | `getChannelData` → 过滤 `channel=="Umeng"` | `date=yesterday` |

## 注意事项

- 本 Skill **仅限只读查询**，不包含 `umeng.uapp.createApp` / `umeng.uapp.event.create` 等写入类接口
- 所有接口均为 `GET` 方法
- `appkey` 到友盟官网 https://www.umeng.com/ 应用管理后台查询
- **`total_user`（总用户数）指标**：仅在"单日快照"场景下由 `getChannelData` / `getVersionData` 响应直接提供；**无独立的 total_user 趋势接口**，如需趋势请拼接多日快照
- **版本维度单日快照无 `launch` 字段**：`VersionInfo` 结构不含启动数；想看"某版本启动趋势"请走 `getLaunchesByChannelOrVersion` + `versions` 参数
- **服务端无排序参数**：排序与 Top N 由客户端完成
- **channels / versions 仅一个**：多个对比需多次调用
- **urlEncode**：含空格/中文/特殊字符的渠道与版本名需要 URL 编码
- `getVersionData` **不支持分页**（仅 `appkey` + `date`）；`getChannelData` 支持 `page`/`perPage`（最大 100）

## 快速参考

| 接口 | Endpoint（相对 baseUrl） | 必填参数 | 可选参数 | 分页 |
|------|--------------------------|----------|----------|------|
| `umeng.uapp.getChannelData` | `param2/1/com.umeng.uapp/umeng.uapp.getChannelData` | `appkey` + `date` | `page` / `perPage` | ✅ |
| `umeng.uapp.getVersionData` | `param2/1/com.umeng.uapp/umeng.uapp.getVersionData` | `appkey` + `date` | — | ❌ |
| `umeng.uapp.getLaunchesByChannelOrVersion` | `param2/1/com.umeng.uapp/umeng.uapp.getLaunchesByChannelOrVersion` | `appkey` + `startDate` + `endDate` + `periodType` | `channels` / `versions` | ❌ |
| `umeng.uapp.getActiveUsersByChannelOrVersion` | `param2/1/com.umeng.uapp/umeng.uapp.getActiveUsersByChannelOrVersion` | `appkey` + `startDate` + `endDate` + `periodType` | `channels` / `versions`（需 urlEncode） | ❌ |
| `umeng.uapp.getNewUsersByChannelOrVersion` | `param2/1/com.umeng.uapp/umeng.uapp.getNewUsersByChannelOrVersion` | `appkey` + `startDate` + `endDate` + `periodType` | `channels` / `versions`（需 urlEncode） | ❌ |

> 完整 uapp namespace 其他接口（如 `getDailyData` / `getYesterdayData` / `getRetentions` / `event.*` 等）请参考 [umeng-cli/reference/openapi/uapp.md](../../../umeng-cli/reference/openapi/uapp.md)。
