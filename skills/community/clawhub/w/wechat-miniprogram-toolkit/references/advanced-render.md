# 小程序高级渲染指南

> 整合 Skyline 官方 Worklet 动画规范 + 数学公式 + 表格全方案。

---

## 能力导航

- 需要 Worklet 动画核心规范 → 看**第一章**
- 需要 Skyline 配置 → 看**第一章**
- 需要数学公式 → 看**第二章**
- 需要表格展示 → 看**第三章**

---

## 一、Skyline 渲染引擎 & Worklet 动画

### 概述

Skyline 是微信小程序的高性能渲染引擎（类似 Flutter），对比原生渲染：

| 对比项 | 原生渲染 | Skyline |
|--------|----------|---------|
| 渲染模式 | WebView | 原生组件树 |
| 首屏速度 | 较慢 | 更快 |
| 长列表性能 | 一般 | 优秀 |
| 动画 | CSS 动画 | Worklet 原生动画 |
| 兼容性 | 基础库 ≥ 2.0 | 基础库 ≥ 3.0 |

---

### 启用 Skyline

在 `app.json` 或页面 `*.json` 中：

```json
{
  "componentFramework": "skyline",
  "renderer": "skyline"
}
```

> ⚠️ Skyline 和原生渲染不可混用，启用后所有组件走 Skyline 渲染路径。

---

### 核心概念（腾讯官方规范）

Skyline 运行在**双线程架构**中：

```
JS 线程 ←→ UI 线程（Worklet 动画在此运行）
```

**关键问题**：UI 事件需要跨线程传递到 JS 线程再回传，交互动画会有明显延迟。
**Worklet 解决**：让动画逻辑直接在 UI 线程执行，实现类原生动画体验。

### 三大核心概念

| 概念 | 说明 | 关键 API |
|------|------|----------|
| worklet 函数 | 可在 UI 线程执行的函数，顶部声明 `'worklet'` | `runOnUI()`, `runOnJS()` |
| SharedValue | 跨线程同步的变量，通过 `.value` 读写 | `shared()`, `derived()` |
| 动画驱动 | 将 SharedValue 绑定到节点样式 | `applyAnimatedStyle()` |

---

### 核心 API 速查（完整）

#### 基础 API

| 分类 | API | 说明 |
|------|-----|------|
| 基础 | `wx.worklet.shared(initialValue)` | 创建 SharedValue |
| 基础 | `wx.worklet.derived(updaterWorklet)` | 创建衍生值（类 computed） |
| 基础 | `wx.worklet.cancelAnimation(sharedValue)` | 取消动画 |

#### 动画 API

| 分类 | API | 说明 |
|------|-----|------|
| 动画 | `wx.worklet.timing(toValue, options?, callback?)` | 时间曲线动画（默认 300ms） |
| 动画 | `wx.worklet.spring(toValue, options?, callback?)` | 弹簧物理动画 |
| 动画 | `wx.worklet.decay(options?, callback?)` | 滚动衰减动画 |
| 组合 | `wx.worklet.sequence(anim1, anim2, ...)` | 依次执行多个动画 |
| 组合 | `wx.worklet.repeat(anim, reps, reverse?, callback?)` | 重复动画（reps=-1 表示无限） |
| 组合 | `wx.worklet.delay(ms, anim)` | 延迟执行 |

#### 工具 API

| API | 说明 |
|-----|------|
| `runOnUI(workletFn)` | 在 UI 线程执行 |
| `runOnJS(normalFn)` | 回调到 JS 线程（从 worklet 中调用普通函数） |

#### Easing 缓动函数

| 名称 | 效果 | 名称 | 效果 |
|------|------|------|------|
| `easing.linear` | 线性 | `easing.ease` | 缓动 |
| `easing.easeIn` | 加速 | `easing.easeOut` | 减速 |
| `easing.easeInOut` | 先加速后减速 | `easing.easeOutIn` | 先减速后加速 |

---

### 强制规则（必读）

#### ✅ 必须声明 `'worklet'`

```javascript
// ✅ 正确
function handleGesture(evt) {
  'worklet'
  offset.value += evt.deltaX
}

// ❌ 错误：缺少 worklet 声明，不会在 UI 线程执行
function handleGesture(evt) {
  offset.value += evt.deltaX
}
```

#### ✅ 必须通过 `.value` 读写 SharedValue

```javascript
// ✅ 正确
const offset = shared(0)
offset.value = 100
console.log(offset.value)

// ❌ 错误：直接赋值替换了整个对象
offset = 100
```

#### ✅ 通过 runOnJS 调用普通函数

```javascript
// ✅ 正确：worklet 中通过 runOnJS 回调 JS 线程
function showModal(msg) {
  wx.showModal({ title: msg })
}
function handleTap() {
  'worklet'
  const fn = runOnJS(showModal.bind(this))
  fn('hello')
}

// ❌ 错误：worklet 中直接调用普通 JS 函数
function handleTap() {
  'worklet'
  wx.showModal({ title: 'hello' })  // ❌ wx API 不在 worklet 中可用
}
```

#### ✅ 页面方法必须 bind(this)

```javascript
// ✅ 正确
handleTap() {
  'worklet'
  const fn = runOnJS(this.onTapDone.bind(this))
  fn('done')
}
onTapDone(msg) {
  this.setData({ status: msg })
}

// ❌ 错误：未 bind(this)，this 丢失
handleTap() {
  'worklet'
  runOnJS(this.onTapDone)('done')  // this 指向丢失
}
```

#### ✅ 访问 this.data 不能解构

```javascript
// ✅ 正确
handleTap() {
  'worklet'
  const msg = this.data.msg   // 保持引用
}

// ❌ 错误：解构 this.data 导致 Object.freeze，setData 失效
handleTap() {
  'worklet'
  const { msg } = this.data   // ❌ 解构会冻结 this.data
}
```

---

### 完整动画示例

#### 示例 1：点击按钮 → 弹性回弹

```javascript
// pages/index/index.js
const { shared, spring, runOnJS } = wx.worklet  // 在文件顶部解构

Page({
  data: { animStyle: '' },

  onReady() {
    this._scale = shared(1)  // ✅ 在 onReady 创建一次，后续复用

    // 绑定样式到 #box（只绑定一次）
    this.applyAnimatedStyle('#box', () => {
      'worklet'
      return { transform: `scale(${this._scale.value})` }
    })
  },

  handleTap() {
    'worklet'
    // 触发弹簧动画
    this._scale.value = spring(1.2, { damping: 15, stiffness: 200 })
    // 回弹
    setTimeout(() => {
      this._scale.value = spring(1, { damping: 15, stiffness: 200 })
    }, 300)
  },
})
```

```xml
<!-- index.wxml -->
<view id="box" class="box" bindtap="handleTap">点我</view>
```

#### 示例 2：拖拽手势跟随

```javascript
// pages/drag/drag.js
Page({
  data: { x: 0, y: 0 },
  onReady() {
    const { shared } = wx.worklet
    this.offsetX = shared(0)
    this.offsetY = shared(0)

    this.applyAnimatedStyle('#draggable', () => {
      'worklet'
      return {
        transform: `translate(${this.offsetX.value}px, ${this.offsetY.value}px)`,
      }
    })
  },

  onPan(e) {
    'worklet'
    this.offsetX.value += e.deltaX
    this.offsetY.value += e.deltaY
  },
})
```

```xml
<!-- index.wxml -->
<pan-container bind:onpan="onPan">
  <view id="draggable" class="draggable">拖我</view>
</pan-container>
```

#### 示例 3：序列动画 + 重复

```javascript
const { sequence, timing, repeat, delay, easing } = wx.worklet

// 依次放大 → 缩小 → 淡出（循环）
const anim = sequence(
  timing(1.2, { duration: 300, easing: easing.easeOut }),
  timing(1.0, { duration: 300, easing: easing.easeIn }),
  timing(0, { duration: 500, easing: easing.easeInOut }),
)

const scale = shared(1)
this.applyAnimatedStyle('#pulse', () => {
  'worklet'
  return { transform: `scale(${scale.value})`, opacity: scale.value }
})

scale.value = repeat(anim, -1, true)  // -1=无限循环, true=每次反向
```

---

## 二、数学公式渲染

### 方案一：Unicode 轻量方案（零依赖，推荐）

适用于简单公式，直接使用 Unicode 符号：

```
加:  +    减:  −    乘:  ×    除:  ÷
等于: =   不等: ≠   约等: ≈
根号: √   求和: ∑   积分: ∫   偏导: ∂
α α  β β  γ γ  θ θ  π π  σ σ
上标: ⁰¹²³⁴⁵⁶⁷⁸⁹ⁿ⁺⁻⁼⁽⁾
下标: ₀₁₂₃₄₅₆₇₈₉ₙ₊₋₌₍₎
```

**工具函数（可直接使用）：**

```javascript
// utils/mathSymbol.js
const GREEK_MAP = {
  alpha: 'α', beta: 'β', gamma: 'γ', delta: 'δ', epsilon: 'ε',
  theta: 'θ', lambda: 'λ', mu: 'μ', pi: 'π', sigma: 'σ',
  phi: 'φ', psi: 'ψ', omega: 'ω',
  Gamma: 'Γ', Delta: 'Δ', Theta: 'Θ', Lambda: 'Λ',
  Pi: 'Π', Sigma: 'Σ', Phi: 'Φ', Psi: 'Ψ', Omega: 'Ω',
}

function latexToUnicode(latex) {
  let r = latex
  for (const [k, v] of Object.entries(GREEK_MAP)) r = r.replace(new RegExp(k, 'g'), v)
  r = r.replace(/\\sum/g, '∑').replace(/\\int/g, '∫').replace(/\\infty/g, '∞')
  r = r.replace(/\\sqrt/g, '√').replace(/\\partial/g, '∂').replace(/\\nabla/g, '∇')
  r = r.replace(/\\leq/g, '≤').replace(/\\geq/g, '≥').replace(/\\neq/g, '≠')
  r = r.replace(/\\frac{([^}]+)}{([^}]+)}/g, '($1)⁄($2)')
  r = r.replace(/\^{([^}]+)}/g, m => [...m.slice(2,-1)].map(c => ({'0':'⁰','1':'¹','2':'²','3':'³','4':'⁴','5':'⁵','6':'⁶','7':'⁷','8':'⁸','9':'⁹','n':'ⁿ','+':'⁺','-':'⁻'})[c]||c).join(''))
  r = r.replace(/_{([^}]+)}/g, m => [...m.slice(2,-1)].map(c => ({'0':'₀','1':'₁','2':'₂','3':'₃','4':'₄','5':'₅','6':'₆','7':'₇','8':'₈','9':'₉','n':'ₙ'})[c]||c).join(''))
  return r
}

// 使用示例
console.log(latexToUnicode('E = mc^2'))                   // E = mc²
console.log(latexToUnicode('\\frac{-b \\pm \\sqrt{b^2-4ac}}{2a}'))  // (−b±√(b²−4ac))⁄(2a)
console.log(latexToUnicode('\\sum_{i=1}^{n} x_i'))        // ∑ᵢ₌₁ⁿxᵢ
```

### 方案二：WebView + KaTeX（完整公式，推荐）

**HTML 模板（上传到云存储）：**

```html
<!DOCTYPE html>
<html>
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.css">
  <script src="https://cdn.jsdelivr.net/npm/katex@0.16.9/dist/katex.min.js"></script>
  <style>
    body { font-size: 20px; padding: 20px; text-align: center; background: transparent; }
    .formula { margin: 20px auto; }
  </style>
</head>
<body>
  <div class="formula" id="f1"></div>
  <div class="formula" id="f2"></div>
  <script>
    const formulas = JSON.parse(decodeURIComponent(location.search.slice(1)))
    formulas.forEach((latex, i) => katex.render(latex, document.getElementById('f'+(i+1)), {
      throwOnError: false, displayMode: true
    }))
  </script>
</body>
</html>
```

```javascript
// 加载公式页
async function loadMathPage(formulas) {
  const tpl = `<!DOCTYPE html><html><head>...${htmlContent}...</head><body>...</body></html>`
  const url = `data:text/html;charset=utf-8,${encodeURIComponent(tpl)}?${encodeURIComponent(JSON.stringify(formulas))}`
  this.setData({ mathUrl: url })
}

// 在 wxml 中
// <web-view src="{{mathUrl}}" />
```

### 方案三：服务端图片渲染

服务端 Python 将 LaTeX 转为 PNG base64（需要 matplotlib + 小字体）：

```python
import io, base64, matplotlib.pyplot as plt

def latex_to_b64(latex, fontsize=18):
    fig, ax = plt.subplots(figsize=(0.01, 0.01))
    fig.patch.set_alpha(0)
    ax.text(0.5, 0.5, f'${latex}$', fontsize=fontsize, ha='center', va='center', transform=ax.transAxes)
    ax.axis('off')
    buf = io.BytesIO()
    fig.savefig(buf, format='png', dpi=150, bbox_inches='tight', transparent=True, pad_inches=0.05)
    plt.close(fig)
    return 'data:image/png;base64,' + base64.b64encode(buf.getvalue()).decode()
```

---

## 三、表格展示

### 方案一：Flex 表格（推荐）

```xml
<view class="table">
  <!-- 表头 -->
  <view class="tr header">
    <view class="th" style="width:25%">姓名</view>
    <view class="th" style="width:25%">科目</view>
    <view class="th" style="width:25%">分数</view>
    <view class="th" style="width:25%">等级</view>
  </view>
  <!-- 数据行 -->
  <block wx:for="{{rows}}" wx:key="index">
    <view class="tr {{item.highlight ? 'highlight' : ''}}">
      <view class="td" style="width:25%">{{item.name}}</view>
      <view class="td" style="width:25%">{{item.subject}}</view>
      <view class="td {{item.score >= 90 ? 'score-a' : ''}}" style="width:25%">{{item.score}}</view>
      <view class="td" style="width:25%"><text class="badge {{item.level}}">{{item.level}}</text></view>
    </view>
  </block>
</view>
```

```css
.table { display: flex; flex-direction: column; border: 1rpx solid #e0e0e0; border-radius: 8rpx; overflow: hidden; }
.tr { display: flex; border-bottom: 1rpx solid #f0f0f0; }
.tr:last-child { border-bottom: none; }
.tr.highlight { background: #fff9e6; }
.header .th { background: #f5f5f5; font-weight: bold; color: #333; }
.th, .td { flex: 1; padding: 20rpx 16rpx; text-align: center; border-right: 1rpx solid #f0f0f0; font-size: 26rpx; }
.th:last-child, .td:last-child { border-right: none; }
.badge { display: inline-block; padding: 4rpx 16rpx; border-radius: 20rpx; font-size: 22rpx; }
.badge.A { background: #52c41a; color: #fff; }
.badge.B { background: #1890ff; color: #fff; }
.badge.C { background: #faad14; color: #fff; }
.score-a { color: #52c41a; font-weight: bold; }
```

### 方案二：合并单元格（多级表头）

```xml
<view class="table">
  <view class="tr">
    <view class="th" style="width:20%" rowspan="2">姓名</view>
    <view class="th" style="width:60%" colspan="3">成绩</view>
    <view class="th" style="width:20%" rowspan="2">总评</view>
  </view>
  <view class="tr">
    <view class="th" style="width:20%">数学</view>
    <view class="th" style="width:20%">语文</view>
    <view class="th" style="width:20%">英语</view>
  </view>
  <block wx:for="{{data}}">
    <view class="tr">
      <view class="td" style="width:20%">{{item.name}}</view>
      <view class="td" style="width:20%">{{item.math}}</view>
      <view class="td" style="width:20%">{{item.chinese}}</view>
      <view class="td" style="width:20%">{{item.english}}</view>
      <view class="td" style="width:20%">{{item.avg}}</view>
    </view>
  </block>
</view>
```

### 方案三：横向滚动表格（列数多时）

```xml
<scroll-view scroll-x class="table-scroll">
  <view class="table">
    <view class="tr header">
      <block wx:for="{{columns}}">
        <view class="th" style="width:220rpx;min-width:220rpx">{{item}}</view>
      </block>
    </view>
    <block wx:for="{{rows}}">
      <view class="tr">
        <block wx:for="{{columns}}" wx:for-item="col">
          <view class="td" style="width:220rpx;min-width:220rpx">{{item[col]}}</view>
        </block>
      </view>
    </block>
  </view>
</scroll-view>
```

```css
.table-scroll { white-space: nowrap; }
.table { display: inline-table; }
.th, .td { display: table-cell; }
```

---

## 四、WXS 脚本模式（性能优化参考）

> WXS（WeiXin Script）是微信小程序的一套脚本语言，可以在 WXML 中直接使用，类似过滤器，用于减少 JS 线程通信。

```xml
<!-- wxml -->
<wxs module="utils" src="./utils.wxs"></wxs>
<view>{{utils.formatPrice(price)}}</view>
<view>{{utils.timeAgo(timestamp)}}</view>
<view>{{utils.truncate(text, 20)}}</view>
```

```javascript
// utils.wxs（WXS 语法，与普通 JS 有差异）
var formatPrice = function(price) {
  if (typeof price !== 'number') return price
  return '¥' + (price / 100).toFixed(2)
}

var timeAgo = function(ts) {
  if (!ts) return ''
  var now = Date.now()
  var diff = now - ts
  if (diff < 60000) return '刚刚'
  if (diff < 3600000) return Math.floor(diff / 60000) + '分钟前'
  if (diff < 86400000) return Math.floor(diff / 3600000) + '小时前'
  return Math.floor(diff / 86400000) + '天前'
}

var truncate = function(str, len) {
  if (!str || str.length <= len) return str
  return str.slice(0, len) + '...'
}

module.exports = {
  formatPrice: formatPrice,
  timeAgo: timeAgo,
  truncate: truncate,
}
```

> ⚠️ WXS 只支持 ES5 语法，不支持 ES6+ 特性。
