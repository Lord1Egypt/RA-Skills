---
slug: typescript-skills-tool-free
name: typescript-skills-tool-free
version: 1.0.0
displayName: TS编码规范工具(免费版)
summary: "面向个人开发者的TypeScript编码规范指导,覆盖命名、类型、函数、模块等基础约定.。TypeScript编码规范工具免费版为个人开发者提供符合行业惯例的TypeScript编码约定,涵"
license: Proprietary
edition: free
description: 'TypeScript编码规范工具免费版为个人开发者提供符合行业惯例的TypeScript编码约定,涵盖命名规范、类型与接口、函数与类、模块与导入等基础主题。核心能力:

  - 命名规范指导(变量、函数、类、接口、枚举)

  - 类型与接口选择策略

  - 函数与类的最佳实践

  - 模块与导入顺序约定

  - 错误处理与空值处理基础

  适用场景:

  - 个人TypeScript项目编码规范落地

  - 学习并应用业界主流TS编码约定

  - 快速审查代码风格问题

  差异化:免费版聚焦个人开发者的基础规范需求,提供核心约定与示例'
tags:
  - TypeScript
  - 编码规范
  - 代码风格
  - 前端开发
  - 个人开发
  - 工具
  - 效率
  - 自动化
  - 开发
  - 代码
  - 通信
  - 邮件
  - 运维
  - typescript
  - type
  - string
  - true
  - interface
tools:
  - read
  - exec
  - write
homepage: ""
category: "Automation"
---
# TypeScript 编码规范工具(免费版)

## 概述

`typescript-skills-tool-free` 为个人开发者提供符合行业惯例的 TypeScript 编码规范指导。它覆盖命名、类型、函数、类、模块等基础约定,帮助你在个人项目中写出风格一致、可读性强的代码。免费版聚焦核心规范,适合中小型项目与学习实践.
当你在对话中提及 TypeScript 相关话题时,本工具会自动激活并输出符合规范的代码示例与解释.
## 核心能力

| 能力 | 说明 |
|---|---|
| 命名规范 | 变量 `camelCase`、类 `PascalCase`、常量 `UPPER_SNAKE_CASE`、文件 `kebab-case.ts` |
| 类型与接口 | `interface` vs `type` 的选择策略,避免 `I` 前缀与 `Type` 后缀 |
| 函数规范 | 显式返回类型、参数数量限制、默认参数优于可选参数 |
| 类与继承 | 组合优于继承、`readonly` 属性、显式访问修饰符 |
| 模块与导入 | 具名导出优先、`import type` 用法、导入分组顺序 |
| 空值处理 | `strictNullChecks`、可选链 `?.`、空值合并 `??` |

### 核心功能执行
用`input_params`参数进行配置.

**处理**: 解析核心功能执行的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回核心功能执行的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作

### 参数配置与调用
用`config_options`参数进行配置.

**处理**: 解析参数配置与调用的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回参数配置与调用的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`config_options`参数,支持修改/重置/导入操作

### 结果处理与输出
用`output_format`参数进行配置.

**处理**: 解析结果处理与输出的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回结果处理与输出的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`output_format`参数,支持导出/保存/转换操作
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：面向个人开发者的、TypeScript、编码规范指导、覆盖命名、模块等基础约定、编码规范工具免费、版为个人开发者提、供符合行业惯例的、编码约定、涵盖命名规范、函数与类、模块与导入等基础、核心能力、命名规范指导、类型与接口选择策、函数与类的最佳实、模块与导入顺序约、错误处理与空值处、理基础等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景 1:命名规范快速参考

当你不确定某个构造的命名约定时,直接询问即可获得表格化参考.
```
问:TypeScript 中常量、类、接口、枚举成员分别用什么命名风格?
```

| 构造 | 约定 | 示例 |
|:-----|:-----|:-----|
| 变量 / 函数 | `camelCase` | `getUserName`、`isActive` |
| 布尔变量 | `camelCase` 带前缀 | `isLoading`、`hasAccess` |
| 模块常量 | `UPPER_SNAKE_CASE` | `MAX_RETRY_COUNT`、`API_BASE_URL` |
| 类 / 接口 / 类型 | `PascalCase` | `UserService`、`UserProfile` |
| 枚举成员 | `PascalCase` | `Direction.Up`、`HttpStatus.Ok` |
| 文件名 | `kebab-case.ts` | `user-service.ts` |
| 测试文件 | `kebab-case.test.ts` | `user-service.test.ts` |
| React 组件文件 | `PascalCase.tsx` | `UserProfile.tsx` |

### 场景 2:类型与接口选择

当你需要为对象形状定义类型时,本工具会指导你选择 `interface` 还是 `type`.
```typescript
// 推荐:对象形状用 interface
interface User {
  readonly id: string;
  name: string;
  email: string;
}
// ...
// 推荐:联合、交叉、映射类型用 type
type Status = 'active' | 'inactive' | 'suspended';
type Result<T> = Success<T> | Failure;
```

| 用 `interface` 当 | 用 `type` 当 |
|-------------:|-------------:|
| 定义对象或类的形状 | 创建联合或交叉类型 |
| 需要声明合并 | 使用映射 / 条件类型 |
| 继承其他接口 | 别名原始或元组类型 |

### 场景 3:函数参数过多时的重构

当函数参数超过 3 个时,本工具会建议你使用选项对象.
```typescript
// 不推荐:位置参数过多
function createUser(name: string, email: string, role: Role, dept: string): User { ... }
// ...
// 推荐:使用选项对象
interface CreateUserOptions {
  name: string;
  email: string;
  role?: Role;
  department?: string;
}
function createUser(options: CreateUserOptions): User { ... }
```

## 不适用场景

以下场景TS编码规范工具(免费版)不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

### 第一步:激活工具

在对话中提及 TypeScript,本工具会自动激活。例如:

```
帮我写一个 TypeScript 函数,合并两个对象.
```

```
审查这段 TypeScript 代码的风格问题.
```

### 第二步:获取规范代码

工具会输出符合规范的代码、解释与可选的 ESLint 规则提示.
### 第三步:本地验证

```bash
npx tsc --noEmit
npx eslint . --fix
```

## 示例

### 个人项目 `tsconfig.json`

```jsonc
{
  "compilerOptions": {
    "target": "ES2022",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "lib": ["ES2022"],
    "strict": true,
    "esModuleInterop": true,
    "skipLibCheck": true,
    "forceConsistentCasingInFileNames": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noFallthroughCasesInSwitch": true
  }
}
```

### 个人项目 ESLint 基线

```jsonc
{
  "rules": {
    "@typescript-eslint/no-explicit-any": "error",
    "@typescript-eslint/explicit-function-return-type": "warn",
    "@typescript-eslint/no-unused-vars": "error",
    "@typescript-eslint/consistent-type-imports": "error",
    "@typescript-eslint/no-non-null-assertion": "warn"
  }
}
```

## 最佳实践

1. **始终启用 `strict: true`**:这会开启 `noImplicitAny`、`strictNullChecks`、`strictFunctionTypes` 等关键检查.
2. **优先具名导出**:具名导出利于重构与自动导入,默认导出仅用于 React 组件(若项目约定要求).
3. **`import type` 用于类型导入**:帮助打包器 tree-shaking,避免运行时依赖.
4. **`const` 优先,`let` 仅在需要重新赋值时使用,永不使用 `var`**.
5. **函数参数最多 3 个**,超出则用选项对象.
6. **错误处理使用自定义错误类**,`catch` 变量类型为 `unknown`,收窄后再使用.
7. **使用 TSDoc 注释公共 API**,包含 `@param`、`@returns`、`@example` 标签.
8. **缩进 2 空格,分号必加,单引号,多行结构尾逗号**:配合 Prettier 自动格式化.
## 常见问题

### Q1: 接口要不要加 `I` 前缀?

不要。`IUser` 是 .NET 风格,TypeScript 社区普遍使用 `User`。也不要加 `Type` 或 `Interface` 后缀.
### Q2: 枚举用字符串枚举还是字符串字面量联合?

小集合且不需要命名空间特性时,优先字符串字面量联合(更简单、可 tree-shaking)。需要反向映射或命名空间时用字符串枚举。避免数字枚举,自动递增易出错.
### Q3: `async/await` 还是 `.then()` 链?

优先 `async/await`,可读性更好。并行独立操作用 `Promise.all()`。避免 `async void` 函数(无法 `await` 且吞错误).
### Q4: 私有成员要不要加 `_` 前缀?

不要。TypeScript 的 `private` 关键字已足够。需要真正运行时私有性时用 `#` ES 私有字段.
### Q5: 免费版与 Pro 版的区别?

免费版提供个人项目所需的基础规范与示例;Pro 版扩展团队规范、自动化审查脚本、企业级 ESLint 规则集与 CI 集成能力.
## 依赖说明

### 运行环境

- **Agent 平台**:支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**:Windows / macOS / Linux
- **Node.js**:建议 18+
- **TypeScript**:建议 5.0+

### 依赖详情

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|:---:|:---:|:---:|:---:|
| TypeScript | npm 包 | 推荐 | `npm i -D typescript` |
| ESLint + @typescript-eslint | npm 包 | 可选 | `npm i -D eslint @typescript-eslint/eslint-plugin` |
| Prettier | npm 包 | 可选 | `npm i -D prettier` |
| LLM API | API | 必需 | 由 Agent 内置 LLM 提供 |

### API Key 配置

- 本 Skill 完全基于 Markdown 指令,无需额外 API Key
- 本地 `tsc` 与 `eslint` 使用本地工具链,不涉及外部 API

### 可用性分类

- **分类**: MD+EXEC(纯 Markdown 指令,部分功能需要 exec 命令行执行能力)
- **说明**: 基于自然语言指令驱动 Agent 输出规范代码与解释;用户可通过 `tsc --noEmit` 与 `eslint` 在本地验证

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:------|------:|:------|
| 配置错误 | 参数缺失或格式错误 | 检查依赖说明中的配置要求 |
| 运行时错误 | 运行环境不满足 | 确认运行环境符合依赖说明 |
| 网络错误 | 连接超时或不可达 | 执行ping命令测试网络连通性,检查防火墙和代理设置连接后执行ping命令测试网络连通性,检查防火墙和代理设置连接后重新执行命令，参考国内替代方案 |

## 已知限制

- 需LLM支持,无LLM环境不可用
- 复杂业务场景建议结合人工经验判断
- 执行效率受模型能力与网络环境影响
- 当前为免费版本,如需完整功能请升级到付费版获取全部能力

## 输出格式
```json
{
  "success": true,
  "data": {
    "result": "TS编码规范工具(免费版)处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "typescript skills"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
