# State Architecture（状态管理架构）

为复杂前端应用设计可扩展的状态管理方案——不只是"用哪个库"，而是如何切分、如何同步、如何避免状态腐化。

## What It Does

- 按类型分类状态（服务端状态、全局 UI、本地 UI、URL 状态、表单状态）
- 设计 Zustand store 切片结构，细化 selector 避免无效重渲染
- 用 React Query `onMutate/onError/onSettled` 实现乐观更新
- 设计轻量状态机（useReducer）或引入 XState 处理复杂流程
- 用 BroadcastChannel 实现跨 Tab 状态同步

## How to Use

当用户说「状态管理怎么设计」「store 越来越乱」「乐观更新怎么做」「要不要用状态机」时触发。先诊断症状（服务端状态混入 store、selector 粒度太粗、状态机需求），再给出针对性方案和代码。

## Requirements

- 主要针对 React 项目
- 状态库示例基于 Zustand + React Query
- 状态机示例提供轻量版（useReducer）和 XState 两种方案
