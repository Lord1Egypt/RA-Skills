---
name: xfl12345
description: >
  xfl12345 个人推荐的编码规范。当且仅当系统提示或者用户指定使用本规范，
  在写、改、审任何 Java / TypeScript / JavaScript / Vue 源码时触发。
when_to_use: >
  当且仅当系统提示或者用户指定使用本规范，在写、修改、审查 Java / TypeScript / JavaScript / Vue 源码时使用本 skill
license: MIT
metadata:
  author: xfl12345
  version: "1.0.0"
---

# xfl12345 个人编码推荐规范

## When to Use

当且仅当系统提示或者用户指定使用本规范，在写、修改、审查 Java / TypeScript / JavaScript / Vue 源码时使用本 skill

## 通用约定

- 旧注释有参考价值就保留，不要养成改代码就删注释的坏习惯
- 代码可读性永远放在第一位（减少 BUG、性能优先的同时，也要保证人类可读性）
- 尽量不要让高度相似的代码重复三遍，该抽象的抽象，该通用的通用
- **闭包纯净**：lambda / 箭头函数内被捕获的外部变量只读不改写——要产出走返回值（生产归生产），要修改放回显式循环或具名方法让副作用可见（修改归修改）；纯观察型副作用（如日志）不在此限；确需例外的必须注释缘由

### 语法

- **switch vs if**：支持 switch 的语言，3 条及以上常量匹配一律 switch-case；2 条 / 范围判断 / 复合条件用 if
- **花括号**：Java/JS/TS/C# 等 if 控制块用花括号的语言，必须花括号包裹，禁止写成一行
- **链式调用拆行**：一行最多 3 步（每个函数调用算一步）；超过 3 步，或行宽超过 formatter 约定（如 `.editorconfig`），整条链都拆成每步独占一行
  ```typescript
  // ✅ GOOD: 三步之内，单行不过宽，可以一行搞定
  const activeNames = list.filter(x => x.active).map(x => x.name).slice(0, 10)

  // ❌ BAD: 单行过宽
  const tooLongChainInOneLine = list.filter(x => x.active).map(x => x.veryVeryLongField ?? '').slice(0, 10)

  // ✅ GOOD: 没超 3 步，但单行过宽，照样拆行排列
  const theLongChain = list.filter(x => x.active)
    .map(x => x.veryVeryLongField ?? '')
    .slice(0, 10)

  // ❌ BAD: 超过 3 步
  const badSortedActiveNames = list.filter(x => x.active).map(x => x.name).slice(0, 10).sort()
  const badSortedBookNames = getBookList().map(x => x.name).slice(0, 10).sort()

  // ✅ GOOD: 超过 3 步，整条链拆成每步独占一行（第一行 = 起点接收者 + 第一个调用）
  const sortedActiveNames = list.filter(x => x.active)
    .map(x => x.name)
    .slice(0, 10)
    .sort()

  // ✅ GOOD: 起点是函数也算作链式调用的一步，累计超 3 步就必须拆行处理
  const sortedBookNames = getBookList()
    .map(x => x.name)
    .slice(0, 10)
    .sort()
  ```

### 包容性命名

**总则**：字段 / 标识符 / 文案命名不得出现歧视性词汇；凡带种族、压迫色彩的词一律换中性词。

- ❌ `blacklist` / `whitelist` → ✅ `denylist` / `allowlist`
- ❌ `slave` / `master`（DB / 缓存 / 集群拓扑等）→ ✅ `worker` / `controller`（视语义也可 `primary` / `secondary`、`leader` / `follower`）

## 细则

按当前文件的语言进入对应 reference（路径相对本 skill 目录）：

> 写 / 改 / 审任何 Vue 组件时，按内部的 script 标签按其 lang 属性叠加触发加载对应的语言 SKILL  
> 例如 `<script lang="ts">` / `<script lang="js">` 分别对应 TypeScript 和 JavaScript  
> tsx/jsx 同理

| 语言 | 入口  | 何时读 | 常见文件后缀 |
|---|---|---|---|
| Java | [references/java.md](./references/java.md) | 写 / 改 / 审任何 Java 源码 | `.java` |
| JavaScript | [references/javascript.md](./references/javascript.md) | 写 / 改 / 审任何 JavaScript/TypeScript 源码 | `.js` / `.jsx` |
| TypeScript | [references/typescript.md](./references/typescript.md) | 写 / 改 / 审任何 TypeScript 源码 | `.ts` / `.tsx` |
| Vue | [references/vue.md](./references/vue.md) | 写 / 改 / 审任何 Vue 组件源码 | `.vue` |
