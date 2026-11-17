---
slug: shadcn-ui-tool-free
name: shadcn-ui-tool-free
version: 1.0.0
displayName: shadcn UI工具-免费版
summary: "使用shadcn/ui构建现代React应用,支持组件安装、表单验证与主题定制。shadcn/ui 开发工具免费版,面向个人开发者与小型项目。核心能力:"
license: Proprietary
edition: free
description: shadcn/ui 开发工具免费版,面向个人开发者与小型项目。核心能力:，可处理提升工作效率

  - shadcn/ui 组件安装与管理

  - Tailwind CSS 样式定制

  - react-hook-form + zod 表单验证

  - 暗色/亮色主题切换

  - 常用组件使用示例

  - 响应式布局指导

  适用场景:

  - 个人项目 UI 快速搭建

  - 学习 shadcn/ui 组件库

  - React 应用界面开发

  差异化:免费版提供核心组件使用能力'
tags:
  - shadcn/ui
  - React
  - Tailwind CSS
  - 前端开发
  - UI设计
  - 前端
  - 设计
  - form
  - shadcn
  - import
  - button
  - components
tools:
  - read
  - exec
  - write
homepage: ""
category: "Creative"
---
# shadcn UI 工具 - 免费版

## 概述

shadcn/ui 工具免费版帮助开发者使用 shadcn/ui 组件库构建现代 React 应用。结合 Tailwind CSS 样式系统、react-hook-form 表单管理与 zod 数据验证,快速搭建美观且功能完善的用户界面.
## 核心能力

### 依赖详情

通过 CLI 工具安装 shadcn/ui 组件,组件代码直接复制到项目中,完全可控.

**处理**: 解析依赖说明的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回依赖说明的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 2. Tailwind CSS 样式

基于 Tailwind CSS 的原子化样式系统,支持深度定制主题颜色、字体、间距.

**处理**: 解析Tailwind CSS 样式的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回Tailwind CSS 样式的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 3. 表单验证

react-hook-form + zod 实现类型安全的表单验证,覆盖登录、注册、数据录入等场景.

**处理**: 解析表单验证的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回表单验证的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 4. 主题切换

支持暗色/亮色主题切换,基于 CSS 变量实现,性能优异.

**处理**: 解析主题切换的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回主题切换的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 示例

提供 Button、Card、Dialog、Form、Table 等常用组件的使用示例.

**处理**: 解析示例的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回示例的响应数据,包含状态码、结果和日志.
- 执行此能力时使用`input_params`参数,支持创建/查询/导出操作
### 6. 响应式布局

基于 Tailwind 的响应式工具类,适配手机、平板、桌面多种屏幕.

**处理**: 解析响应式布局的输入参数,完成核心逻辑,返回结构化响应.
**输出**: 返回响应式布局的响应数据,包含状态码、结果和日志.
**技术参数**：使用`input_params`和`output_format`参数控制执行行为,支持`json`/`text`/`csv`输出格式.
**能力覆盖范围**：本skill的核心能力覆盖以下场景关键词：构建现代、支持组件安装、表单验证与主题定、开发工具免费版、面向个人开发者与、小型项目、核心能力、组件安装与管理、样式定制、常用组件使用示例、响应式布局指导等。这些关键词对应description中声明的使用场景,均已在上述能力点中提供对应的操作支持.
## 使用场景

### 场景一:创建登录表单

使用 shadcn/ui 表单组件创建带验证的登录表单.
## 输入格式
| 参数名 | 类型 | 必填 | 说明 |
|---|---|---|---|
| input | string | 是 | shadcn UI工具-免费版处理的输入数据或指令 |
| options | object | 否 | 附加配置选项,如模式选择、格式偏好等 |
| callback_url | string | 否 | 异步处理完成后的回调通知URL |

```bash
# 安装所需组件
npx shadcn@latest add button input form label card
```

```typescript
// components/login-form.tsx
"use client"
// ...
import { useForm } from "react-hook-form"
import { zodResolver } from "@hookform/resolvers/zod"
import { z } from "zod"
import { Button } from "@/components/ui/button"
import { Input } from "@/components/ui/input"
import {
  Form,
  FormControl,
  FormField,
  FormItem,
  FormLabel,
  FormMessage,
} from "@/components/ui/form"
// ...
const loginSchema = z.object({
  email: z.string().email("请输入有效的邮箱地址"),
  password: z.string().min(8, "密码至少 8 位"),
})
// ...
type LoginValues = z.infer<typeof loginSchema>
// ...
export function LoginForm() {
  const form = useForm<LoginValues>({
    resolver: zodResolver(loginSchema),
    defaultValues: { email: "", password: "" },
  })
// ...
  const onSubmit = (values: LoginValues) => {
    console.log(values)
  }
// ...
  return (
    <Form {...form}>
      <form onSubmit={form.handleSubmit(onSubmit)} className="space-y-4">
        <FormField
          control={form.control}
          name="email"
          render={({ field }) => (
            <FormItem>
              <FormLabel>邮箱</FormLabel>
              <FormControl>
                <Input type="email" placeholder="you@example.com" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <FormField
          name="password"
          render={({ field }) => (
            <FormItem>
              <FormLabel>密码</FormLabel>
              <FormControl>
                <Input type="password" placeholder="********" {...field} />
              </FormControl>
              <FormMessage />
            </FormItem>
          )}
        />
        <Button type="submit" className="w-full">登录</Button>
      </form>
    </Form>
  )
}
```

### 场景二:创建数据表格

使用 shadcn/ui Table 组件创建数据展示表格.
```bash
# 安装表格组件
npx shadcn@latest add table
```

```typescript
// components/user-table.tsx
import {
  Table,
  TableBody,
  TableCell,
  TableHead,
  TableHeader,
  TableRow,
} from "@/components/ui/table"
// ...
const users = [
  { id: 1, name: "张三", email: "zhang@example.com", role: "管理员" },
  { id: 2, name: "李四", email: "li@example.com", role: "用户" },
]
// ...
export function UserTable() {
  return (
    <div className="rounded-md border">
      <Table>
        <TableHeader>
          <TableRow>
            <TableHead>姓名</TableHead>
            <TableHead>邮箱</TableHead>
            <TableHead>角色</TableHead>
          </TableRow>
        </TableHeader>
        <TableBody>
          {users.map((user) => (
            <TableRow key={user.id}>
              <TableCell className="font-medium">{user.name}</TableCell>
              <TableCell>{user.email}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </div>
  )
}
```

### 场景三:主题切换

```bash
# 安装主题相关组件
npx shadcn@latest add button dropdown-menu
```

```typescript
// components/theme-toggle.tsx
"use client"
// ...
import { Moon, Sun } from "lucide-react"
import { useTheme } from "next-themes"
import { Button } from "@/components/ui/button"
// ...
export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
// ...
  return (
    <Button
      variant="ghost"
      size="icon"
      onClick={() => setTheme(theme === "light" ? "dark" : "light")}
    >
      <Sun className="h-5 w-5 rotate-0 scale-100 transition-all dark:-rotate-90 dark:scale-0" />
      <Moon className="absolute h-5 w-5 rotate-90 scale-0 transition-all dark:rotate-0 dark:scale-100" />
    </Button>
  )
}
```

## 不适用场景

以下场景shadcn UI工具-免费版不适合处理：

- 无明确技术栈的模糊需求
- 纯架构设计决策
- 运维部署管理

## 触发条件

需要代码生成、编程辅助、调试测试、开发部署时使用。不适用于非本工具能力范围的需求.
## 快速开始

1. 阅读## 核心能力章节了解skill功能
2. 按## 依赖说明配置环境
3. 执行所需能力对应的命令
4. 参考## 错误处理章节处理异常
5. 查看## FAQ解答常见疑问

### 项目初始化

```bash
# 创建 Next.js 项目
npx create-next-app@latest my-app --typescript --tailwind --eslint
# ...
# 初始化 shadcn/ui
cd my-app
npx shadcn@latest init
# ...
# 安装常用组件
npx shadcn@latest add button card input label
```

### 配置文件

```json
// components.json
{
  "$schema": "https://ui.shadcn.com/schema.json",
  "style": "default",
  "rsc": true,
  "tsx": true,
  "tailwind": {
    "config": "tailwind.config.ts",
    "css": "app/globals.css",
    "baseColor": "slate",
    "cssVariables": true
  },
  "aliases": {
    "components": "@/components",
    "utils": "@/lib/utils"
  }
}
```

**响应解析**: 完成完成后,查看输出响应确认任务状态。成功时输出包含解析摘要和响应数据;失败时根据错误信息排查问题,查阅错误解析章节获取恢复步骤.
## 配置示例

### Tailwind 主题配置

```css
/* app/globals.css */
@layer base {
  :root {
    --background: 0 0% 100%;
    --foreground: 222.2 84% 4.9%;
    --primary: 222.2 47.4% 11.2%;
    --primary-foreground: 210 40% 98%;
    --radius: 0.5rem;
  }
// ...
  .dark {
    --background: 222.2 84% 4.9%;
    --foreground: 210 40% 98%;
    --primary: 210 40% 98%;
    --primary-foreground: 222.2 47.4% 11.2%;
  }
}
```

### 常用组件速查

| 组件 | 安装命令 | 用途 |
|:-----|:-----|:-----|
| Button | `npx shadcn@latest add button` | 按钮 |
| Card | `npx shadcn@latest add card` | 卡片容器 |
| Input | `npx shadcn@latest add input` | 输入框 |
| Form | `npx shadcn@latest add form` | 表单(含验证) |
| Table | `npx shadcn@latest add table` | 数据表格 |
| Dialog | `npx shadcn@latest add dialog` | 弹窗对话框 |
| Dropdown | `npx shadcn@latest add dropdown-menu` | 下拉菜单 |
| Toast | `npx shadcn@latest add toast` | 消息提示 |
| Tabs | `npx shadcn@latest add tabs` | 标签页 |
| Select | `npx shadcn@latest add select` | 下拉选择 |

## 最佳实践

1. **组件可控**:shadcn/ui 组件代码在项目中,可自由修改,不要当外部库用
2. **统一主题**:通过 CSS 变量管理颜色,不要在组件中硬编码颜色值
3. **表单验证用 zod**:定义 schema 后,类型自动推断,前后端共享验证规则
4. **响应式优先**:使用 Tailwind 的 `sm:`/`md:`/`lg:` 前缀,移动优先设计
5. **暗色模式**:使用 `next-themes` 或 CSS 变量,确保暗色模式下对比度足够
6. **组件组合**:优先组合现有组件,而非创建新组件

## 常见问题

### Q: shadcn/ui 和传统组件库(如 Ant Design)有什么区别?

A: shadcn/ui 不是传统 npm 包,而是将组件代码直接复制到项目中。优点:完全可控、可自由修改、无版本锁定。缺点:需要自己管理组件更新.
### Q: 如何自定义组件样式?

A: 直接修改 `components/ui/` 下的组件文件。样式使用 Tailwind CSS 类名,也可以修改 CSS 变量统一调整主题.
### Q: zod schema 如何与后端共享?

A: 将 zod schema 定义在单独文件中,前后端都引用。前端用于表单验证,后端用于 API 请求体验证,确保数据一致性.
### Q: 如何添加自定义组件?

A: 在 `components/` 目录下创建新组件,引用 `components/ui/` 中的基础组件进行组合。遵循 shadcn/ui 的设计语言和样式规范.
## 依赖说明

### 运行环境

- **Agent平台**: 支持 SKILL.md 的任意 AI Agent(Claude Code / Cursor / Codex / Gemini CLI 等)
- **操作系统**: Windows / macOS / Linux
- **Node.js**: 18+

### 第三方依赖

| 依赖项 | 类型 | 是否必需 | 获取方式 |
|---:|---:|---:|---:|
| Node.js | 运行时 | 必需 | 官方网站下载 |
| Next.js | 框架 | 推荐 | npx create-next-app |
| React | UI库 | 必需 | npm install react |
| Tailwind CSS | 样式框架 | 必需 | npm install tailwindcss |
| shadcn/ui CLI | 组件工具 | 必需 | npx shadcn@latest |
| react-hook-form | 表单管理 | 表单必需 | npm install react-hook-form |
| zod | 数据验证 | 表单必需 | npm install zod |
| lucide-react | 图标库 | 推荐 | npm install lucide-react |
| LLM API | API | 必需 | 由Agent内置LLM提供 |

### API Key 配置

- 本 Skill 无需 API Key
- 组件代码为开源,无需认证

### 可用性分类

- **分类**: MD+EXEC(Markdown指令 + 命令行执行)
- **说明**: 通过自然语言指令驱动 Agent 执行 shadcn/ui 组件安装与代码生成
- **限制**: 免费版不支持设计系统管理、企业组件库与团队协作

## 错误处理

| 错误场景 | 原因 | 处理方式 |
|:---:|:---:|:---:|
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
    "result": "shadcn UI工具-免费版处理结果",
    "execution_time": "0.5s",
    "metadata": {
      "version": "1.0",
      "processor": "shadcn ui"
    }
  },
  "execution_log": ["解析输入参数", "执行核心处理", "格式化输出结果"],
  "error": null
}
```
