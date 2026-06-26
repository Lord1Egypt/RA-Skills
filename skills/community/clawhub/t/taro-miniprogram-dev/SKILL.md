---
name: taro-miniprogram-dev
description: Taro + React + TypeScript 微信小程序开发框架技能。适用于：(1) 从零初始化 Taro 项目并编译为微信小程序；(2) 创建页面、组件、样式；(3) 搭建 services 请求层（接入真实后端或 Mock 数据）；(4) 配置 TabBar、页面路由、设计系统。触发关键词：小程序开发、Taro开发、微信小程序、mini program、Taro框架、项目初始化。
---

# Taro 小程序开发技能

基于 Taro 3 + React + TypeScript 的微信小程序开发框架。

## 项目初始化

```bash
# 创建项目目录
mkdir my-project && cd my-project

# 初始化 Taro 项目
npx @tarojs/cli init . --framework react --typescript

# 安装依赖
npm install

# 开发模式
NODE_OPTIONS=--openssl-legacy-provider npm run dev:weapp

# 生产构建
NODE_OPTIONS=--openssl-legacy-provider npm run build:weapp
```

> ⚠️ Node.js ≥ 18 时，webpack 需要 `--openssl-legacy-provider`。

## 目录结构

```
src/
├── app.config.js       # 全局配置（页面注册、TabBar、窗口样式）
├── app.tsx             # 应用入口
├── styles/
│   └── global.scss     # 全局样式 + 设计系统变量
├── pages/              # 页面
│   └── {module}/
│       └── {page}/index.tsx + index.scss
├── services/           # 接口层（接入时创建）
│   ├── api/           # API 接口定义（按模块拆分）
│   ├── utils/
│   │   └── request.ts # 请求封装
│   └── mock.ts        # Mock 数据
└── assets/            # 静态资源
```

## 页面开发

详见 [references/pages.md](references/pages.md)

```typescript
// pages/demo/index.tsx
import { Component } from 'react'
import { View, Text } from '@tarojs/components'
import './index.scss'

export default class DemoPage extends Component {
  state = { data: null as any, loading: false }

  componentDidMount() {
    // TODO: 加载数据
  }

  render() {
    const { data } = this.state
    return (
      <View className="page">
        <Text>页面内容</Text>
      </View>
    )
  }
}
```

## 接口层接入

详见 [references/api-design.md](references/api-design.md)

```typescript
// services/utils/request.ts
const IS_MOCK = true           // 切换 Mock/真实接口
const BASE_URL = 'https://api.example.com'
```

```typescript
// services/api/index.ts
import { get, post } from '../utils/request'

export function getUserInfo() {
  return get<UserInfo>('/api/auth/user-info')
}

export function login(params: LoginParams) {
  return post<LoginResult>('/api/auth/login', params)
}
```

## 设计系统

详见 [references/design-system.md](references/design-system.md)

全局样式变量：`$bg`, `$pink`, `$pink-deep`, `$ink`, `$muted`, `$line`

组件类名：`.card`, `.btn-primary`, `.btn-ghost`, `.pill`, `.bottom-nav`

## 编译说明

微信开发者工具导入 `dist/` 目录，AppID 先用测试号 `touristappid`，开发阶段开启"不校验合法域名"。

## 常用命令

| 命令 | 说明 |
|------|------|
| `npm run dev:weapp` | 微信小程序开发模式 |
| `npm run build:weapp` | 微信小程序生产构建 |
| `npm run dev:h5` | H5 开发模式 |
