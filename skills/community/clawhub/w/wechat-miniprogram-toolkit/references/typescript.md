# 微信小程序 TypeScript 支持全指南

## 激活契约

**符合以下任一场景时加载：**
- 小程序 TypeScript、TS 类型、泛型封装
- 微信小程序 + TypeScript、miniprogram types
- 小程序 WXML 类型提示、Taro / uni-app 类型
- API 返回值类型、Page/Component 泛型
- 小程序云函数 TypeScript、wxs 类型

---

## 一、项目初始化（TypeScript 模式）

### 1.1 微信开发者工具开启 TS

微信开发者工具 → 工具 → 构建 npm（首次需先 npm init）
→ 勾选「使用 TypeScript 编译」→ 开始使用

### 1.2 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "moduleResolution": "node",
    "allowSyntheticDefaultImports": true,
    "esModuleInterop": true,
    "resolveJsonModule": true,
    "sourceMap": true,
    "baseUrl": ".",
    "paths": {
      "@/*": ["miniprogram/*"],
      "@utils/*": ["miniprogram/utils/*"],
      "@components/*": ["miniprogram/components/*"],
      "@services/*": ["miniprogram/services/*"]
    }
  },
  "include": ["miniprogram/**/*"],
  "exclude": ["node_modules", "miniprogram_dist"]
}
```

### 1.3 小程序类型定义包

```bash
npm install --save-dev miniprogram-typings
# 或使用腾讯官方类型包
npm install --save-dev wechat-miniprogram @types/node
```

```json
// tsconfig.json 中添加类型路径
{
  "compilerOptions": {
    "typeRoots": ["./typings", "./node_modules/@types"],
    "paths": {
      "miniprogram": ["node_modules/miniprogram-typings"]
    }
  }
}
```

### 1.4 小程序全局类型声明

```typescript
// typings/miniprogram.d.ts
import 'miniprogram-typings'

// 扩展 Page 的 data 类型（通过装饰器注入）
declare module 'miniprogram' {
  interface IPage {
    // 自定义页面数据字段（使用时在具体页面覆盖）
  }

  interface IComponent {
    // 自定义组件数据字段
  }
}

// 声明全局 wx 对象的方法
declare const wx: WechatMiniprogram.Wx
declare const getApp: () => AppInstance
```

---

## 二、Page 和 Component 泛型

### 2.1 带类型的 Page

```typescript
// 定义页面数据接口
interface IndexPageData {
  userInfo: UserInfo | null
  loading: boolean
  posts: Post[]
  hasMore: boolean
}

interface IndexPageOptions {
  id: string  // 页面参数类型
}

class IndexPage extends Proxy<Page> {
  // ⚠️ 小程序不支持 ES6 class 继承 Page
  // 使用泛型方式：
}

// 推荐：独立定义 data 类型，在 onLoad 中手动指定
Page({
  data: {
    userInfo: null,
    loading: false,
    posts: [],
    hasMore: true,
  } as IndexPageData,

  async onLoad(options: IndexPageOptions) {
    // options 的类型安全
    console.log(options.id)
  },

  async onPullDownRefresh() {
    await this.fetchData()
    wx.stopPullDownRefresh()
  },

  // 方法参数类型化
  handleTap(postId: string) {
    wx.navigateTo({ url: `/pages/post/detail?id=${postId}` })
  },
})
```

### 2.2 Component 泛型（推荐）

```typescript
// components/goods-card/types.ts
export interface GoodsCardProps {
  goods: GoodsItem
  mode: 'list' | 'grid'
  showPrice?: boolean  // 可选字段
}

export interface GoodsCardState {
  expanded: boolean
  loading: boolean
}

// components/goods-card/index.ts
Component({
  properties: {
    goods: {
      type: Object,
      value: {} as GoodsItem,
    },
    mode: {
      type: String,
      value: 'list',
    },
    showPrice: {
      type: Boolean,
      value: true,
    },
  },

  data: {
    expanded: false,
    loading: false,
  } as GoodsCardState,

  methods: {
    toggleExpand() {
      this.setData({ expanded: !this.data.expanded })
    },

    onBuy(goodsId: string) {
      // 触发事件，通知父组件
      this.triggerEvent('buy', { goodsId })
    },
  },
})
```

### 2.3 页面引用组件并传入数据

```xml
<!-- pages/index/index.wxml -->
<goods-card
  goods="{{item}}"
  mode="list"
  bind:buy="onBuyGoods"
/>
```

```typescript
// pages/index/index.ts
Page({
  data: {
    items: [] as GoodsItem[],
  },

  onBuyGoods(e: WechatMiniprogram.CustomEvent<{ goodsId: string }>) {
    const { goodsId } = e.detail
    // goodsId 是 string 类型，IDE 有提示
  },
})
```

---

## 三、云函数 TypeScript

### 3.1 云函数项目结构

```
cloudfunctions/
├── login/
│   ├── index.ts         ← TypeScript 源码
│   ├── package.json
│   └── tsconfig.json
└── tsconfig.json        ← 全局配置
```

### 3.2 云函数 tsconfig.json

```json
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "strict": true,
    "outDir": "./dist",
    "rootDir": "./",
    "sourceMap": true,
    "esModuleInterop": true
  },
  "include": ["**/*.ts"],
  "exclude": ["node_modules", "dist"]
}
```

### 3.3 带类型的云函数

```typescript
// cloudfunctions/login/index.ts
import cloud from 'wx-server-sdk'
import { Db } from 'wx-server-sdk'

cloud.init({ env: cloud.DYNAMIC_CURRENT_ENV })

interface LoginEvent {
  userInfo: {
    nickName: string
    avatarUrl: string
  }
}

interface LoginResult {
  code: number
  action: 'login' | 'register'
  openid: string
  user?: UserRecord
}

interface UserRecord {
  _id: string
  name: string
  avatar: string
  role: string
  createdAt: Date
}

const db: Db = cloud.database()
const _ = db.command

exports.main = async (
  event: LoginEvent,
  context: cloud.ICloudContext
): Promise<LoginResult> => {
  const openid = context.OPENID

  const exist = await db.collection('users')
    .where({ _openid: openid })
    .count()

  if (exist.total === 0) {
    const addRes = await db.collection('users').add({
      data: {
        _openid: openid,
        name: event.userInfo.nickName,
        avatar: event.userInfo.avatarUrl,
        role: 'user',
        createdAt: db.serverDate(),
      }
    })
    return {
      code: 0,
      action: 'register',
      openid,
      user: { _id: addRes._id, name: event.userInfo.nickName, avatar: event.userInfo.avatarUrl, role: 'user', createdAt: new Date() },
    }
  }

  const userData = await db.collection('users')
    .where({ _openid: openid })
    .get()

  return {
    code: 0,
    action: 'login',
    openid,
    user: userData.data[0] as UserRecord,
  }
}
```

### 3.4 云函数编译脚本

```json
// cloudfunctions/tsconfig.json（全局）
{
  "compilerOptions": {
    "target": "ES2020",
    "module": "CommonJS",
    "strict": true,
    "outDir": "../dist",
    "rootDir": ".",
    "esModuleInterop": true,
    "skipLibCheck": true
  }
}
```

```javascript
// cloudfunctions/build.js（编译脚本）
const { execSync } = require('child_process')

const dirs = ['login', 'createOrder', 'payNotify', 'trackEvent']

dirs.forEach(dir => {
  console.log(`Building ${dir}...`)
  execSync(`tsc -p ${dir}/tsconfig.json`, { stdio: 'inherit' })
})
```

---

## 四、通用类型封装（推荐实践）

### 4.1 数据模型类型

```typescript
// types/models.ts

/** 小程序标准用户信息 */
interface UserInfo {
  nickName: string
  avatarUrl: string
  gender: 0 | 1 | 2  // 未知/男/女
  country: string
  province: string
  city: string
  language: 'zh_CN' | 'en'
}

/** 云开发数据库通用记录 */
interface DbRecord {
  _id: string
  _openid?: string
  createdAt?: number | Date
  updatedAt?: number | Date
}

/** 分页列表响应 */
interface PaginatedResponse<T> {
  list: T[]
  total: number
  page: number
  pageSize: number
  hasMore: boolean
}

/** 云函数通用响应 */
interface CloudResponse<T = unknown> {
  code: number
  message: string
  data?: T
}

/** 订单状态 */
type OrderStatus = 'pending' | 'paid' | 'shipped' | 'completed' | 'refunded' | 'closed'

/** 订单 */
interface Order extends DbRecord {
  outTradeNo: string
  userOpenid: string
  goodsName: string
  totalFee: number        // 单位：元
  status: OrderStatus
  transactionId?: string
  paidAt?: string
}
```

### 4.2 API 响应封装（泛型）

```typescript
// utils/request.ts

/** 云函数调用的类型安全封装 */
class CloudRequest {
  async call<T = unknown>(
    name: string,
    data?: Record<string, unknown>
  ): Promise<CloudResponse<T>> {
    try {
      const res = await wx.cloud.callFunction({
        name,
        data: data ?? {},
      })

      return res.result as CloudResponse<T>
    } catch (err) {
      return {
        code: -1,
        message: err instanceof Error ? err.message : '网络异常',
      }
    }
  }

  /** 带分页的云函数调用 */
  async callWithPagination<T>(
    name: string,
    params: { page: number; pageSize: number } & Record<string, unknown>
  ): Promise<PaginatedResponse<T>> {
    const res = await this.call<{
      list: T[]
      total: number
    }>(name, params)

    if (res.code !== 0) {
      throw new Error(res.message)
    }

    return {
      list: res.data?.list ?? [],
      total: res.data?.total ?? 0,
      page: params.page,
      pageSize: params.pageSize,
      hasMore: (params.page - 1) * params.pageSize + (res.data?.list?.length ?? 0) < (res.data?.total ?? 0),
    }
  }
}

export const cloudRequest = new CloudRequest()

// 使用示例
const res = await cloudRequest.call<UserRecord>('login', { userInfo })
if (res.code === 0 && res.data) {
  const user: UserRecord = res.data  // 类型安全
}
```

### 4.3 Storage 封装（泛型）

```typescript
// utils/storage.ts

class Storage<T> {
  constructor(private key: string) {}

  get(): T | null {
    const raw = wx.getStorageSync(this.key)
    if (!raw) return null
    try {
      return JSON.parse(raw) as T
    } catch {
      return null
    }
  }

  set(value: T): void {
    wx.setStorageSync(this.key, JSON.stringify(value))
  }

  remove(): void {
    wx.removeStorageSync(this.key)
  }

  update(patch: Partial<T>): void {
    const current = this.get() ?? ({} as T)
    this.set({ ...current, ...patch } as T)
  }
}

// 使用示例
const userStorage = new Storage<UserInfo>('userInfo')
const user = userStorage.get()

const tokenStorage = new Storage<string>('token')
tokenStorage.set('abc123')

const orderCache = new Storage<Order[]>('recentOrders')
orderCache.update({ orderList: [...] })
```

### 4.4 WXS 工具函数类型

```typescript
// wxs/common.wxs（混写 TS 需要在外部注释声明）

/**
 * @param {*} price - 价格（支持数字或字符串，会自动转换）
 * @param {number} decimals - 小数位数，默认2
 * @returns {string} 格式化后的价格
 */
function formatPrice(price, decimals) {
  var num = parseFloat(price.toString())
  if (isNaN(num)) return '0.00'
  return num.toFixed(decimals)
}

/**
 * @param {number} ts - 时间戳（毫秒）
 * @returns {string} 相对时间描述
 */
function relativeTime(ts: number): string {
  var diff = Date.now() - ts
  var minute = 60 * 1000
  var hour = 60 * minute
  var day = 24 * hour

  if (diff < minute) return '刚刚'
  if (diff < hour) return Math.floor(diff / minute) + '分钟前'
  if (diff < day) return Math.floor(diff / hour) + '小时前'
  return Math.floor(diff / day) + '天前'
}

module.exports = {
  formatPrice,
  relativeTime,
}
```

---

## 五、Taro / uni-app 中的类型（参考）

> 如果使用 Taro 或 uni-app 开发小程序，可以使用更完整的 TypeScript 支持：

### 5.1 Taro Page Props 泛型

```typescript
import { FC } from 'react'
import { View, Text } from '@tarojs/components'

interface IndexPageProps {
  title: string
}

const IndexPage: FC<IndexPageProps> = ({ title }) => {
  return (
    <View>
      <Text>{title}</Text>
    </View>
  )
}

IndexPage.defaultProps = {
  title: '首页',
}

export default IndexPage
```

### 5.2 uni-app 页面参数类型

```typescript
// pages/index/index.vue
<script setup lang="ts">
// uni-app 支持 <script setup lang="ts">
interface PageOptions {
  id: string
}

const props = defineProps<{
  id: string
}>()

const onLoad = (options: PageOptions) => {
  console.log(props.id ?? options.id)
}
</script>
```

---

## 六、Common Mistakes（TypeScript 高频错误）

| 错误 | 正确做法 |
|------|---------|
| `wx` 对象类型缺失 | 安装 `miniprogram-typings` 并在 `tsconfig.json` 中配置 |
| 云函数返回值类型不匹配 | 明确标注 `Promise<CloudResponse<T>>` 返回类型 |
| Page `data` 没有类型 | 手动声明 `as SomeDataInterface`，或在 `this.setData` 时类型推断 |
| WXS 不支持 TypeScript | WXS 是独立的 DSL，必须写 JS 或在外部用 TS 注释声明类型 |
| 泛型参数过于宽泛 | 尽量用具体的 `interface` 而非 `any` |
| 云函数内使用 `async/await` 不返回 Promise | 云函数 `exports.main` 必须是 `async function`，且返回 `Promise<T>` |

---

## 七、官方文档链接

- 小程序 TypeScript：https://developers.weixin.qq.com/miniprogram/dev/tutorial/type-definition.html
- miniprogram-typings：https://www.npmjs.com/package/miniprogram-typings
- TypeScript 官方：https://www.typescriptlang.org/docs/
