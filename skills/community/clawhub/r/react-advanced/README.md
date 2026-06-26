# React Advanced（React 进阶）

掌握 React 并发特性、Server Components、渲染优化和 Next.js App Router 架构，写出真正高性能的 React 应用。

## What It Does

- RSC vs Client Component 边界决策树，避免 `'use client'` 滥用
- Suspense 的两种用途：代码分割 vs 数据加载（配合 React Query）
- useTransition / useDeferredValue 并发特性的正确使用场景
- 用 React DevTools Profiler 定位重渲染，修复 memo/useMemo 不生效的问题
- 自定义 Hook 设计原则：封装关注点而不是打包 state
- Next.js App Router 数据获取策略与 Server Actions

## How to Use

当用户说「RSC 怎么用」「重渲染太多」「memo 没效果」「Suspense 怎么用」「Next.js App Router 架构」时触发。先判断问题类型，再给出决策树、代码示例和反模式对比。

## Requirements

- 适用于 React 18+ 项目
- Next.js 相关内容基于 App Router（Next.js 13+）
- 渲染优化部分需要 React DevTools 配合
