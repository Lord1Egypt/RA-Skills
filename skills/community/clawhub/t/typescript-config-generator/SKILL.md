---
name: typescript-config-generator
description: 生成专业的 TypeScript 配置，支持严格模式、React、Node.js、Webpack 等多种场景，一键生成最佳实践配置。
metadata: {"clawdbot":{"emoji":"📘","requires":{},"primaryEnv":""}}
---

# TypeScript Config Generator

生成专业的 TypeScript 配置文件，适用于各种项目场景。

## 功能

- ⚡ 一键生成配置
- 🎯 多种场景预设
- 🔧 严格类型检查
- 📝 完整注释

## 预设

| 预设 | 说明 | 适用场景 |
|------|------|----------|
| strict | 严格模式 | 生产项目 |
| node | Node.js | 后端服务 |
| react | React | 前端应用 |
| minimal | 最小配置 | 快速原型 |
| library | 类库 | npm 包 |

## 使用方法

### 基本用法

```bash
# 严格模式
typescript-config-generator --preset strict

# Node.js 项目
typescript-config-generator --preset node

# React 项目
typescript-config-generator --preset react
```

### 选项

| 选项 | 说明 |
|------|------|
| `--preset, -p` | 预设类型 |
| `--output, -o` | 输出文件 |
| `--target` | 编译目标 |

## 严格模式配置

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true
  }
}
```

## 安装

```bash
npm install -g typescript
tsc --init
```
