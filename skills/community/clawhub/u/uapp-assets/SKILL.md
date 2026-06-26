---
name: umeng-cli-uapp-assets
description: 友盟应用资产查询技能，支持通过 umeng-cli call 调用友盟 OpenAPI（gateway.open.umeng.com）的 3 个只读资产接口，覆盖 App 总数、App 列表、小程序列表及小程序总数查询（跨 com.umeng.uapp 与 com.umeng.umini 两个命名空间）。当用户需要查询"我有多少应用 / 列出我所有的 App / 我的小程序列表 / 应用资产概况"时使用。
metadata:
  requires:
    bins: ["umeng-cli"]
  cliHelp: "umeng-cli call --help"
  install: "npm install -g @umengfe/umeng-cli"
  homepage: "https://github.com/umeng/umeng-cli"
---

# 友盟应用资产查询技能

> `umeng-cli` 是友盟提供的命令行程序，所有操作通过执行 `umeng-cli call` 命令完成。

查询当前登录账号下的 **App 资产**（数量 / 列表）与 **小程序资产**（列表 / 数量），覆盖两类核心需求：

- **App 资产**：App 总数（一次调用直出）、App 列表（分页）
- **小程序资产**：小程序列表（分页，`totalCount` 随列表响应返回）

共 **3 个只读查询接口**，跨 2 个命名空间（`com.umeng.uapp` + `com.umeng.umini`）。本 Skill 为**资产发现型** —— `appkey` 是"输出"不是"输入"，无需用户提供任何应用标识即可工作。

> **埋点上报：** AI Agent 在阅读本 Skill 文档后，请执行以下命令进行调用埋点上报：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-assets"}'
> ```
>
> **Appkey 维度打点：** 本 Skill 为资产发现型，通常 Appkey 是**输出**而非输入；但若在任务上下文中出现 Appkey 的输入操作（例如用户主动提供某 Appkey 让你回查其归属），在拿到该 Appkey 之后、发起首个业务 API 调用之前，再追加执行一次带 appkey 的打点：
> ```bash
> umeng-cli trace '{"skill_name":"umeng-cli-uapp-assets", "appkey":"<输入的Appkey>"}'
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

- 用户询问"我一共注册了多少个应用？"
- 用户询问"列出我所有的 App / 我的 App 列表"
- 用户询问"我有多少小程序 / 我的小程序列表"
- 用户询问"同时列出我的 App 和小程序"
- 用户需要按平台（`android` / `iphone` / `mini_wechat` 等）过滤资产
- 用户在使用其他 skill 前需要先"发现"`appkey`
- 关键词：应用列表、App 列表、小程序列表、应用数量、小程序数量、应用资产、我的应用、我的小程序、有哪些 App、有哪些小程序

## 鉴权方式

- **authType**: `umeng-aksk`（友盟 OpenAPI AK/SK 签名，HMAC-SHA1）
- **baseUrl**: `https://gateway.open.umeng.com/openapi`
- **endpoint 路径规则**：`param2/1/com.umeng.uapp/<接口名>` 或 `param2/1/com.umeng.umini/<接口名>`
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

## 不需要 appkey

本 Skill **不接受 `appkey` 作为入参** —— 所有 3 个接口都以"当前登录账号"为作用域，返回账号下全部 App / 小程序。`appkey`（或小程序的 `dataSourceId`）是本 Skill 的**输出**，通常用作下游 Skill（`umeng-cli-uapp-core-index` / `umeng-cli-uapp-channel-version` / `umeng-cli-uapp-retention` / `umeng-cli-uapp-event` 等）的输入。

## 通用调用格式

```bash
umeng-cli call '{
  "name": "<接口名>",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/<namespace>/<接口名>",
    "authType": "umeng-aksk"
  }
}' '<参数JSON>'
```

- 3 个接口均为 `GET` 方法
- `<namespace>` 为 `com.umeng.uapp` 或 `com.umeng.umini`

## 核心概念

### 两命名空间并列

| 资产类型 | 命名空间 | 总数接口 | 列表接口 |
|---------|---------|----------|----------|
| App（Android / iOS） | `com.umeng.uapp` | `umeng.uapp.getAppCount`（**一次调用直出**） | `umeng.uapp.getAppList` |
| 小程序（微信 / 支付宝 / 字节 / 百度 / QQ / H5 等） | `com.umeng.umini` | 无独立总数接口，走 `getAppList.totalCount` | `umeng.umini.getAppList` |

### 分页参数差异表 ⚠️

**这是本 Skill 最容易出错的地方** —— 两个命名空间的分页参数名**完全不同**：

| 维度 | `umeng.uapp.getAppList` | `umeng.umini.getAppList` |
|------|-------------------------|--------------------------|
| 页码参数 | `page`（从 1 开始） | `pageIndex`（从 1 开始） |
| 页大小参数 | `perPage`（最大 100） | `pageSize`（默认 30） |
| 响应总页数 | `totalPage` ✅ | 无直接字段（由 `totalCount` 和 `pageSize` 客户端换算） |
| 响应总条数 | **无 `totalCount`** ❌（要取总数走 `getAppCount`） | `appListDTO.totalCount` ✅ |
| 响应当前页 | `page` | `appListDTO.currentPage` |
| 数据数组 | `appInfos[]`（根级） | `appListDTO.data[]`（嵌套一层） |

### 响应字段别名表

两个 `getAppList` 的 DTO 字段**语义相同但命名不同**，客户端合并列表时需做字段映射：

| 含义 | `uapp.getAppList.appInfos[]` | `umini.getAppList.appListDTO.data[]` |
|------|------------------------------|--------------------------------------|
| 唯一标识（即 AppKey） | `appkey` | `dataSourceId` |
| 应用名称 | `name` | `appName` |
| 平台 | `platform`（`android` / `iphone`） | `platform`（`mini_wechat` / `mini_alipay` / `mini_bytedance` / `mini_baidu` / `mini_qq` / `mini_game_wechat` / `html_5` 等） |
| 一级分类 | `category` | `firstLevel` |
| 二级分类 | 无 | `secondLevel` |
| 创建时间 | `createdAt` | `gmtCreate` |
| 更新时间 | `updatedAt` | 无 |
| 是否游戏 | `useGameSdk`（boolean） | 无（小程序通过 `mini_game_wechat` 等平台标识） |
| 是否关注 | `popular`（0/1） | 无 |
| 账号名 | 无 | `userName` |

## 接口路由表

| 接口 | Endpoint | 功能 |
|------|----------|------|
| `umeng.uapp.getAppCount` | `param2/1/com.umeng.uapp/umeng.uapp.getAppCount` | 获取账户下 App 总数（一次调用直出 `count`） |
| `umeng.uapp.getAppList` | `param2/1/com.umeng.uapp/umeng.uapp.getAppList` | 获取账户下 App 列表（分页，`page`/`perPage`） |
| `umeng.umini.getAppList` | `param2/1/com.umeng.umini/umeng.umini.getAppList` | 获取账户下小程序列表（分页，`pageIndex`/`pageSize`；响应含 `totalCount`） |

### 与本 skill 相邻能力的边界

| 能力 | 归属 Skill | 说明 |
|------|-----------|------|
| App 某日 / 趋势 DAU / 新增 / 启动等核心指标 | `umeng-cli-uapp-core-index` | 本 Skill 仅出"应用清单"，不出任何指标 |
| App 版本列表 / 渠道列表（按 appkey） | `umeng-cli-uapp-channel-version` | 本 Skill 仅管账户层级，不管 App 内部渠道/版本 |
| App 留存率 | `umeng-cli-uapp-retention` | — |
| App 自定义事件 | `umeng-cli-uapp-event` | — |
| APM（崩溃/性能） | `umeng-cli-uapm` | — |
| 小程序指标（`getOverview` / `getTotalUser` / `getRetentionByDataSourceId` 等） | 未来独立 `umeng-cli-umini-*` Skill | 本 Skill 仅覆盖小程序"清单+数量"，不覆盖小程序指标 |

---

## 操作

### 1. 获取 App 总数 (getAppCount)

获取当前账户下所有 App 的数量。**无需任何参数**，一次调用直出。

**参数说明**：无

**调用示例**：

```bash
umeng-cli call '{
  "name": "umeng.uapp.getAppCount",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getAppCount",
    "authType": "umeng-aksk"
  }
}' '{}'
```

**返回格式**：

```json
{
  "count": 893
}
```

**返回字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `count` | integer | 账户下 App 总数 |

> 💡 本接口是旧 `--count`（App）的直接等价实现；`getAppList` 无 `totalCount`，想拿 App 真实总数**只能**走本接口，不要用 `totalPage × perPage` 估算。

---

### 2. 获取 App 列表 (uapp.getAppList)

分页获取账户下 App 列表。

**参数说明**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| page | integer | 否 | 1 | 页号，从 1 开始 |
| perPage | integer | 否 | 10 | 每页记录数（**最大 100**） |

**调用示例**：

```bash
# 默认首页
umeng-cli call '{
  "name": "umeng.uapp.getAppList",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.uapp/umeng.uapp.getAppList",
    "authType": "umeng-aksk"
  }
}' '{}'

# 指定第 2 页，每页 100 条
umeng-cli call '{"name":"umeng.uapp.getAppList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.uapp/umeng.uapp.getAppList","authType":"umeng-aksk"}}' '{"page":2,"perPage":100}'
```

**返回格式**：

```json
{
  "appInfos": [
    {
      "appkey": "4f83c5d852701564c0000011",
      "name": "友盟SDK",
      "platform": "android",
      "category": "工具",
      "createdAt": "2012-04-10 10:00:00",
      "updatedAt": "2026-04-28 09:00:00",
      "useGameSdk": false,
      "popular": 1
    }
  ],
  "totalPage": 9,
  "page": 1
}
```

**返回字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `appInfos[].appkey` | string | 应用 ID（AppKey），下游 skill 的输入 |
| `appInfos[].name` | string | App 名称 |
| `appInfos[].platform` | string | 平台：`android` / `iphone` |
| `appInfos[].category` | string | 应用分类（单级） |
| `appInfos[].createdAt` | string | 创建时间 |
| `appInfos[].updatedAt` | string | 更新时间 |
| `appInfos[].useGameSdk` | boolean | 是否为游戏 |
| `appInfos[].popular` | integer | 是否关注（0/1） |
| `totalPage` | integer | 总页数 |
| `page` | integer | 当前页号 |

> ⚠️ **本接口响应没有 `totalCount` 字段**。若需要 App 总数，**必须**单独调 `getAppCount`，不要用 `(totalPage-1) × perPage + appInfos.length` 估算。

---

### 3. 获取小程序列表 (umini.getAppList)

分页获取账户下小程序列表。**响应同时返回小程序总数 `totalCount`**，因此不需要独立的"小程序数量"接口。

**参数说明**：

| 参数 | 类型 | 必填 | 默认值 | 说明 |
|------|------|------|--------|------|
| pageIndex | integer | 否 | 1 | 页号，从 1 开始（**注意不是 `page`**） |
| pageSize | integer | 否 | 30 | 每页记录数（**注意不是 `perPage`**） |

**调用示例**：

```bash
# 默认首页
umeng-cli call '{
  "name": "umeng.umini.getAppList",
  "api": {
    "method": "GET",
    "baseUrl": "https://gateway.open.umeng.com/openapi",
    "endpoint": "param2/1/com.umeng.umini/umeng.umini.getAppList",
    "authType": "umeng-aksk"
  }
}' '{}'

# 只为拿"小程序总数"：pageSize=1 足矣
umeng-cli call '{"name":"umeng.umini.getAppList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getAppList","authType":"umeng-aksk"}}' '{"pageIndex":1,"pageSize":1}'

# 正常分页（第 3 页，每页 100）
umeng-cli call '{"name":"umeng.umini.getAppList","api":{"method":"GET","baseUrl":"https://gateway.open.umeng.com/openapi","endpoint":"param2/1/com.umeng.umini/umeng.umini.getAppList","authType":"umeng-aksk"}}' '{"pageIndex":3,"pageSize":100}'
```

**返回格式**：

```json
{
  "data": {
    "data": [
      {
        "dataSourceId": "5e8c6dea978eea071c37c682",
        "appName": "示例小程序",
        "platform": "mini_wechat",
        "firstLevel": "公共交通与出行",
        "secondLevel": "公共交通",
        "gmtCreate": "2020-03-10 10:00:00",
        "userName": "alice@example.com"
      }
    ],
    "totalCount": 42,
    "currentPage": 1
  },
  "msg": "",
  "code": 0,
  "success": true
}
```

**返回字段说明**：

| 字段 | 类型 | 说明 |
|------|------|------|
| `data.data[].dataSourceId` | string | 小程序的 AppKey（下游 skill 的输入） |
| `data.data[].appName` | string | 小程序名称 |
| `data.data[].platform` | string | 小程序平台（见下文枚举表） |
| `data.data[].firstLevel` | string | 一级分类 |
| `data.data[].secondLevel` | string | 二级分类 |
| `data.data[].gmtCreate` | string | 创建时间 |
| `data.data[].userName` | string | 账号名 |
| `data.totalCount` | integer | **小程序总数**（一次调用即得） |
| `data.currentPage` | integer | 当前页号 |

> 💡 **想要小程序总数？** 传 `pageSize=1` 调一次本接口，直接读 `data.totalCount` 即可，无需翻页。

---

## 公共约束

### 分页差异速查（核心）

| 接口 | 页码字段 | 页大小字段 | 总数字段 | 数据数组路径 |
|------|----------|------------|----------|---------------|
| `uapp.getAppList` | `page` | `perPage`（最大 100） | **无**（走 `getAppCount`） | `appInfos[]`（根级） |
| `umini.getAppList` | `pageIndex` | `pageSize`（默认 30） | `data.totalCount` | `data.data[]`（嵌套） |
| `getAppCount` | — | — | `count`（直出） | — |

### 平台枚举与客户端过滤

本 Skill 接口**不支持服务端按平台过滤**。旧 skill 的 `--platform android/ios/mini` 由客户端后过滤实现。枚举参考：

| 过滤需求 | `uapp.appInfos[].platform` 取值 | `umini.data.data[].platform` 取值 |
|----------|----------------------------------|-----------------------------------|
| Android App | `android` | — |
| iOS App | `iphone` | — |
| 微信小程序 | — | `mini_wechat` |
| 支付宝小程序 | — | `mini_alipay` |
| 字节跳动小程序 | — | `mini_bytedance` |
| 百度小程序 | — | `mini_baidu` |
| QQ 小程序 | — | `mini_qq` |
| 微信小游戏 | — | `mini_game_wechat` |
| H5 | — | `html_5` |

**jq 客户端过滤示例**：

```bash
# 过滤 Android App
umeng-cli call '...getAppList...' '{"page":1,"perPage":100}' \
  | jq '.appInfos[] | select(.platform == "android")'

# 过滤所有微信系小程序
umeng-cli call '...umini.getAppList...' '{"pageIndex":1,"pageSize":100}' \
  | jq '.data.data[] | select(.platform | startswith("mini_wechat") or . == "mini_game_wechat")'

# 模糊匹配所有小程序（旧 `--platform mini`）
umeng-cli call '...umini.getAppList...' '{"pageIndex":1,"pageSize":100}' \
  | jq '.data.data[] | select(.platform | startswith("mini"))'
```

### 翻页全量遍历

本 Skill 接口**不提供"一次拉完所有"**的能力。客户端如需全量：

- App：先 `getAppCount` 拿总数 → 按 `perPage=100` 计算总页数 `ceil(count / 100)` → 循环 `page=1..N`
- 小程序：首次调用 `pageSize=100, pageIndex=1` 拿 `totalCount` → 计算 `ceil(totalCount / 100)` → 循环 `pageIndex=2..N`

### 输出格式

`umeng-cli call` 原生输出 JSON。旧 skill 的 `--output table` / `--output json` 开关不再存在，**Markdown 表格由 LLM 按需在摘要时整理**。

## 典型工作流

### 工作流 1：App 总数（1 次调用直出）

```
需求："我一共注册了多少个应用？"
1. getAppCount()   ← 无参
2. 读响应 count
3. 回复："你在友盟注册了 <count> 个 App。"
```

### 工作流 2：小程序总数（1 次调用，pageSize=1）

```
需求："我有多少小程序？"
1. umini.getAppList(pageIndex=1, pageSize=1)
2. 读 data.totalCount
3. 回复："你在友盟注册了 <totalCount> 个小程序。"
```

### 工作流 3：App + 小程序合并清单（对应旧 --list-all）

```
需求："把我所有的 App 和小程序都列出来"
1. uapp.getAppList(page=1, perPage=100)     ← 并行
   umini.getAppList(pageIndex=1, pageSize=100) ← 并行
2. 客户端合并两份 data，字段映射：
   - uapp.appInfos[].appkey ↔ umini.data.data[].dataSourceId → 统一字段 "key"
   - uapp.appInfos[].name ↔ umini.data.data[].appName → 统一字段 "name"
   - uapp.appInfos[].platform ↔ umini.data.data[].platform → 统一字段 "platform"
3. 若单页未拉完（totalPage>1 或 totalCount>100），按"翻页全量遍历"循环
4. 摘要：总 App 数 / 总小程序数 / 按平台分组计数
```

### 工作流 4：按平台过滤（对应旧 --platform）

```
需求："列出我所有的 Android App"
1. getAppCount() 拿 App 总数
2. 循环 uapp.getAppList(page=1..N, perPage=100) 拉全
3. jq/客户端过滤 appInfos[] 中 platform == "android" 的项
4. 摘要：Android App 数量、名称与 appkey 列表

需求："列出我的微信小程序"
1. umini.getAppList(pageIndex=1, pageSize=1) 拿 totalCount
2. 按 totalCount 循环拉全
3. 客户端过滤 platform == "mini_wechat"
4. 摘要：微信小程序数量与 dataSourceId 列表
```

## 边界条件与错误处理

- **账户下无任何 App**：`getAppCount` 返回 `count=0`；`getAppList` 返回 `appInfos=[]`，`totalPage=0`
- **账户下无任何小程序**：`umini.getAppList` 返回 `data.data=[]`，`data.totalCount=0`
- **`page` / `pageIndex` 越界**：返回空数组；应先由 `getAppCount` / `totalCount` 预判最大页数
- **`perPage > 100`**：`uapp.getAppList` 会被服务端截断到 100；客户端应主动限制在 100 以内
- **混淆分页参数**：`uapp.getAppList` 传 `pageIndex`/`pageSize` 会被忽略并退化为默认首页；`umini.getAppList` 传 `page`/`perPage` 同理。**参数名必须严格区分**
- **估算 App 总数**：**禁止**用 `totalPage × perPage` 估算（旧 assets.py 里的估算逻辑已由 `getAppCount` 替代）
- **按平台过滤**：接口不支持服务端过滤；客户端用 jq / LLM 后处理
- **未登录 / 登录态过期**：执行 `umeng-cli login --no-qr`（AI Agent 以后台模式运行并将链接展示给用户）
- **小程序与 App 合并**：`appkey` 与 `dataSourceId` 都是"AppKey"，但**分别在不同命名空间**注册，合并清单时无需去重

## 典型问法 → 接口/参数映射

| 典型问法 | 调用 | 参数 & 后处理 |
|----------|------|---------------|
| "我一共注册了多少个 App？" | `getAppCount` | 无参；读 `count` |
| "我有多少小程序？" | `umini.getAppList` | `pageIndex=1,pageSize=1`；读 `data.totalCount` |
| "我有多少应用（含 App + 小程序）？" | `getAppCount` + `umini.getAppList` | 两次调用求和 |
| "列出我所有的 App" | `uapp.getAppList` | `page=1,perPage=100`（可能需翻页） |
| "列出我所有的 Android App" | `uapp.getAppList` + 客户端过滤 | `platform == "android"` |
| "列出我所有的 iOS App" | `uapp.getAppList` + 客户端过滤 | `platform == "iphone"` |
| "我的小程序列表" | `umini.getAppList` | `pageIndex=1,pageSize=100` |
| "我的微信小程序" | `umini.getAppList` + 客户端过滤 | `platform == "mini_wechat"` |
| "我的字节跳动小程序" | `umini.getAppList` + 客户端过滤 | `platform == "mini_bytedance"` |
| "同时列出我的 App 和小程序" | `uapp.getAppList` + `umini.getAppList` | 客户端合并（字段别名） |
| "下一页" | 对应 `getAppList` | `page+1` 或 `pageIndex+1` |
| "某 App 的 DAU / 启动次数 / 留存" | 指向 `umeng-cli-uapp-core-index` / `-retention` 等 | 用本 Skill 拿到的 `appkey` 作为输入 |
| "小程序的累计用户 / 分享数据" | 指向未来 `umeng-cli-umini-*` Skill | 用本 Skill 拿到的 `dataSourceId` 作为输入 |

### 旧 skill 参数等价对照

旧 `uapp-assets` 的 CLI 参数与新接口的等价关系：

| 旧 CLI 参数 | 新接口调用 |
|-------------|------------|
| `--count` | `getAppCount`（等价直出 App 总数） |
| `--list-apps` | `uapp.getAppList`（默认首页） |
| `--list-apps --page N` | `uapp.getAppList`，`page=N` |
| `--list-apps --per-page M`（最大 100） | `uapp.getAppList`，`perPage=M` |
| `--list-apps --platform android` | `uapp.getAppList` + 客户端 jq `select(.platform == "android")` |
| `--list-apps --platform iphone` | 同上，`.platform == "iphone"` |
| `--list-apps --platform ios` | 同上，`.platform == "iphone"`（`ios` 是别名） |
| `--list-minis` | `umini.getAppList`（默认首页） |
| `--list-minis --page N` | `umini.getAppList`，`pageIndex=N`（**注意不是 `page`**） |
| `--list-minis --per-page M` | `umini.getAppList`，`pageSize=M`（**注意不是 `perPage`**） |
| `--list-minis --platform mini` | `umini.getAppList` + 客户端 jq `select(.platform \| startswith("mini"))` |
| `--list-minis --platform mini_bytedance` | 同上，`.platform == "mini_bytedance"` |
| `--list-all` | 并行 `uapp.getAppList` + `umini.getAppList`，客户端合并（见工作流 3） |
| `--output json` | `umeng-cli call` 原生输出即 JSON，无需额外开关 |
| `--output table` | 由 LLM 按需从 JSON 整理为 Markdown 表格 |
| `--config <path>` | 不再支持；登录态由 `umeng-cli login` 管理 |

## 注意事项

- 本 Skill **仅覆盖 3 个只读查询接口**：`getAppCount` + `uapp.getAppList` + `umini.getAppList`；不涉及任何写入或编辑
- 3 个接口均为 `GET` 方法；**均不需要 `appkey`**（账户级接口）
- **分页参数命名严格区分**：`uapp` 用 `page`/`perPage`，`umini` 用 `pageIndex`/`pageSize`；混用会被忽略
- **App 总数走 `getAppCount`**：`uapp.getAppList` 无 `totalCount`，禁止翻页估算
- **小程序总数走 `umini.getAppList.data.totalCount`**：`pageSize=1` 即可拿到
- **字段别名**：`appkey` ↔ `dataSourceId` / `name` ↔ `appName` / `createdAt` ↔ `gmtCreate`；合并清单时记得映射
- **平台过滤**：接口无服务端过滤参数，由客户端 jq / LLM 后处理；`uapp` 平台只有 `android`/`iphone`，小程序平台以 `mini_*` / `html_5` 开头
- **`perPage` 上限 100**：`uapp.getAppList` 服务端截断；`umini` 未见明确上限但建议同值
- **小程序指标查询不在本 Skill**：`umeng.umini.getOverview` / `getTotalUser` / `getRetentionByDataSourceId` 等归未来的 `umeng-cli-umini-*` Skill
- **App 指标查询不在本 Skill**：DAU / 新增 / 启动 / 留存 / 渠道 / 版本 / 事件 / APM 等均由对应 `umeng-cli-uapp-*` / `umeng-cli-uapm` 处理

## 快速参考

| # | 接口 | Endpoint（相对 baseUrl） | 必填参数 | 可选参数 | 用途 |
|---|------|--------------------------|----------|----------|------|
| 1 | `umeng.uapp.getAppCount` | `param2/1/com.umeng.uapp/umeng.uapp.getAppCount` | — | — | App 总数（直出 `count`） |
| 2 | `umeng.uapp.getAppList` | `param2/1/com.umeng.uapp/umeng.uapp.getAppList` | — | `page`（默认 1）/ `perPage`（默认 10，最大 100） | App 列表（响应 `appInfos[]` + `totalPage` + `page`，**无 totalCount**） |
| 3 | `umeng.umini.getAppList` | `param2/1/com.umeng.umini/umeng.umini.getAppList` | — | `pageIndex`（默认 1）/ `pageSize`（默认 30） | 小程序列表（响应 `data.data[]` + `data.totalCount` + `data.currentPage`） |

> 完整 uapp namespace 其他接口（如 `getYesterdayData` / `getRetentions` / `event.list` 等）请参考 [umeng-cli/reference/openapi/uapp.md](../../../umeng-cli/reference/openapi/uapp.md)；完整 umini namespace 接口请参考 [umeng-cli/reference/openapi/umini.md](../../../umeng-cli/reference/openapi/umini.md)。
> App 核心指标查询请使用 [umeng-cli-uapp-core-index](../umeng-cli-uapp-core-index/SKILL.md)；渠道/版本请使用 [umeng-cli-uapp-channel-version](../umeng-cli-uapp-channel-version/SKILL.md)；留存请使用 [umeng-cli-uapp-retention](../umeng-cli-uapp-retention/SKILL.md)；事件请使用 [umeng-cli-uapp-event](../umeng-cli-uapp-event/SKILL.md)；APM 请使用 [umeng-cli-uapm](../umeng-cli-uapm/SKILL.md)。
