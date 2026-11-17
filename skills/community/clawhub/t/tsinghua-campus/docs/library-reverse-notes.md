# 图书馆逆向交接文档

> 记录清华大学图书馆各子系统的逆向成果与攻破笔记，供后续同学继续。
> 时间：2026-08-16

## 一、现状速览

| 子系统 | 功能 | 状态 |
|--------|------|------|
| seat.lib | 座位余量（公开）| ✅ library.py seat 已实现 |
| seat.lib | 座位分布（馆→楼层→区域，公开 API）| ✅ library.py areas 已实现 |
| seat.lib | 我的座位预约记录 | ✅ library.py my-bookings 已实现 |
| seat.lib | 选座 + 预约 | ✅ library.py book 已实现 |
| seat.lib | 取消预约 | ✅ library.py cancel 已实现 |
| cab.lib | 研读间占用状态 | ✅ library.py rooms 已实现 |
| discover.lib | 我的图书馆（借阅）| ⛔ 登录在 CDP 环境受限（见下）|
| discover.lib | 水木搜索（馆藏检索）| 🔍 公开 API 已发现（Primo），检索 endpoint 待逆向 |

## 二、已实现功能（skill/campus/library/）

### 1. 座位余量（公开，无需登录）
- URL: `seat.lib.tsinghua.edu.cn/home/web/f_second`
- 解析 `div.rooms` 块：馆名/今日剩余/总量/馆区id（area id）
- 实测：北馆 424/877、西馆 593/876、文科 459/536、法律 524/643 等 6 馆

### 2. 座位登录（iframe CAS）
- 点"登录"→ iframe 内嵌 CAS（frame URL = id.tsinghua.edu.cn）
- 登录：遍历 `page.frames` 找 id.tsinghua → `fr.fill("#i_user")` + `fr.fill("#i_pass")` + `fr.evaluate("doLogin()")`
- 信任浏览器免 2FA，登录稳定

### 3. 我的座位预约（登录后）
- URL: `seat.lib.tsinghua.edu.cn/user/index/book`
- 表格：预约号/预约空间/开始时间/结束时间/当前状态（已使用/审核中/待审核等）
- 详情: `/user/index/look/id/<预约号>`

### 4. 座位分布（公开 API，无需登录）
- URL: `seat.lib.tsinghua.edu.cn/api.php/v3areas/<馆区id>`
- 返回馆→楼层→区域树，每层 `TotalCount`/`UnavailableSpace`
- 馆区 id: 35北馆/64西馆/89文科/6法律/19美术/29金融
- 实测：北馆二层 280 总/191 余、西馆二层 492/439、文科二层 138/84 等

### 5. 座位预约 API（已攻破，book/cancel 已实现）
- 关键全局配置 `ska`：`areaApi=/api.php/v3areas`, `timeApi=/api.php/space_time_buckets`, `spacesApi=/api.php/spaces`, `dayApi=/api.php/space_days`, `loginApi/logoutApi/checkUrl`, `access_token`（登录后动态）
- 时间段：`/api.php/space_time_buckets?area=<区域>&day=<日期>` → `spaceName`(NF2A001)/`bookTimeId`/`beginTime`/`endTime`/`status`
- **时间段查证结论（2026-08-16）**：后台**不提供选时间段接口**。`space_time_buckets` 对每个日期只返回 **1 个时段**：
  - 当天 → 当前时刻到闭馆（如 16:13-17:00）
  - 次日 → 开馆到闭馆（09:00-17:00）
  - `space_time_buckets_one/two/third` 等无额外能力；`space_days` 需路径式调用（`/api.php/space_days/<area>`）
  - → 学生无法自选时间段，library.py book 取 `segments[0]` 与后台能力匹配，无需 --segment 参数
- 座位列表：`/api.php/spaces_old?area=<区域>&segment=<时间段>&day=<日期>&startTime=<>&endTime=<>`（**注意是 spaces_old**）
- **座位是 DOM `li.seat`**（非纯 Canvas！），`data-no=<座位id>` + `data-data=<JSON>`，absolute 定位（left=point_x*1366/100*size, top=point_y*768/100*size），status=1 可选
- **预约**：`POST /api.php/spaces/<spaceId>/book` + `{access_token, userid, segment, type:1, operateChannel:2}` → 返回预约号
- **取消**：`POST /api.php/profile/books/<预约id>` + `{_method:delete, id, userid, access_token, operateChannel:2}`
- 区域点击跳转：`/web/seat2/area/<区域id>/day/<日期>`；选时间段跳转：`/web/seat3?area=&segment=&day=&startTime=&endTime=`
- **当日取消次数有限制**（官方规则第 6 条：**取消预约功能限每日 1 次**；实测超限返回"当日取消次数已达上限"）
- 座位状态：1可选/2已预约/6使用中/7暂离/3-5关闭
- **预约规则（ska.bookRule，官方原文）**：
  1. 可约当日/次日，开放 6:00-23:00
  2. 开馆时段预约当日 → 成功 30 分钟内签到（门禁自动）
  3. 未开馆预约（含次日）→ 生效日开馆后 30 分钟内签到
  4. 未签到 → 释放座位 + 记违规 1 次
  5. 临时离开保留 60 分钟（美术/法律馆就餐时段 90 分钟）
  6. **取消预约每日限 1 次**
  7. 违规满 5 次暂停 3 天；每学期初（3/1、9/1）清零

### 6. 研读间占用（cab.lib，登录后）
- URL: `cab.lib.tsinghua.edu.cn`（Vue SPA，iframe CAS 登录）
- 首页空间列表：北馆单人研读间（三层）等 9 类
- **真实点击**空间（`page.click("text=空间名")` 触发 Vue 路由）→ `#/ic/researchSpace/1/<id>/<id>`
- 占用视图：房间（北馆3F-01 等）+ 占用者姓名（程*、郭*苓 等，脱敏格式）
- 解析：body 文本从"预约状态"后提取房间行 + 占用者
- **占用视图渲染需长等待**（Vue 异步，~40s）
- ⚠️ **cab 登录修复**：cab 是 Vue SPA，body 挂载前为空，`_iframe_cas_login` 会误判登录成功。必须等 Vue ready（body 出现"个人中心"）再判断。

### 6b. 研读间预约逆向（深水区，未完成）
- **预约 API**：`POST /ic-web/reserve/bulkAdd`（base = window.g.ApiUrl = /ic-web）
- **交互**：时间条 `div.line` 绑定 mousedown/mousemove/mouseup（**拖拽选时间**），timeItem 是只读刻度
- **流程**：拖拽选时间段 → `up()` 存 vuex（newResearch.roomConfig + setCreatedStatus）→ 确认按钮 → bulkAdd
- **参数**（部分）：newResearch={resvDates, kindIds} + roomConfig={startTime, endTime} + sysKind；完整结构需实测
- **受阻**：
  - 拖拽模拟（Playwright mouse down/move/up）未触发 Vue 选择（事件/坐标/时段问题）
  - bulkAdd 参数需实测请求（无法纯静态确定）
  - cab 登录虽修复，但点击/拖拽时序敏感
- **时间格坐标**（北馆3F-01 line）：(551, 710, 701x58)，timeItem 09:00=551 起每格 88px
- **vuex 配置**：resvTimeUnit=10（10分钟单位）、syskind=33、空间 kindId（北馆单人研读间=2071759）
- 占用查询（rooms）已实现；预约建议后续在校内网/浏览器环境深挖
- 首页空间列表：北馆单人研读间（三层）等 9 类
- **真实点击**空间（`page.click("text=空间名")` 触发 Vue 路由）→ `#/ic/researchSpace/1/<id>/<id>`
- 占用视图：房间（北馆3F-01 等）+ 占用者姓名（程*、郭*苓 等，脱敏格式）
- 解析：body 文本从"预约状态"后提取房间行 + 占用者

## 三、discover.lib（我的图书馆/水木搜索）攻破笔记

### 登录链
```
discover 点"统一认证" → www.metaauth.com/211030/login.html（302）
→ http://uas.yuntaigo.com/casservice/tsinghua/login?serviceIP=www.metaauth.com/（302）
→ https://id.tsinghua.edu.cn/do/off/ui/auth/login/form/<token>/1?/casservice/tsinghua/validate（清华 CAS）
```

### 两个硬障碍（CDP 即用即退环境）
1. **yuntaigo/metaauth 被 CDP Chrome 拦截**：`ERR_BLOCKED_BY_CLIENT`
   - 根因：CDP 模式（`--remote-debugging-port` 独立启动）下 Chrome 对这两个域名客户端拦截
   - 尝试了：`--disable-blink-features=AutomationControlled`、`--disable-safe-browsing`、`--disable-features=HttpsUpgrades`（拦截解除变 TOO_MANY_REDIRECTS）、`page.route`（拦不到导航层）、`--allow-insecure-localhost`——均无法在 CDP 下稳定访问
   - **Playwright 原生 launch（非 CDP）能访问**（200），但浏览器随脚本退出，无法跨进程两阶段
   - **解法（已验证）**：urllib 预取 yuntaigo 302 → 拿 CAS URL（https，CDP 不拦）→ CDP goto CAS
2. **CAS casservice 入口 login/check chrome-error**：doLogin 后跳 `login/check`，但 CDP 下加载失败（chrome-error）
   - 未解决。learn/info 的标准 CAS（非 casservice）在 CDP 下正常

### 结论
- discover 登录在 **base-cas CDP 架构下不可行**（两个障碍）
- 需校内网环境或非 CDP 浏览器（Playwright 原生 launch 单次运行）才能完成
- 用户浏览器（校内网）可用

### 其他发现
- discover 是 **Vue SPA**（tsuproject）+ **Ex Libris Primo** 水木搜索
- 公开 API：`/tsinghuasearch/primo/scopes`、`/configuration`、`/detect/index`（无需登录）
- 检索 API endpoint 未逆出（需从前端 chunk JS 找）
- discover 有"其它账号登录"（本地账号）但实测只有统一认证可用

## 四、cab 研读间/研讨间内部 API（逆向，2026-09-11）

> cab.lib.tsinghua.edu.cn 是 **Vue SPA**（"Information Commons"，图书馆空间预约系统）。
> 之前 `library.py rooms` 靠**文本抓取**（点空间→解析页面文字），脆弱。已改为**内部 API**。

### 架构
- SPA 入口 `https://cab.lib.tsinghua.edu.cn/`（`config/config.js` → `window.g.ApiUrl = '/ic-web'`）
- 所有 API：`https://cab.lib.tsinghua.edu.cn/ic-web/<path>`，`withCredentials`（cookie 会话）
- 请求头需 `X-Requested-With: XMLHttpRequest`、`Content-Type: application/json; charset=UTF-8`
- 登录：**CAS 单点登录**（`window.g.loginMode = 2`）；未登录时 API 返回 `{"code":300,"message":"用户未登录，请重新登录"}`
- `hiddenReferer: true`（部分请求不带 referer）

### 登录流程
| 端点 | 方法 | 说明 |
|------|------|------|
| `auth/address` | GET | 返回 CAS 跳转地址（带 service）|
| `auth/userInfo` | GET | 当前用户信息（300=未登录）|
| `login/publicKey` | GET | RSA 公钥（密码加密用）|
| `login/user` | POST | 账号密码登录（loginMode=1 时用）|
| `login/signOut` | POST | 登出 |
| `sysConfig/public` | GET | 公开系统配置（**无需登录**）|

> cab 实际用 iframe CAS（Vue 注入 `id.tsinghua` frame）；`_cab_login` 已在 library.py 实现（遍历 frames 填表）。

### 查询端点
| 端点 | 方法 | 登录 | 说明 |
|------|------|:---:|------|
| `roomMenu` | GET | ❌公开 | **空间种类列表** → `[{kindId, kindName}]` |
| `reserve` | GET | ✅ | **房间占用 + 预约人**（SPA 时间线用；**含脱敏姓名**）|
| `roomDevice/roomInfos` | GET | ✅ | 房间占用（**仅时间段+状态，无姓名**）|
| `home/page/room/idle` | GET | ✅ | 空闲房间统计 |
| `seatDevice/resvStatus` | GET | 部分 | `{available, used}` 统计 |
| `seatRoom/open` / `seatRoom/openScope` | GET | ✅ | 房间开放时段 |
| `reserve/areaInfo` / `reserve/seatArea` / `/room/openTimes` | GET | ✅ | 区域/座位/开放时间 |

**⭐ `reserve` GET（含预约人，SPA 时间线用）**：
```
GET /ic-web/reserve?sysKind=1&resvDates=YYYYMMDD&page=1&pageSize=30&kindIds=<kindId>&labId=
```
响应 `data=[{devId, devName, kindName, labName, openStart, openEnd,
  resvRule:{minResvTime,maxResvTime,...}, resvInfo:[{
    title, trueName(脱敏 张*嘉), logonName(脱敏 2***3),
    startTime(epoch ms), endTime, resvStatus, resvId, uuid}]}]`
- **`trueName` = 预约人姓名（系统已脱敏：姓*名）**
- **`logonName` = 学号（系统已脱敏：2********3）**
- `startTime`/`endTime` 是 epoch 毫秒，需转换
- `minUser`/`maxUser`（如 3~10 人）、`resvRule.minResvTime/maxResvTime`（30/240 分钟）
- ⚠️ **隐私**：姓名/学号虽已脱敏，仍是个人信息，面向用户输出须遵守 SKILL 隐私铁律

> 对比：`roomDevice/roomInfos` 的 `resvInfos` **只有** `resvBeginTime/resvEndTime/resvStatus`（无姓名）；要姓名必须用 `reserve`。

**`roomMenu` 实测返回的 9 个空间（kindId）**：
```
北馆单人研读间（三层）        2071759
北馆团体研讨间（二层）        2071757   ← "F2 04" 即此空间 2 层 04 号房间
西馆高山音乐研讨间（中208）   11825707
西馆流水音乐研讨间（中210）   11832983
文科馆单人研读间（三层）      10312
文科馆团体研讨间（二层）      10314
法律馆单人研读间（四层）      10048995
法律馆研讨舱（四层、五层)     12149594
法律馆双人舱（五层)           12149595
```

**`roomDevice/roomInfos` 响应结构（✅ 实测已验证）**：
```json
{"code":0,"message":"查询成功","data":[
  {"kindName":"北馆团体研讨间（二层）","roomInfos":[
    {"devId":2071787,"devName":"北馆2F-04","minResvTime":30,
     "openTimes":[{"openStartTime":"08:00","openEndTime":"22:00","openLimit":1}],
     "resvInfos":[{"resvBeginTime":"2026-09-11 08:00:00","resvEndTime":"2026-09-11 12:00:00","resvStatus":1109}]}
  ]}
]}
```
- `data` = 9 个空间（kindName），每个含 `roomInfos`（房间列表）
- 房间：`devId`（预约用）/ `devName`（如"北馆2F-04"）/ `minResvTime` / `openTimes` / `resvInfos`
- `resvInfos`：`resvBeginTime`/`resvEndTime`/`resvStatus`（**不含姓名**，非管理员看不到）
- `resvStatus` 位掩码：`2`待生效 `4`已生效/使用中 `16`已违约 `128`已结束 `256`待审核 `512`审核未通过 `1024`审核通过 `2048`已暂离
  - 实测值 `1093`=1024+64+4+1（审核通过+已生效）；`1027`=1024+2+1（审核通过+待生效）；`1109`=1024+64+16+4+1（审核通过+已生效+已违约）

**`home/page/room/idle` 响应（✅ 实测）**：每个空间的空闲/总数
```json
{"code":0,"data":[{"name":"北馆团体研讨间（二层）","idelQuantity":0,"totalQuantity":4}, ...]}
```
（注意拼写是 `idelQuantity`）

**北馆团体研讨间（二层）房间**（kindId=2071757）：
| 房间 | devId |
|------|-------|
| 北馆2F-01 | 2071799 |
| 北馆2F-02 | 2071795 |
| 北馆2F-03 | 2071791 |
| **北馆2F-04** | **2071787** |

### 预约端点（写操作，需登录 + 授权）
| 端点 | 方法 | 说明 |
|------|------|------|
| **`reserve`** | **POST** | **单次预约（研讨间实际用这个！body=JSON payload）** |
| **`reserve/delete`** | **POST** | **取消预约（body `{"uuid":"<预约uuid>"}`）✅ 实测"删除成功"** |
| `reserve/endAhaed` | POST | 提前结束（body `{"uuid":...}`）|
| `reserve/endReserve` | POST | 签离（body `{"resvId":...}`）|
| `reserve/update` | POST | 改约 |
| `reserve/endList` | GET | 我的结束列表 |
| `reserve/time/expand` | POST | 续时 |
| `reserve/time/expand/duration` | GET | 续时时长 |
| `reserve/count` | GET | 我的预约计数 |
| `resvMember/operate` | POST | 成员操作 |
| `reserve/operate/rec` | GET | 操作记录（权限不足）|
| `account/getMembers` | GET | **成员搜索 `?key=<姓名>&page=1&pageNum=10` → `[{accNo, logonName, deptName}]`** |

> **取消端点辨析**：`handleDelete`（取消按钮）→ `POST reserve/delete`（`{uuid}`）；`endReserve`（签离）用 `{resvId}`；`endAhaed`（提前结束）用 `{uuid}`。**取消用 `reserve/delete`**。

### ⚠️ 预约规则（实测）
1. **一人一天最多 4 小时**（同一用户当天累计 ≤240min）
2. **不能连续预约**：同一用户已有某时段，不能订**紧接的连续时段**（换房间也不行）→ `{"code":1,"message":"不能连续预约"}`
3. 时段冲突 → `{"code":1,"message":"设备在该时间段内已被预约"}`
4. 需按时签到，违约影响权限
5. `resvRule`：`minResvTime:30` / `maxResvTime:240`（30min~4h）

**预约 payload（从 SPA `handleSubmit` 提取）**：
```json
{
  "resvBeginTime": "YYYY-MM-DD HH:mm:00",
  "resvEndTime":   "YYYY-MM-DD HH:mm:00",
  "sysKind": 1,
  "appAccNo": "<学号>",
  "memberKind": 1,
  "testName": "<主题>",
  "resvKind": 2,
  "resvProperty": 32,
  "appUrl": "",
  "resvMember": ["<学号>"],
  "resvDev": ["<房间 devId>"],
  "memo": "",
  "captcha": "",
  "addServices": []
}
```
- `resvDev` = 房间的设备 id（从 `roomDevice/roomInfos` 的 `devId` 拿）
- 当日预约时 `resvBeginTime` 会被前端改成"当前时间+1 分钟"

### 实现
- `library.py` 新增 `_cab_api`（页面上下文 fetch，带 cookie）+ `_cab_roommenu` + `_cab_room_status`
- `cmd_rooms` 改为：登录 → `roomMenu` 找 kindId → `roomDevice/roomInfos` 取房间状态 → 返回结构化 JSON
- 预约写操作**未实现**（高风险，需用户明确授权 + 图形验证码 `captcha`）

### 踩坑
- **cdp_profile 损坏**（2026-09-11）：`skill/campus/runtime/profiles/cdp_profile` 膨胀到 663MB 后，chrome 启动即崩（打印 "DevTools listening" 后退出，CDP 端口不可用）。
  - **修复**：备份重命名为 `cdp_profile_broken_20260911` → chrome 重建新 profile（~10MB）→ 重新 CAS 登录（一次 2FA）→ 恢复正常。
  - 教训：profile 异常膨胀时应及时清理/重建。
- **登录验证流程**：新 profile 未信任 → base-cas `login.py --system learn --ensure` 触发 2FA → 用户给码 → `--submit-code` → 信任建立（profile 级）→ cab iframe CAS 自动登录。

## 五、后续同学接手建议

1. **discover 借阅记录**：校内网环境用 Playwright 原生 launch 单次登录 → 抓 `/user/index/book`（借阅）或续借 API
2. **水木搜索检索**：抓 chunk JS 找 `/tsinghuasearch/...` 检索 endpoint（Primo search）
3. **座位预约/研读间预约（写操作）**：选座流程（地图/时间格交互）+ 高风险，需用户明确授权
4. **选座机制**：seat 选座是 `/home/web/f_second` 点馆区 → 座位地图；cab 研读间是时间格拖拽选择
5. **cab 研讨间**：API 已逆出（见第四节）；待办 = 修复 cdp_profile + 登录后核实 `roomDevice/roomInfos` 响应结构 + 实现预约写操作（需 captcha）

## 六、相关文件

- `skill/campus/library/scripts/library.py` — 主脚本（seat 余量 + my-bookings + rooms）
- `skill/campus/library/scripts/discover_login.py` — discover 两阶段登录（当前受限）
- `skill/campus/library/SKILL.md` — 子 SKILL 文档
- 逆向临时脚本在 `D:\Temp\campus-env\`（probe_seat*/probe_cab*/probe_discover*/test_cdp*）
