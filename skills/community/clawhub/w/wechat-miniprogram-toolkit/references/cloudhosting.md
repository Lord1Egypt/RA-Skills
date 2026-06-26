# 微信云托管全指南

## 激活契约

**符合以下任一场景时加载：**
- 云托管、CloudBase 托管、容器化部署、Container
- Docker 部署小程序后端、HTTP 触发器
- Node.js/Python/Go 等语言写后端（非云函数）
- 服务端 SDK、REST API、后端服务
- 已有服务器迁移云托管、微服务架构
- 需要持久运行的后台任务、定时任务

---

## 一、云托管 vs 云函数 对比

| 维度 | 云函数 | 云托管 |
|------|--------|--------|
| 语言 | Node.js（受限）| 任意语言（容器）|
| 持久性 | 事件驱动，用完即释放 | 常驻容器，支持长连接 |
| 冷启动 | 有冷启动延迟 | 预付费实例常驻，无冷启动 |
| 适用场景 | API 调用、即时计算 | Web 服务、长连接、定时任务 |
| 扩缩容 | 自动 | 可手动扩缩容 + 自动扩缩 |
| 价格 | 按调用次数 | 按实例规格 × 时长 |
| 端口 | 无端口概念 | 监听固定端口（如 80/443/8080）|
| 环境变量 | 云函数环境变量 | 环境变量 + 私密配置 |
| 日志 | 云函数日志 | 容器日志 + 云日志 |

---

## 二、开通与配置

### 2.1 开通步骤

1. 微信开发者工具 → 云开发控制台 → 云托管 → 开通
2. 创建服务（Service）→ 创建版本（Version）
3. 上传代码包或连接代码仓库（Git）
4. 配置环境变量和启动命令
5. 获取 HTTP 访问地址

### 2.2 项目结构

```
miniprogram/
├── cloudfunctions/     ← 云函数（传统模式）
└── server/             ← 云托管后端代码（新增）
    ├── Dockerfile
    ├── package.json
    ├── src/
    │   ├── index.js     ← 入口文件（监听端口）
    │   └── routes/
    ├── .env.example
    └── .env.secrets     ← 不提交到 Git
```

---

## 三、快速部署 Node.js 服务

### 3.1 服务端入口文件

```javascript
// server/src/index.js
const express = require('express')
const app = express()

// ⚠️ 微信云托管必须监听 80 端口
const PORT = process.env.PORT || 80

// 解析 JSON 请求体
app.use(express.json())

// 跨域（如果小程序和云托管不在同一域名）
app.use((req, res, next) => {
  res.header('Access-Control-Allow-Origin', '*')
  res.header('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
  res.header('Access-Control-Allow-Headers', 'Content-Type, Authorization')
  next()
})

// 路由
const userRouter = require('./routes/user')
const orderRouter = require('./routes/order')
app.use('/api/user', userRouter)
app.use('/api/order', orderRouter)

// 微信云托管健康检查（必须保留）
app.get('/health', (req, res) => {
  res.json({ status: 'ok', timestamp: Date.now() })
})

// 全局错误处理
app.use((err, req, res, next) => {
  console.error('[Server Error]', err)
  res.status(500).json({ code: -1, message: 'Internal Server Error' })
})

app.listen(PORT, () => {
  console.log(`云托管服务运行在端口 ${PORT}`)
})
```

### 3.2 Dockerfile

```dockerfile
# 云托管推荐基础镜像
FROM node:18-alpine

# 工作目录
WORKDIR /app

# 复制 package.json（利用 Docker 缓存层）
COPY package*.json ./

# 安装依赖（生产环境）
RUN npm ci --only=production

# 复制源代码
COPY src/ ./src/

# ⚠️ 云托管要求以非 root 用户运行
RUN addgroup -g 1001 -S app && adduser -S app -u 1001
USER app

# 暴露端口（必须是 80）
EXPOSE 80

# 启动命令（云托管控制台也可配置）
CMD ["node", "src/index.js"]
```

### 3.3 环境变量配置（.env.example）

```bash
# .env.example（不包含敏感信息，提交到 Git）

# 数据库
DB_HOST=localhost
DB_PORT=27017
DB_NAME=production

# 微信支付
WEIXIN_MCH_ID=1234567890
WEIXIN_NOTIFY_URL=https://your-service.cloudbaseapp.com/api/pay/notify

# 日志级别
LOG_LEVEL=info
NODE_ENV=production
```

### 3.4 私密配置（云托管控制台）

> ⚠️ 以下敏感信息**绝对不能**写在代码或 .env 文件中，必须配置到云托管控制台「环境配置 → 私密配置」：

| 变量名 | 说明 | 配置位置 |
|--------|------|---------|
| `WEIXIN_MCH_KEY` | 微信支付密钥 | 云托管控制台 → 环境配置 → 私密配置 |
| `WEIXIN_PRIVATE_KEY` | 微信支付证书私钥 | 云托管控制台 → 环境配置 → 私密配置 |
| `JWT_SECRET` | JWT 签名密钥 | 云托管控制台 → 环境配置 → 私密配置 |
| `DATABASE_URL` | 数据库连接串（含密码）| 云托管控制台 → 环境配置 → 私密配置 |

### 3.5 小程序端调用云托管

```javascript
// config.js — 云托管服务地址配置
const CLOUDBASE_HOST = 'https://your-service.cloudbaseapp.com'  // 从云托管控制台获取

// 调用云托管 API
async function request(path, method = 'GET', data = {}) {
  const token = wx.getStorageSync('token')  // JWT token

  const res = await wx.request({
    url: `${CLOUDBASE_HOST}${path}`,
    method,
    header: {
      'Content-Type': 'application/json',
      'Authorization': token ? `Bearer ${token}` : '',
    },
    data,
  })

  if (res.statusCode !== 200) {
    throw new Error(`请求失败: ${res.statusCode}`)
  }

  return res.data
}

// 使用示例
const user = await request('/api/user/profile')
const orders = await request('/api/order/list', 'POST', { page: 1, pageSize: 20 })
```

---

## 四、微信支付（云托管模式）

> 云托管模式下，支付签名逻辑完全在后端容器中完成，更加安全。

### 4.1 统一下单接口（云托管后端）

```javascript
// server/src/routes/order.js
const express = require('express')
const router = express.Router()
const crypto = require('crypto')
const axios = require('axios')  // npm install axios

// POST /api/order/create
router.post('/create', async (req, res) => {
  const { totalFee, goodsName, openid } = req.body

  if (!openid) return res.status(400).json({ code: -1, message: 'openid is required' })

  // 从私密配置读取
  const mchId = process.env.WEIXIN_MCH_ID
  const mchKey = process.env.WEIXIN_MCH_KEY   // ← 云托管私密配置
  const notifyUrl = process.env.WEIXIN_NOTIFY_URL

  // 生成商户订单号
  const outTradeNo = `${mchId}${Date.now()}${Math.random().toString(36).slice(2, 8)}`

  // 构造统一下单参数（按 ASCII 字典序排序）
  const params = {
    appid: process.env.WEIXIN_APP_ID,
    mch_id: mchId,
    nonce_str: crypto.randomBytes(16).toString('hex'),
    body: goodsName,
    out_trade_no: outTradeNo,
    total_fee: totalFee,          // 单位：分（整数）
    spbill_create_ip: req.ip,
    notify_url: notifyUrl,
    trade_type: 'JSAPI',
    openid,
  }

  // 生成签名
  const sign = generateSign(params, mchKey)
  const signedParams = { ...params, sign }

  // 调用微信支付统一下单 API（XML 格式）
  const xmlParams = toXml(signedParams)
  const wxRes = await axios.post(
    'https://api.mch.weixin.qq.com/pay/unifiedorder',
    xmlParams,
    { headers: { 'Content-Type': 'text/xml' } }
  )

  const result = await parseXml(wxRes.data)

  if (result.return_code !== 'SUCCESS' || result.result_code !== 'SUCCESS') {
    return res.status(400).json({ code: -2, message: result.return_msg })
  }

  // 生成小程序调起支付的参数（时间戳+随机字符串+prepay_id+签名）
  const payParams = {
    appId: process.env.WEIXIN_APP_ID,
    timeStamp: String(Math.floor(Date.now() / 1000)),
    nonceStr: crypto.randomBytes(16).toString('hex'),
    package: `prepay_id=${result.prepay_id}`,
    signType: 'HMAC-SHA256',
  }
  payParams.paySign = generateSign(payParams, mchKey)

  // 保存订单到数据库
  await db.collection('orders').add({
    data: { outTradeNo, openid, goodsName, totalFee, status: 'pending', createdAt: new Date() }
  })

  res.json({ code: 0, orderId: outTradeNo, payParams })
})

// 生成签名（HMAC-SHA256）
function generateSign(params, key) {
  const keys = Object.keys(params).sort()
  const str = keys.map(k => `${k}=${params[k]}`).join('&')
  const signStr = `${str}&key=${key}`
  return crypto.createHmac('sha256', key).update(signStr, 'utf8').digest('hex').toUpperCase()
}

// XML 工具函数
function toXml(obj) {
  return '<xml>' + Object.entries(obj)
    .map(([k, v]) => `<${k}><![CDATA[${v}]]></${k}>`)
    .join('') + '</xml>'
}

async function parseXml(xml) {
  const result = {}
  const matches = xml.matchAll(/<(\w+)><!\[CDATA\[([^\]]+)\]\]><\/\1>/g)
  for (const m of matches) result[m[1]] = m[2]
  return result
}
```

---

## 五、定时任务（Cron Job）

> 云托管容器常驻，适合运行定时任务。

### 5.1 Node.js 定时任务

```javascript
// server/src/cron/cleanup.js
// 每天凌晨 2 点清理过期订单
const cron = require('node-cron')  // npm install node-cron

// ⚠️ 微信云托管每个实例是独立的，多实例时需用分布式锁
const cronTask = cron.schedule('0 2 * * *', async () => {
  console.log('[Cron] 开始清理过期订单', new Date())

  const expiredOrders = await db.collection('orders')
    .where({
      status: 'pending',
      createdAt: { $lt: new Date(Date.now() - 30 * 60 * 1000) }  // 30分钟前
    })
    .get()

  for (const order of expiredOrders.data) {
    await closeOrder(order.outTradeNo)
    await db.collection('orders').doc(order._id).update({
      data: { status: 'closed' }
    })
  }

  console.log(`[Cron] 清理完成，共处理 ${expiredOrders.data.length} 条订单`)
})

// 在 index.js 中启动
app.use(cronTask)
```

### 5.2 微信云托管定时触发器

在云托管控制台配置触发器：

```json
{
  "trigger": {
    "name": "daily-cleanup",
    "type": "timer",
    "config": "0 0 2 * * * *"  // cron 表达式：每天凌晨 2 点
  }
}
```

> 云托管 HTTP 触发器地址：`https://<service-id>.cloudbaseapp.com/<path>`

---

## 六、HTTP 触发器（Webhook）

> 微信支付回调、第三方 webhook 等外部请求直接打到云托管容器。

```javascript
// server/src/routes/webhook.js

// 微信支付结果通知（云托管模式）
router.post('/pay/notify', async (req, res) => {
  const xmlData = req.body

  // 解析 XML（略）
  const result = await parseXml(xmlData)

  // ⚠️ 验签
  const isValid = verifySign(result, process.env.WEIXIN_MCH_KEY)
  if (!isValid) {
    return res.send(toXml({ return_code: 'FAIL', return_msg: '签名错误' }))
  }

  if (result.return_code !== 'SUCCESS') {
    return res.send(toXml({ return_code: 'SUCCESS' }))  // 告诉微信收到
  }

  // 更新订单状态
  await db.collection('orders').where({ outTradeNo: result.out_trade_no }).update({
    data: { status: 'paid', transactionId: result.transaction_id }
  })

  // 返回 SUCCESS 告知微信不要重发
  res.send(toXml({ return_code: 'SUCCESS' }))
})
```

---

## 七、自动扩缩容

云托管控制台配置：

| 配置项 | 建议值 |
|--------|--------|
| 最小实例数 | 1（保证冷启动后有实例）|
| 最大实例数 | 5（控制成本）|
| 扩缩容条件 | CPU > 60% 或 内存 > 70% |
| 预付费实例 | 1 个（保底），超出按量计费 |
| 健康检查 | `/health` 接口，间隔 30s |

---

## 八、Common Mistakes（云托管高频错误）

| 错误 | 正确做法 |
|------|---------|
| 监听非 80 端口 | 云托管容器必须监听 80 端口（或通过控制台配置）|
| 私密信息写在代码中 | 密钥存云托管控制台「私密配置」，代码只读环境变量 |
| 多实例下定时任务重复执行 | 使用分布式锁（如 Redis SETNX）或使用云托管控制台的定时触发器 |
| 没有 /health 接口 | 必须保留健康检查接口，否则扩缩容无法判断实例状态 |
| 容器镜像太大 | 多阶段构建 + `.dockerignore` 精简镜像 |
| 环境变量名错误 | 云托管环境变量名区分大小写，必须完全匹配 `process.env.XXX` |

---

## 九、官方文档链接

- 云托管概述：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/run/CloudBase.html
- 部署 Node.js 服务：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/run/custom.html
- 环境变量与私密配置：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/run/config.html
- 定时触发器：https://developers.weixin.qq.com/miniprogram/dev/wxcloud/run/trigger.html
- 微信支付云托管模式：https://pay.weixin.qq.com/doc/v3/partner/4012529192
