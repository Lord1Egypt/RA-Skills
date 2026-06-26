# 微信小程序云开发指南（深度版）

## 概述

云开发（CloudBase）是微信官方提供的后端云服务，无需自建服务器：

| 服务 | 说明 |
|------|------|
| 云数据库 | NoSQL JSON 数据库（类似 MongoDB） |
| 云存储 | 文件存储（图片/音视频/文件） |
| 云函数 | 服务端 Node.js 代码（wx-server-sdk） |
| 云调用 | 微信开放能力（支付/订阅消息等） |
| 云托管 | 容器化后端服务（支持任意语言） |

---

## 开通与初始化

### 1. 开通云开发

微信开发者工具 → 顶部菜单栏 → **云开发** → 开通 → 创建环境

记住两个关键信息：
- **环境 ID**（如 `env-xxx`）
- **环境名称**（如 `production`）

### 2. 环境初始化

```javascript
// app.js
App({
  onLaunch() {
    if (!wx.cloud) {
      console.error('请使用 2.2.3 或以上的基础库以使用云能力')
    } else {
      wx.cloud.init({
        env: 'your-env-id',    // ⚠️ 填入实际环境 ID
        traceUser: true,       // 在控制台记录用户访问
      })
    }
  }
})
```

### 3. 云函数内初始化（wx-server-sdk）

```javascript
// cloudfunctions/xxx/index.js
const cloud = require('wx-server-sdk')
// cloud.DYNAMIC_CURRENT_ENV = 云函数当前所在环境（自动，无需手动填写）
cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

const db = cloud.database()
const _ = db.command    // 查询操作符
const $ = db.aggregate  // 聚合操作符
```

> ⚠️ `cloud.DYNAMIC_CURRENT_ENV` 是 **wx-server-sdk** 专属常量，**仅在云函数内有效**。小程序端用字符串环境 ID。

---

## 一、云数据库（深度）

### 1.1 数据类型

```javascript
db.serverDate()       // 服务器当前时间
db.Geo.Point(lng, lat) // 地理位置（经纬度）
db.Geo.MultiPoint([...]) // 多个点
db.RegExp({           // 正则匹配
  regexp: keyword,
  options: 'i',       // 不区分大小写
})
```

### 1.2 查询操作符（_.command）

```javascript
// 比较
_.eq(value)           // 等于（默认）
_.neq(value)          // 不等于
_.gt(value)           // 大于
_.gte(value)          // 大于等于
_.lt(value)           // 小于
_.lte(value)          // 小于等于
_.in([a, b, c])       // 包含于
_.nin([a, b])         // 不包含

// 组合
_.and([_.gt(18), _.lt(60)])  // AND
_.or([条件1, 条件2])          // OR
_.not(条件)                   // NOT

// 数组
_.all([a, b])      // 包含所有元素
_.size(n)          // 数组长度为 n
_.elemMatch(条件)  // 数组中至少一个元素满足条件

// 对象/字段
_.exists(true)     // 字段存在
_.type(2)          // 字段类型为数字（类型码：1=String, 2=Object...）
```

### 1.3 聚合管道（_.aggregate）

```javascript
// 云函数内的聚合查询
exports.main = async (event, context) => {
  const { page = 1, pageSize = 10 } = event
  const $ = db.command.aggregate

  // 1. 多表关联（lookup）
  const res = await db.collection('posts')
    .aggregate()
    .lookup({
      from: 'users',              // 关联的集合名
      localField: '_openid',       // 本集合字段
      foreignField: '_openid',     // 目标集合字段
      as: 'authorInfo',            // 输出字段名（数组）
    })
    .unwind('$authorInfo')         // 展开数组（每个元素一条记录）
    .addFields({
      authorName: '$authorInfo.name',
      authorAvatar: '$authorInfo.avatar',
    })
    .match({ status: 'published' }) // 过滤条件
    .sort({ createdAt: -1 })
    .skip((page - 1) * pageSize)
    .limit(pageSize)
    .project({                     // 字段投影
      title: 1,
      content: 1,
      createdAt: 1,
      authorName: 1,
      authorAvatar: 1,
    })
    .end()

  return { list: res.list }
}
```

> 💡 **聚合操作符速查**：
> `$add`, `$subtract`, `$multiply`, `$divide`（算术）
> `$eq`, `$ne`, `$gt`, `$gte`, `$lt`, `$lte`（比较）
> `$cond: [条件, true值, false值]`（条件）
> `$ifNull: [字段, 默认值]`（空值处理）
> `$group`（分组）, `$sort`（排序）, `$skip`（跳过）, `$limit`（限制）

### 1.4 事务（Transaction）

```javascript
// 云函数内事务：原子性操作
exports.main = async (event, context) => {
  const { orderId, userOpenid, amount } = event
  const transaction = await db.startTransaction()

  try {
    // 1. 扣除用户余额
    await transaction.collection('users')
      .where({ _openid: userOpenid })
      .update({
        data: {
          balance: _.inc(-amount),  // 原子增减（推荐，不存在并发问题）
        }
      })

    // 2. 创建订单记录
    await transaction.collection('orders').add({
      data: {
        _id: orderId,
        amount,
        status: 'paid',
        createdAt: db.serverDate(),
      }
    })

    // 3. 提交事务
    await transaction.commit()
    return { code: 0, message: '支付成功' }

  } catch (e) {
    // 任意一步失败 → 自动回滚
    await transaction.rollback()
    return { code: -1, message: '支付失败：' + e.message }
  }
}
```

> ⚠️ `_.inc(amount)` 是原子操作符，推荐用于余额/库存，避免并发超卖。

### 1.5 批量操作

```javascript
// 小程序端批量写入（单个事务，最多 100 条）
async function batchAddPosts(posts) {
  const db = wx.cloud.database()
  const tasks = posts.map(p =>
    db.collection('posts').add({ data: p })
  )
  const results = await Promise.all(tasks)
  return results
}

// 云函数端批量更新
async function batchUpdate() {
  const $ = db.command.aggregate
  const res = await db.collection('posts')
    .where({ status: 'draft' })
    .update({
      data: {
        status: 'published',
        publishedAt: db.serverDate(),
      }
    })
  return { updated: res.stats.updated }
}
```

### 1.6 数据库权限设计（安全规则）

在云开发控制台 → 数据库 → 选择集合 → 权限设置：

| 权限模式 | 读规则 | 写规则 | 适用场景 |
|---------|--------|--------|---------|
| 仅创建者可读写 | `doc._openid == auth.openid` | `doc._openid == auth.openid` | 用户私有数据（笔记、设置） |
| 所有用户可读 | `true` | `doc._openid == auth.openid` | 内容平台（文章、帖子） |
| 所有用户可读写 | `true` | `true` | 公开投票、公开留言板 |
| 后端管理员 | 读: `false` | 写: `false` | 所有操作走云函数，客户端无直接访问 |

```javascript
// ⚠️ 管理员操作必须在云函数内进行
exports.main = async (event, context) => {
  // 云函数内不受数据库权限限制
  const { adminKey } = event
  if (adminKey !== 'your-secret-admin-key') {
    return { code: -1, message: '无权限' }
  }
  await db.collection('posts').doc(event.postId).remove()
  return { code: 0 }
}
```

### 1.7 分页方案

```javascript
// 方案 A：offset 分页（适合小数据量，<10万）
async function getPostsPage(page, pageSize = 20) {
  const skip = (page - 1) * pageSize
  const [listRes, countRes] = await Promise.all([
    db.collection('posts')
      .orderBy('createdAt', 'desc')
      .skip(skip).limit(pageSize).get(),
    db.collection('posts').count(),
  ])
  return {
    list: listRes.data,
    total: countRes.total,
    hasMore: skip + listRes.data.length < countRes.total,
  }
}

// 方案 B：游标分页（适合大数据量，>10万）
// 首次请求只返回列表和第一条的 createdAt
// 下一页用 .startAfter(lastRecord.createdAt)
async function getPostsCursor(firstId, pageSize = 20) {
  let query = db.collection('posts')
    .orderBy('createdAt', 'desc')
    .limit(pageSize)

  if (firstId) {
    const first = await db.collection('posts').doc(firstId).get()
    query = query.startAfter(first.data.createdAt)
  }

  const res = await query.get()
  return res.data
}
```

---

## 二、云存储（深度）

### 2.1 文件上传进阶

```javascript
// 进度监控上传
function uploadWithProgress(filePath) {
  const cloudPath = `uploads/${Date.now()}.${filePath.split('.').pop()}`
  const uploadTask = wx.cloud.uploadFile({
    cloudPath,
    filePath,
    success: res => console.log('成功', res.fileID),
    fail: err => console.error('失败', err),
  })

  uploadTask.onProgressUpdate(res => {
    console.log(`上传进度: ${res.progress}%`)
    console.log(`已上传: ${res.totalBytesExpectedToSend} bytes`)
  })

  return uploadTask
}
```

### 2.2 批量上传/删除

```javascript
// 批量上传
async function batchUpload(filePaths) {
  const tasks = filePaths.map(path =>
    wx.cloud.uploadFile({
      cloudPath: `images/${Date.now()}_${Math.random()}.jpg`,
      filePath: path,
    })
  )
  const results = await Promise.all(tasks)
  return results.map(r => r.fileID)
}

// 批量删除
async function batchDelete(fileIDs) {
  return await wx.cloud.deleteFile({
    fileList: fileIDs,
    success: res => {
      res.fileList.forEach(item => {
        console.log(item.fileID, item.status)
      })
    }
  })
}
```

### 2.3 云存储安全

```javascript
// ⚠️ 绝对不要在前端直接暴露 fileID（用户可能越权访问）
// 推荐方案：云函数返回签名 URL

exports.main = async (event, context) => {
  const { fileID } = event
  // 云函数内验证权限后返回临时链接
  const res = await cloud.getTempFileURL({ fileList: [fileID] })
  return { url: res.fileList[0].tempFileURL }
}
```

---

## 三、云函数（深度）

### 3.1 云函数获取用户信息

```javascript
exports.main = async (event, context) => {
  const wxContext = cloud.getWXContext()

  // 永远可用的身份标识
  const OPENID   = wxContext.OPENID

  // 仅绑定了微信开放平台账号时可用
  const UNIONID  = wxContext.UNIONID

  // 小程序的 AppID
  const APPID    = wxContext.APPID

  // 来源环境（云调用时）
  const FROM_OPENID = wxContext.FROM_OPENID

  return { OPENID, UNIONID, APPID }
}
```

### 3.2 云函数互相调用

```javascript
// 云函数 A 调用云函数 B
exports.main = async (event, context) => {
  const res = await cloud.callContainer({
    config: { env: cloud.DYNAMIC_CURRENT_ENV },
    path: '/B',              // 云函数 B 的路径
    method: 'POST',
    data: { from: 'A', ...event },
    header: { 'Content-Type': 'application/json' },
  })
  return res.data
}
```

### 3.3 云函数定时触发器

```json
// cloudfunctions/schedule/index.js 同级目录
{
  "name": "schedule",
  "trigger": {
    "name": "myTrigger",
    "type": "timer",
    "config": "0 0 2 * * *"  // cron: 每天凌晨 2 点
  }
}
```

### 3.4 云函数 HTTP 访问（云托管）

```javascript
// 云函数可被 HTTP 请求调用（需开启云托管）
exports.main = async (event, context) => {
  // event.httpContext 包含 HTTP 请求信息
  const { method, path, queries, headers, body } = event.httpContext
  return {
    statusCode: 200,
    header: { 'Content-Type': 'application/json' },
    body: JSON.stringify({ message: 'Hello via HTTP' }),
  }
}
```

---

## 四、环境隔离与多环境

### 4.1 多环境切换

```javascript
// 小程序端切换环境
const ENV = 'production'  // 或 'test-xxx'
wx.cloud.init({ env: ENV })

// ⚠️ 环境隔离原则：
// - 小程序测试版 → 测试环境
// - 小程序正式版 → 生产环境
// - 不要混用，否则数据泄露风险
```

### 4.2 云函数跨环境查询

```javascript
// 云函数内指定其他环境（谨慎使用）
const adminDb = cloud.database({ env: 'production' })
```

---

## 五、Common Mistakes（深度云开发篇）

| 错误 | 正确做法 |
|------|---------|
| 在小程序端直接查 `users` 集合做管理员操作 | 所有管理员操作放云函数 |
| 用 `.then()` 嵌套云函数调用 | 用 `Promise.all` 并行调用 |
| 数据库权限设为 `true`/`true`（全开） | 按最小权限原则配置 |
| 用 `Date.now()` 记录时间 | 用 `db.serverDate()` 获取服务端时间 |
| 在小程序端直接暴露敏感操作 | 用云函数封装，客户端只调用 `callFunction` |
| 事务内操作过多（>100条） | 拆分为多个事务 |
| 聚合 `$lookup` 不加 `$unwind` | 关联结果默认是数组，需要 `$unwind` 展开 |
| `_.eq(null)` 查询空字段 | 用 `_.exists(true) && _.eq(null)` 或 `doc.field == undefined` |

---

## 六、性能优化

```javascript
// 1. 字段投影（只取需要的字段）
db.collection('posts').field({ title: true, createdAt: true })

// 2. 限制返回条数（必做，防止数据量过大）
.limit(100)

// 3. 建立索引（控制台 → 数据库 → 索引管理）
// 常用索引场景：orderBy 字段、where 查询字段

// 4. 避免全表扫描
// ❌ 错误：db.collection('posts').where({ title: /.keyword./ }).get()
// ✅ 正确：用正则前加固定前缀，或用云函数 + 搜索引擎

// 5. 列表缓存策略
const CACHE_KEY = 'posts_cache'
const CACHE_TTL = 5 * 60 * 1000  // 5 分钟

function getCachedPosts() {
  const cached = wx.getStorageSync(CACHE_KEY)
  if (cached && Date.now() - cached.ts < CACHE_TTL) {
    return cached.data
  }
  return null
}
```

---

## 七、官方文档链接

- 云数据库指南：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/database/guide/
- 聚合操作：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/database/aggregate/
- 云存储：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/storage/
- 云函数：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/functions/
- 云调用（微信支付）：https://pay.weixin.qq.com/doc/v3/merchant/4012062524
