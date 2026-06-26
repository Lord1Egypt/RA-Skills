---
name: vercel-react-best-practices-cn
description: |
  来自 Vercel 工程团队的 React 和 Next.js 性能优化指南。在编写、审查或重构 React/Next.js 代码时使用此 Skill 以确保最佳性能模式。触发于涉及 React 组件、Next.js 页面、数据获取、包优化或性能改进的任务。
license: MIT
metadata:
  author: vercel
  version: "1.0.0"
  language: zh-CN
---

# Vercel React 最佳实践

React 和 Next.js 应用的全面性能优化指南，由 Vercel 维护。包含 8 个类别的 64 条规则，按影响优先级排序，指导自动化重构和代码生成。

## 应用时机

在以下情况下参考这些指南：
- 编写新的 React 组件或 Next.js 页面
- 实现数据获取（客户端或服务端）
- 审查代码性能问题
- 重构现有 React/Next.js 代码
- 优化包大小或加载时间

## 按优先级分类的规则类别

| 优先级 | 类别 | 影响 | 前缀 |
|--------|------|------|------|
| 1 | 消除瀑布流 | 关键 | `async-` |
| 2 | 包大小优化 | 关键 | `bundle-` |
| 3 | 服务端性能 | 高 | `server-` |
| 4 | 客户端数据获取 | 中高 | `client-` |
| 5 | 重渲染优化 | 中 | `rerender-` |
| 6 | 渲染性能 | 中 | `rendering-` |
| 7 | JavaScript 性能 | 中低 | `js-` |
| 8 | 高级模式 | 低 | `advanced-` |

## 快速参考

### 1. 消除瀑布流（关键）

- `async-defer-await` - 将 await 移到实际使用的分支中
- `async-parallel` - 对独立操作使用 Promise.all()
- `async-dependencies` - 对部分依赖使用 better-all
- `async-api-routes` - 在 API 路由中早启动 Promise，晚 await
- `async-suspense-boundaries` - 使用 Suspense 流式传输内容

### 2. 包大小优化（关键）

- `bundle-barrel-imports` - 直接导入，避免桶文件
- `bundle-dynamic-imports` - 对重组件使用 next/dynamic
- `bundle-defer-third-party` - 水合后加载分析/日志
- `bundle-conditional` - 仅在功能激活时加载模块
- `bundle-preload` - 悬停/聚焦时预加载以提升感知速度

### 3. 服务端性能（高）

- `server-auth-actions` - 像 API 路由一样认证服务器操作
- `server-cache-react` - 使用 React.cache() 进行请求级去重
- `server-cache-lru` - 使用 LRU 缓存进行跨请求缓存
- `server-dedup-props` - 避免在 RSC props 中重复序列化
- `server-hoist-static-io` - 将静态 I/O（字体、logo）提升到模块级别
- `server-serialization` - 最小化传递给客户端组件的数据
- `server-parallel-fetching` - 重构组件以并行化获取
- `server-after-nonblocking` - 使用 after() 进行非阻塞操作

### 4. 客户端数据获取（中高）

- `client-swr-dedup` - 使用 SWR 自动去重请求
- `client-event-listeners` - 去重全局事件监听器
- `client-passive-event-listeners` - 对滚动使用被动监听器
- `client-localstorage-schema` - 版本化并最小化 localStorage 数据

### 5. 重渲染优化（中）

- `rerender-defer-reads` - 不要仅订阅回调中使用的状态
- `rerender-memo` - 将昂贵工作提取到记忆化组件中
- `rerender-memo-with-default-value` - 提升默认非原始 props
- `rerender-dependencies` - 在 effects 中使用原始依赖
- `rerender-derived-state` - 订阅派生布尔值，而非原始值
- `rerender-derived-state-no-effect` - 在渲染期间派生状态，而非 effects
- `rerender-functional-setstate` - 使用函数式 setState 获得稳定回调
- `rerender-lazy-state-init` - 为昂贵值传递函数给 useState
- `rerender-simple-expression-in-memo` - 对简单原始值避免 memo
- `rerender-split-combined-hooks` - 拆分独立依赖的 hooks
- `rerender-move-effect-to-event` - 将交互逻辑放在事件处理器中
- `rerender-transitions` - 对非紧急更新使用 startTransition
- `rerender-use-deferred-value` - 延迟昂贵渲染以保持输入响应
- `rerender-use-ref-transient-values` - 对瞬态频繁值使用 refs
- `rerender-no-inline-components` - 不要在组件内定义组件

### 6. 渲染性能（中）

- `rendering-animate-svg-wrapper` - 动画 div 包装器，而非 SVG 元素
- `rendering-content-visibility` - 对长列表使用 content-visibility
- `rendering-hoist-jsx` - 将静态 JSX 提取到组件外
- `rendering-svg-precision` - 减少 SVG 坐标精度
- `rendering-hydration-no-flicker` - 对仅客户端数据使用内联脚本
- `rendering-hydration-suppress-warning` - 抑制预期的不匹配
- `rendering-activity` - 对显示/隐藏使用 Activity 组件
- `rendering-conditional-render` - 使用三元，而非 && 条件
- `rendering-usetransition-loading` - 优先使用 useTransition 处理加载状态
- `rendering-resource-hints` - 使用 React DOM 资源提示预加载
- `rendering-script-defer-async` - 在 script 标签上使用 defer 或 async

### 7. JavaScript 性能（中低）

- `js-batch-dom-css` - 通过类或 cssText 批量更改 CSS
- `js-index-maps` - 为重复查找构建 Map
- `js-cache-property-access` - 在循环中缓存对象属性
- `js-cache-function-results` - 在模块级 Map 中缓存函数结果
- `js-cache-storage` - 缓存 localStorage/sessionStorage 读取
- `js-combine-iterations` - 将多个 filter/map 合并为一个循环
- `js-length-check-first` - 在昂贵比较前检查数组长度
- `js-early-exit` - 从函数提前返回
- `js-hoist-regexp` - 在循环外提升 RegExp 创建
- `js-min-max-loop` - 用循环求 min/max 而非 sort
- `js-set-map-lookups` - 使用 Set/Map 进行 O(1) 查找
- `js-tosorted-immutable` - 使用 toSorted() 保持不可变
- `js-flatmap-filter` - 使用 flatMap 在一次遍历中映射和过滤

### 8. 高级模式（低）

- `advanced-event-handler-refs` - 在 refs 中存储事件处理器
- `advanced-init-once` - 每次应用加载初始化一次
- `advanced-use-latest` - useLatest 获得稳定回调 refs

## 使用方法

阅读单个规则文件获取详细解释和代码示例：

```
rules/async-parallel.md
rules/bundle-barrel-imports.md
```

每个规则文件包含：
- 为什么重要的简要说明
- 错误代码示例及解释
- 正确代码示例及解释
- 额外上下文和参考

## 完整编译文档

获取包含所有规则展开的完整指南：`AGENTS.md`

---

**中文翻译版** | 原版：vercel-react-best-practices
