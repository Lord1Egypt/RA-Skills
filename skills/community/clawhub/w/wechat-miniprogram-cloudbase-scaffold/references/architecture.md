# 架构与数据模型（云开发小程序）

从「不刷短剧·打卡帮」沉淀的架构方法论。核心思路：**确定性下沉到工具层**，
用简单、可验证的模式规避云开发（无 schema、无事务、集合弱类型）的天然短板。

## 一、为什么用「单函数 REST 路由」

云开发有两种后端组织方式：

| 方式 | 说明 | 取舍 |
|---|---|---|
| 每接口一个云函数 | 每个功能一个函数 | 冷启动多、函数多难管理、鉴权重复写 |
| **单函数 REST 路由（推荐）** | 一个 `api` 函数承载所有接口，内部按 `path` 分发 | 只维护一个函数、鉴权统一、冷启动少 |

`api` 云函数就是一个「迷你 Express」：前端把请求封装成
`{ path, method, body, query }` 传给 `wx.cloud.callFunction({ name: 'api' })`，
函数内部按 path+method 路由到 handler。平台自动注入 `OPENID`，无需登录态/token。

## 二、标准目录与职责

```
cloudfunctions/api/
├── index.js        # 唯一入口：解 OPENID → 构造 ctx → 路由分发 → 统一 try/catch
├── db.js           # wx-server-sdk 初始化（DYNAMIC_CURRENT_ENV），导出 { cloud, db, _ }
├── services/       # 业务逻辑，纯函数优先，可单独测试
│   ├── streak.js   # 纯函数：连续天数计算（不碰数据库）
│   └── stats.js    # 数据访问：读 checkins 调 streak，返回统计
└── package.json    # 仅依赖 wx-server-sdk
```

关键点：
- `db.js` 用 `cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })`——让函数自动用所在环境，
  避免写死环境 ID（换环境/换 AppID 不用改代码）。
- `services/` 里**纯函数与数据访问分离**：`streak.js` 是纯函数（可单测），
  `stats.js` 负责取数。业务越复杂越要这样拆。

## 三、数据模型设计原则

云数据库是弱类型 NoSQL（类 Mongo），没有 schema 强约束，所以**约束靠代码 + 唯一索引兜底**。

1. **字段命名统一**：数据库用 camelCase（`createdAt`、`gangId`），对外 API 视图再转
   snake_case / 你需要的格式。在 `index.js` 里写 `xxxView()` 转换函数，避免脏字段外泄。
2. **时间统一 ISO 字符串**：`new Date().toISOString()`，不要存 Date 对象（前端好处理）。
3. **日期用「东八区字符串」**：`todayStr()` 用 `Date.now() + 8*3600*1000` 再取 UTC 前 10 位，
   避免 UTC 边界把晚上打卡算到第二天。
4. **唯一性靠索引兜底**：幂等写入（如每天只能打卡一次）除了代码先查再写，还必须在
   控制台建唯一索引（如 `checkins{openid:1,date:1}`），防止并发穿透。**索引是手动建的**
   （见 deploy skill）。
5. **避免缓存集合**：能实时算的（连续天数、总数）就实时算，不要维护 `user_stats` 这类
   缓存集合——它既不省事（要写同步逻辑）又是「集合不存在」和「不一致」的双重隐患源。

## 四、关键设计模式（代码级）

### 1. 幂等建号（消除时序竞争）

`login` 云函数和 `me` 接口都可能「第一个」拿到新用户，存在时序竞争。解法：**两者都幂等建号**。

`api/index.js` 的 `me()`：
```js
let u = (await db.collection('users').where({ openid: ctx.OPENID }).get()).data[0];
if (!u) {
  try {
    const add = await db.collection('users').add({ data: { openid: ctx.OPENID, ...默认值 } });
    // 新用户自动加入所有公开数据
    for (const g of (await db.collection('gangs').where({ type: 'public' }).get()).data) {
      await db.collection('gang_memberships').add({ data: { openid: ctx.OPENID, gangId: g._id, role: 'member' } });
    }
    u = (await db.collection('users').doc(add._id).get()).data;
  } catch (e) {
    // 并发下 login 可能已建号，重查一次兜底
    u = (await db.collection('users').where({ openid: ctx.OPENID }).get()).data[0];
  }
}
```

### 2. 幂等建集合（seed）

CLI 不能建集合，且 `tcb fn invoke` 有 Namespace 元数据 bug（见 deploy skill）。
所以用 `seed` 云函数在建号前跑一次，对每个集合「加占位再删」实现幂等建集合：

```js
async function ensureCollection(name) {
  try {
    const r = await db.collection(name).add({ data: { _init: true } });
    await db.collection(name).doc(r._id).remove();
  } catch (e) { /* 已存在则忽略 */ }
}
// 种子数据只在空时插入，保证幂等
const cnt = (await db.collection('gangs').count()).total;
if (cnt === 0) { /* 插入默认数据 */ }
```

### 3. 实时计算代替缓存集合

`services/stats.js` 直接读 `checkins` 事实表算 streak，不做 `user_stats` 缓存：

```js
async function fetchStreaks(openid) {
  const res = await db.collection('checkins').where({ openid }).orderBy('date', 'asc').get();
  return computeStreaks(res.data.map(c => ({ date: c.date, watched: c.watched })));
}
```

`computeStreaks` 是纯函数（`streak.js`），返回 `{ current, longest, total }`。
「current」向后截断到今天/昨天（昨天截断 = 今天还没打但没断）。

### 4. 订阅消息 + 定时触发器

`dailyPush` 函数做两件事：
- 从 `reminders` 集合读 `enabled:1` 的用户；
- 从 `subscribe_grants` 读剩余订阅额度，>0 才 `cloud.openapi.subscribeMessage.send`。

定时触发器**必须写在函数自己的 `config.json`**（不是只写在 cloudbaserc.json）：
```json
{
  "permissions": { "openapi": ["subscribeMessage.send"] },
  "triggers": [{ "name": "dailyPushTimer", "type": "timer", "config": "0 0 20 * * * *" }]
}
```
cron `0 0 20 * * * *` = 每天 20:00（秒 分 时 日 月 周 年，7 段）。

### 5. 前端统一请求封装（request.js）

```js
function callApi(path, method, data) {
  // 兼容 /api/checkins?month=2026-08 这种 query 写法
  // ...解析 query...
  return new Promise((resolve, reject) => {
    wx.cloud.callFunction({
      name: 'api',
      data: { path: pathname, method, body: data || {}, query },
      success: res => {
        if (res.result && res.result.error) {
          wx.showToast({ title: res.result.error, icon: 'none' });
          return reject(new Error(res.result.error));
        }
        resolve(res.result);
      },
      fail: err => {
        console.error('[callApi fail]', pathname, method, err);  // 关键：打印完整错误
        reject(err);
      },
    });
  });
}
```

要点：
- **`fail` 回调里 `console.error` 完整 err 对象**——这是排障的关键，别只打印 errMsg。
- `login` 单独走 `wx.cloud.callFunction({ name: 'login' })`，不走 api 路由（它不含业务 path）。
- 登录态用 `App.onLaunch` 里 `api.login()` 拿 user 存 `globalData`，页面用回调或轮询拿。

## 五、从「自托管后端」迁移的思路

如果你已有 Express/SQLite 后端（本项目就是这么迁移来的），映射关系：

| 自托管 | 云开发 |
|---|---|
| Express 路由 | `api` 云函数 `index.js` 的路由分发 |
| SQLite 表 | 云数据库集合（弱类型，约束靠代码+索引）|
| SQL 查询 | `db.collection().where().get()`（注意单次最多 100 条，用 limit 分页）|
| 登录态 session | `cloud.getWXContext().OPENID`（平台注入，免维护）|
| 定时任务 cron | 云函数 `config.json` 的 `triggers` |
| 短信/推送 | 订阅消息 `subscribeMessage.send` |

迁移时注意：云数据库**没有 join**，多表关联要靠「应用层 join」（先查 A 再逐条查 B），
数据量大会有 N+1 问题——工具型小程序（用户量级不大）可接受，量大了要重构。
