---
name: javascript
description: JavaScript 编码规范。编写任何 JavaScript 源码时都应触发。
---

# JavaScript

## Coding Practices

- 禁止扩展内置对象原型（prototype）

### 空值与兜底

- 作为值用途时，一律用 `void 0` 代替 `undefined`：

  ```javascript
  // ❌ BAD: 作「值」用 undefined——可被局部变量遮蔽（`let undefined = 1` 就废了）
  const badFallback = undefined
  if (value === undefined) {
  }

  // ✅ GOOD: void 0 永远是安全的 undefined，不受遮蔽影响
  const fallback = void 0
  if (value === void 0) {
  }
  ```

- 兜底赋值用 `??`，禁用 `||`（`||` 会把 `0` / `''` / `false` 当假值，经典坑 `count || 10` 当 count=0；布尔逻辑短路如 `if (a || b)` 不在约束内）。注意：`??` 与 `&&` / `||` 混用必须显式加括号，否则直接是语法错误：

  ```javascript
  const count = 0
  const label = ''
  const enabled = false

  // ❌ BAD: || 把 0 / '' / false 都当假值，真实值被兜底吞掉
  const badCount = count || 10       // 10，丢了真实的 0
  const badLabel = label || 'anon'   // 'anon'，丢了真实的 ''
  const badFlag = enabled || true    // true，丢了真实的 false

  // ✅ GOOD: ?? 只在 null / undefined 时兜底，0 / '' / false 原样保留
  const safeCount = count ?? 10      // 0
  const safeLabel = label ?? 'anon'  // ''
  const safeFlag = enabled ?? true   // false

  // ❌ BAD: ?? 与 || 混用不写括号——语言级 SyntaxError，编译都过不了
  // const badMixed = enabled || fallback ?? 'default'

  // ✅ GOOD: 括号写明结合意图
  const safeMixed = (enabled || fallback) ?? 'default'
  ```

### 文件命名

> 文件名后缀视项目具体情况而定。例如 `.js` / `.jsx` / `.cjs` / `.mjs` 等等  
> 本规范涉及文件命名时，只定义主文件名（Main Filename）  

- 单个 JavaScript 文件只写一个主实体，文件名与主实体同名
- class：PascalCase 且与文件同名（如 `BroadcastContext.js` ↔ `class BroadcastContext {}`）
- class 组织按作用域二选一：
  - **全局通用**（跨模块复用）→ 多文件：一类一文件、PascalCase 与文件同名（即上条）
  - **局部定义**（模块 / 目录内部使用的数据契约类）→ 单文件：集中放固定名 `schemas`
- 常量集合文件固定名 `TheConst`：一个目录至多一个；集合内常量一律 SCREAMING_SNAKE_CASE
  - **依赖封闭**：只允许引用第三方库与项目 class，禁止引用任何其它项目文件
  - 缘由：常量是被广泛导入的基石，历史上经包装再导出曾放大循环引用风险——把依赖面封死，环便无从形成，re-export 无需再设防
- 工具函数文件：只含函数，文件名用 camelCase

### 优先使用 JS 原生 API

#### 数组优先用 `push` / `unshift` / `concat` / `splice` / `forEach` / `map` / `filter` / `at` 等

```javascript
let arr = [1, 2, 3]
const item = 4
const other = [5, 6]

// 目的 A：就地把元素加进 arr（不要新数组对象）
//   ❌ BAD: 展开语法：展开必然产生新数组，原地追加的场合是浪费
arr = [...arr, item]
arr = [item, ...arr]
//   ✅ GOOD: 原地修改的原生 API
arr.push(item)           // 尾部追加
arr.unshift(item)        // 头部插入
arr.splice(1, 1, item)   // 按下标 删 / 插 / 改

// 目的 B：要一份新数组（拼接 / 映射 / 过滤）
//   ❌ BAD: 手写下标循环 + 临时数组
const badDoubled = []
for (let i = 0; i < arr.length; i++) {
  badDoubled.push(arr[i] * 2)
}
//   ✅ GOOD: 返回新数组的原生 API
const merged = arr.concat(other)
const doubled = arr.map(x => x * 2)
const positives = arr.filter(x => x > 0)

// 目的 C：按下标取元素（尤其取倒数第 N 个）
//   ❌ BAD: 取末尾元素用 arr[arr.length - 1] 啰嗦；arr[-1] 是经典 bug（返回 undefined，因为 -1 不是合法索引）
const last = arr[arr.length - 1]
//   ✅ GOOD: arr.at(i)：支持负索引，at(-1) 即末尾元素
const lastEl = arr.at(-1)      // 末尾
const secondLast = arr.at(-2)  // 倒数第二
const head = arr.at(0)         // 等价 arr[0]，但取首元素用 arr[0] 更直接（非负字面量无需 at）

// 目的 D：仅遍历、不收集 → forEach（要 break / 早返回则 for-of，见下节）
arr.forEach(x => console.log(x))
```

#### 对象优先用 `Object.keys(obj)` / `Object.values(obj)` / `Object.entries(obj)` / `Object.fromEntries(entries)` / `Object.assign(...)` 等

```javascript
const obj = { a: 1, b: 2, c: 3 }
const other = { d: 4 }

// 目的 A：把对象的 键 / 值 / 键值对 收集成数组
//   ❌ BAD: for...in 手动收集（啰嗦；第三方库扩展原型时还会混入继承属性——经典坑）
const badKeys = []
for (const k in obj) {
  badKeys.push(k)
}
//   ✅ GOOD: Object.keys / values / entries，只取自身可枚举属性
const keys = Object.keys(obj)    // ['a', 'b', 'c']
const vals = Object.values(obj)  // [1, 2, 3]
const pairs = Object.entries(obj) // [['a', 1], ['b', 2], ['c', 3]]
//   注：纯遍历对象、不收集成数组时，for...in 也行（见下节）。

// 目的 B：浅拷贝 / 合并对象（要新对象）
const merged = Object.assign({}, obj, other)
const mergedSpread = { ...obj, ...other }  // 等价写法，后盖前
const overridden = { ...obj, b: 20 }       // 逐字段覆盖：{ a: 1, b: 20, c: 3 }

// 目的 C：转换对象的值（mapValues 模式）
//   ❌ BAD: for...in 手搓新对象
const badDoubled = {}
for (const k in obj) {
  badDoubled[k] = obj[k] * 2
}
//   ✅ GOOD: entries + map + fromEntries，声明式一次成型
const doubled = Object.fromEntries(
  Object.entries(obj).map(([k, v]) => [k, v * 2]),
)
```

### 尽量避免下标遍历

不修改原数组、也不需要操作下标的遍历

- ✅ `for (const item of iterable)`（数组 / 可迭代对象）
- ✅ `for (const key in obj)` 或 `for (const [k, v] of Object.entries(obj))`（对象）

只有在明确需下标或原地修改时，才使用下标遍历的方法 `for (let i = 0; i < arr.length; i++)`
