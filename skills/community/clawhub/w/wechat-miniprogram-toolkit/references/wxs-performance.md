# 小程序 WXS & 性能优化指南

---

## 激活契约

**符合以下任一场景时加载：**
- 需要在小程序中实现高性能过滤/格式化
- setData 过慢 / 页面卡顿
- 列表渲染大数据量（>100 条）
- 需要在小程序端做实时计算（不减慢 JS 线程）
- 想让视图层和逻辑层解耦

---

## 一、WXS 脚本详解

### WXS 与 JS 的区别

| 特性 | WXS | JS |
|------|-----|-----|
| 运行线程 | 视图层（渲染线程） | 逻辑层（JS 线程） |
| 调用方式 | 在 WXML 中直接调用 | 在 JS 中调用 |
| 与 setData | **无需 setData**，直接驱动视图 | 需要 setData 更新视图 |
| ES6+ 支持 | ❌ 仅 ES5 | ✅ 完全支持 |
| 模块系统 | ✅ 支持 require | ✅ 支持 require/import |
| 异步/Promise | ❌ 不支持 | ✅ 支持 |
| 微信 API | ❌ 不可调用 | ✅ 全部可用 |
| 适用场景 | 过滤器、简单计算 | 复杂逻辑、网络请求、业务流程 |

### 核心使用场景

#### 场景 1：过滤器（最常用）

```xml
<!-- 金额格式化（分→元） -->
<wxs module="filters">
module.exports = {
  formatPrice: function(price) {
    return '¥' + (Number(price) / 100).toFixed(2)
  },
  formatDate: function(ts) {
    var d = getDate(ts)
    return d.getFullYear() + '-' + pad(d.getMonth()+1) + '-' + pad(d.getDate())
  },
  gender: function(g) {
    return ['', '男', '女'][g] || '未知'
  },
  statusText: function(s) {
    return { pending: '待处理', done: '已完成', cancel: '已取消' }[s] || s
  }
}
function pad(n) { return n < 10 ? '0' + n : n }
</wxs>

<!-- 在 WXML 中使用 -->
<text class="price">{{filters.formatPrice(order.price)}}</text>
<text>{{filters.formatDate(item.createdAt)}}</text>
<text class="tag {{item.status}}">{{filters.statusText(item.status)}}</text>
```

#### 场景 2：条件渲染增强

```xml
<wxs module="utils">
module.exports = {
  if: function(cond, truthy, falsy) { return cond ? truthy : falsy },
  unless: function(cond, val) { return cond ? '' : val },
  eq: function(a, b) { return a === b },
  gt: function(a, b) { return a > b },
  between: function(v, min, max) { return v >= min && v <= max },
}
</wxs>

<!-- 使用 -->
<text class="{{utils.eq(item.status, 'done') ? 'success' : 'pending'}}">
  {{utils.eq(item.status, 'done') ? '已完成' : '处理中'}}
</text>
```

#### 场景 3：WXS 内联（简单表达式）

```xml
<!-- WXS 内联写法，无需外部模块 -->
<text>{{(price * 0.8).toFixed(2)}}</text>
<text>{{'¥' + (price / 100).toFixed(2)}}</text>
<text>{{arr.slice(0, 3).join(',')}}</text>
```

---

## 二、性能优化

### 原则 1：减少 setData 频率

**❌ 低效：** 在每次事件中频繁 setData
```javascript
// 每次按键都触发一次 setData
input(e) {
  this.setData({ value: e.detail.value })  // 每次触发一次通信
  this.setData({ length: e.detail.value.length })  // 又一次
}
```

**✅ 高效：** 合并到一次 setData
```javascript
input(e) {
  const value = e.detail.value
  this.setData({ value, length: value.length })  // 一次搞定
}
```

**✅ 更高性能：** 使用 WXS 处理格式化，无需 setData
```xml
<wxs module="f">
module.exports = {
  len: function(s) { return s ? s.length : 0 }
}
</wxs>
<!-- 不需要 setData(length)，WXS 直接计算 -->
<text>{{f.len(inputValue)}}</text>
```

### 原则 2：减少 setData 数据量

**❌ 低效：** 整个 data 对象传进去
```javascript
this.setData({ list: this.data.list })  // 整列都传
```

**✅ 高效：** 只传变化的字段
```javascript
this.setData({ 'list[' + index + '].read': true })  // 精准修改
```

### 原则 3：列表渲染优化

```xml
<!-- ✅ 使用 wx:key，指定稳定唯一标识 -->
<block wx:for="{{posts}}" wx:key="id">
  <post-card item="{{item}}" />
</block>

<!-- ✅ 长列表使用 scroll-view + 分页加载 -->
<scroll-view scroll-y bindscrolltolower="loadMore" style="height: 100vh">
  <block wx:for="{{list}}" wx:key="id">
    <post-card item="{{item}}" />
  </block>
  <view wx:if="{{hasMore}}" class="loading">加载中...</view>
</scroll-view>
```

### 原则 4：图片优化

```xml
<!-- ✅ 指定图片尺寸，避免重排 -->
<image
  src="{{item.avatar}}"
  mode="aspectFill"
  style="width: 80rpx; height: 80rpx;"
  lazy-load="{{true}}"        <!-- 懒加载 -->
/>

<!-- ✅ 使用 CDN 图片，小程序不压缩 -->
<!-- 建议：CDN 图片控制在 100KB 以内 -->
```

### 原则 5：页面切换优化

```javascript
// onHide 时暂停非必要任务
onHide() {
  this._timer && clearInterval(this._timer)
  this._ws && this._ws.close()
},

// onShow 时恢复
onShow() {
  if (this.data.shouldResume) {
    this._initData()
  }
}
```

### 原则 6：代码包体积优化

| 优化项 | 操作 |
|--------|------|
| 图片压缩 | TinyPNG / tinypng.com 压缩到 100KB 以内 |
| 去掉调试代码 | `console.log` 上线前全部删除 |
| tree-shaking | 只 import 实际用到的模块 |
| 雪碧图 | 多张小图标合并为一张 sprite.png |
| CDN 替代本地 | 静态资源上传到 CDN，分包按需加载 |
| 分包 | 把非首页资源移到分包 |

---

## 三、生命周期优化

### 推荐页面生命周期顺序

```javascript
Page({
  data: { /* 初始状态 */ },

  // 1. 页面加载（只触发一次）
  onLoad(options) {
    this._init(options)
  },

  // 2. 页面显示（每次进入都触发）
  onShow() {
    // 不要在这里做重的操作，onShow 可能频繁触发
    if (this._needRefresh) this._loadData()
  },

  // 3. 页面初次渲染完成
  onReady() {
    this._initAnimation()   // 动画初始化放这里
    this._observeElements()  // 元素监听放这里
  },

  // 4. 页面隐藏（暂停任务）
  onHide() {
    this._pausePolling()
  },

  // 5. 页面卸载（清理资源）
  onUnload() {
    this._cleanup()
  },

  // ===== 内部方法 =====
  async _init(options) {
    // 一次性初始化
  },
  async _loadData() {
    // 加载数据
  },
  _initAnimation() {
    // 动画初始化
  },
  _pausePolling() {
    clearInterval(this._timer)
  },
  _cleanup() {
    this._pausePolling()
    this._observer && this._observer.disconnect()
  },
})
```

---

## 四、组件性能

### 组件隔离模式

```json
// 组件 *.json
{
  "component": true,
  "styleIsolation": "isolated",   // isolated: 样式隔离，不受页面影响
  "virtualHost": true,             // 虚拟化（减少节点数）
  "pureDataPattern": {
    "regexp": "^_p_"              // 以下划线 _p_ 开头的 data 不参与渲染
  }
}
```

### 组件通信优化

```javascript
// ❌ 低效：父组件频繁更新子组件
// parent.js - 每次都触发子组件更新
this.setData({ items: newItems })  // 整个列表更新

// ✅ 高效：组件内部处理逻辑
// child.js - 组件自己订阅变化
Component({
  properties: {
    userId: { type: String, observer: '_onUserIdChange' }
  },
  methods: {
    _onUserIdChange(newVal) {
      this._loadUserData(newVal)
    }
  }
})
```

---

## 五、内存优化

```javascript
// 及时释放大对象
onUnload() {
  // 取消所有定时器
  clearTimeout(this._t1)
  clearInterval(this._t2)
  clearInterval(this._t3)

  // 关闭观察者
  if (this._observer) this._observer.disconnect()

  // 清空数据引用
  this.setData({ largeList: [] })
}

// 避免循环引用
Page({
  onUnload() {
    this._callback = null  // 断开循环引用
  }
})
```

---

## 六、调试与真机测试

```javascript
// 开启性能面板（在开发者工具中）
// 微信开发者工具 → 性能 → 性能 trace

// 真机调试
// 开发者工具 → 详情 → 本地设置 → 勾选"启用真机调试"

// 查看性能数据
wx.getPerformance()  // 获取性能数据
```
