# SEVO Web 驾驶舱使用文档

OpenClaw（dev-02 子Agent）| 2026-04-29

## 1. 这是什么

SEVO Web 驾驶舱是一个基于 Next.js 14 的前端控制台，面向 FR（需求 / 功能请求）运营、审批和交付跟踪。它把仪表盘、FR 列表、待办队列、门禁审批、澄清回复、交付物索引、交付账本、跨项目统计这些内容放到同一个 Web 界面里，方便直接做状态判断和操作闭环。

当前代码结构显示，这个 Web 端已经具备完整的页面骨架、API 路由和交互路径；数据层目前主要通过 `web/lib/engine-service.ts` 提供 mock / stub 数据。

## 2. 项目位置

- Web 根目录：`projects/sevo/web/`
- 文档产出：`projects/sevo/docs/web-dashboard-guide.md`

## 3. 依赖安装

### 3.1 package.json 中的运行依赖

来自 `web/package.json`：

- `next` `^14.2.0`
- `react` `^18.3.0`
- `react-dom` `^18.3.0`
- `swr` `^2.4.1`
- `recharts` `^3.8.1`
- `lucide-react` `^1.8.0`
- `@radix-ui/react-slot` `^1.2.4`
- `@radix-ui/react-tabs` `^1.1.13`
- `class-variance-authority` `^0.7.1`
- `clsx` `^2.1.1`
- `tailwind-merge` `^3.5.0`
- `tailwindcss` `^3.4.19`
- `tailwindcss-animate` `^1.0.7`
- `postcss` `^8.5.10`
- `autoprefixer` `^10.5.0`
- `@tailwindcss/postcss` `^4.2.2`

### 3.2 开发依赖

- `typescript` `^5.7.0`
- `@types/node` `^22.0.0`
- `@types/react` `^18.3.0`
- `@types/react-dom` `^18.3.0`

### 3.3 安装方式

仓库里已经存在 `package-lock.json`，默认按 npm 使用：

```bash
cd projects/sevo/web
npm install
```

如果只是查看已有代码结构，不需要安装；如果是新环境首次启动，先安装依赖再运行脚本。

## 4. 启动方式

来自 `web/package.json` 的 scripts：

```json
{
  "dev": "next dev",
  "build": "next build",
  "start": "next start",
  "typecheck": "tsc --noEmit"
}
```

常用命令：

```bash
cd projects/sevo/web
npm run dev
```

用于本地开发。

```bash
cd projects/sevo/web
npm run typecheck
```

用于只做 TypeScript 检查。

```bash
cd projects/sevo/web
npm run build
npm run start
```

用于生产构建和启动。

## 5. 访问路径与基础配置

### 5.1 basePath

`web/next.config.mjs` 中配置了：

```js
const nextConfig = {
  basePath: '/sevo',
};
```

这意味着：

- 应用不是挂在站点根路径，而是挂在 `/sevo`
- 页面访问入口是 `/sevo/...`
- API 请求也都走 `/sevo/api/...`
- `web/lib/api-client.ts` 里把 `BP` 固定成了 `"/sevo"`

如果反向代理、Nginx、子路径部署没配对，这个项目最容易出的问题就是页面能开、接口 404，或者登录后跳转路径不对。

### 5.2 环境变量

`web/.env.example` 里目前只有一个变量：

```env
AUTH_PASSWORD=
```

这个变量用于登录认证。

如果不配置：

- `POST /api/auth/login` 会直接返回 401
- 用户无法正常登录

建议本地运行时至少配置：

```env
AUTH_PASSWORD=你自己的访问密码
```

### 5.3 会话与 Cookie

从 `web/app/api/auth/login/route.ts`、`logout/route.ts`、`middleware.ts` 可见：

- Cookie 名：`sevo_session`
- 会话 token：随机 UUID
- Cookie 路径：`/sevo`
- `sameSite: "lax"`
- `httpOnly: true`
- 当前代码里 `secure: false`
- 有效期：7 天

### 5.4 中间件逻辑

`web/middleware.ts` 的逻辑很直接：

- 放行 `/login`
- 放行 `/api/auth/*`
- 放行 `/_next` 和 `favicon`
- 其他路径都检查 `sevo_session` Cookie
- 中间件只做“Cookie 是否存在且像 UUID”这类轻校验
- 真正的会话有效性校验要靠服务端 `/api/auth/verify`

这套设计的意思是：

- 用户未登录时，会被重定向到 `/login`
- 前端所有仪表盘页都默认受保护
- Edge Runtime 不直接读 Node 侧 session store，所以中间件只做快速拦截

## 6. 页面结构总览

### 6.1 根布局

- `web/app/layout.tsx`：全局 HTML 外壳，加载 `globals.css`
- `web/app/page.tsx`：根路径直接 `redirect("/dashboard")`
- `web/app/(dashboard)/layout.tsx`：用 `AppShell` 包裹所有后台页面

### 6.2 登录页

路径：`/sevo/login`

文件：`web/app/(auth)/login/page.tsx`

作用：

- 输入访问密码
- 调用 `api/auth/login`
- 登录成功后跳转 `/dashboard`
- 登录失败显示错误信息

页面左侧还写了三类入口价值：

- 看清整条 FR 管线
- 审批前先看上下文
- 失败和阻塞会被集中暴露

### 6.3 驾驶舱主导航

`web/components/app-shell.tsx` 定义了左侧导航，主要页面如下：

- `/dashboard` 仪表盘
- `/todos` 待办队列
- `/todos?type=gate` 门禁审批
- `/todos?type=clarification` 澄清问题
- `/frs` FR 列表
- `/projects` 项目
- `/deliverables` 交付物
- `/analytics` 统计分析
- `/ledger` 交付账本
- `/notifications` 通知中心
- `/search` 全局搜索

顶部还有一个全局搜索框，支持跨 Projects、FR、交付物、通知、账本检索。

## 7. 页面功能概览

下面按 `web/app/(dashboard)/` 的路由结构说明。

### 7.1 仪表盘 `/dashboard`

文件：`web/app/(dashboard)/dashboard/page.tsx`

首页职责：

- 展示总 FR 数、健康度、推进中数量、阻塞中数量
- 展示宏阶段分布
- 用图表展示阶段占比和数量
- 给出当前运营判断

核心感受是“先看风险，再看分布”。如果系统里有失败项或阻塞项，这一页会优先把问题顶出来。

### 7.2 待办队列 `/todos`

文件：`web/app/(dashboard)/todos/page.tsx`

这里聚合三类待处理事项：

- 门禁审批
- 待回复澄清
- 失败项

支持筛选、分页，并把下一步动作直接写在卡片上。

### 7.3 FR 列表 `/frs`

文件：`web/app/(dashboard)/frs/page.tsx`

作用：

- 以列表方式展示所有 FR
- 支持按宏阶段筛选
- 突出失败项、当前阶段、最近更新时间
- 点击进入 FR 详情页

### 7.4 FR 详情 `/frs/[id]`

文件：`web/app/(dashboard)/frs/[id]/page.tsx`

作用：

- 展示单个 FR 的总体状态
- 展示当前宏阶段和当前阶段
- 展示阶段时间线、风险状态、已完成 / 待开始阶段
- 支持操作：`pause`、`resume`、`cancel`、`retry`、`abandon`

这是一个“读状态 + 发动作”的核心页面。

### 7.5 FR 质量页 `/frs/[id]/quality`

从路由结构可见已存在该页面入口，对应质量视图接口：

- 页面：`web/app/(dashboard)/frs/[id]/quality/page.tsx`
- API：`/api/v1/frs/[id]/quality`

适合看单个 FR 的质量结论和问题分布。

### 7.6 FR 时间线页 `/frs/[id]/timeline`

对应：

- 页面：`web/app/(dashboard)/frs/[id]/timeline/page.tsx`
- API：`/api/v1/frs/[id]/timeline`

用于看阶段推进记录。

### 7.7 FR 全景页 `/frs/[id]/panorama`

对应：

- 页面：`web/app/(dashboard)/frs/[id]/panorama/page.tsx`

用于补充更完整的 FR 上下文视图。

### 7.8 项目页 `/projects`

文件：`web/app/(dashboard)/projects/page.tsx`

作用：

- 按项目维度查看状态
- 显示每个项目的 FR 数量、完成数、进行中、失败数
- 显示项目完成比例
- 点击进入项目 FR 矩阵

### 7.9 项目 FR 矩阵 `/projects/[id]/fr-matrix`

文件：`web/app/(dashboard)/projects/[id]/fr-matrix/page.tsx`

作用：

- 以矩阵形式展示 FR 在各宏阶段的状态
- 支持按状态筛选
- 适合快速看某个项目的全局推进面

### 7.10 门禁审批详情 `/gates/[id]`

文件：`web/app/(dashboard)/gates/[id]/page.tsx`

作用：

- 查看 blocker
- 查看审查包
- 对门禁做 `approve`、`reject`、`request-review`

页面的产品表达很明确：先看 blocker，再点通过，不鼓励盲批。

### 7.11 澄清详情 `/clarifications/[id]`

文件：`web/app/(dashboard)/clarifications/[id]/page.tsx`

作用：

- 查看问题正文和上下文
- 查看历史回复
- 提交新的澄清回复
- 推动当前阶段继续前进

### 7.12 交付物列表 `/deliverables`

文件：`web/app/(dashboard)/deliverables/page.tsx`

作用：

- 按交付物类型、阶段、FR 关键词筛选
- 展示文档 / 代码 / 报告 / 制品
- 显示路径、阶段、来源 FR
- 对可预览内容直接展示 preview

### 7.13 交付物详情 `/deliverables/[id]`

文件：`web/app/(dashboard)/deliverables/[id]/page.tsx`

作用：

- 查看单个交付物的元数据
- 查看来源 FR 和文件路径
- 查看可预览内容
- 快速跳回对应 FR

### 7.14 统计分析 `/analytics`

文件：`web/app/(dashboard)/analytics/page.tsx`

作用：

- 看跨项目统计
- 看平均交付周期
- 看门禁一次通过率
- 看阶段失败热区
- 看不同执行者效率

当前文案里已经明确写出：MVP 先用 demo 数据跑通阅读路径。

### 7.15 交付账本 `/ledger`

文件：`web/app/(dashboard)/ledger/page.tsx`

作用：

- 以时间倒序查看账本记录
- 支持按 FR、操作类型、结果筛选
- 看摘要、结论、证据链引用

### 7.16 账本详情 `/ledger/[id]`

文件：`web/app/(dashboard)/ledger/[id]/page.tsx`

作用：

- 查看单条账本记录
- 查看操作类型、结果、阶段
- 查看证据链列表
- 跳回对应 FR

### 7.17 通知中心 `/notifications`

文件：`web/app/(dashboard)/notifications/page.tsx`

作用：

- 展示信息 / 提醒 / 关键通知
- 每条通知带下一步动作入口
- 支持按严重级别筛选

### 7.18 通知详情 `/notifications/[id]`

从路由结构可见存在详情页：

- 页面：`web/app/(dashboard)/notifications/[id]/page.tsx`

适合接通知详情、标记已读或上下文扩展。

### 7.19 全局搜索 `/search`

文件：`web/app/(dashboard)/search/page.tsx`

会同时搜索：

- Projects
- FR
- 交付物
- 通知
- 账本

当前实现是前端聚合多个数据源后做检索。

## 8. API 路由概览

`web/app/api/` 下已经整理出比较完整的接口层。

### 8.1 认证接口

- `POST /api/auth/login`
- `POST /api/auth/logout`
- `GET /api/auth/verify`

### 8.2 仪表盘与分析

- `GET /api/v1/dashboard/summary`
- `GET /api/v1/analytics`

### 8.3 FR 相关

- `GET /api/v1/frs`
- `GET /api/v1/frs/[id]`
- `POST /api/v1/frs/[id]/pause`
- `POST /api/v1/frs/[id]/resume`
- `POST /api/v1/frs/[id]/cancel`
- `POST /api/v1/frs/[id]/retry`
- `POST /api/v1/frs/[id]/abandon`
- `GET /api/v1/frs/[id]/quality`
- `GET /api/v1/frs/[id]/timeline`
- `GET /api/v1/frs/[id]/artifacts`

### 8.4 门禁与澄清

- `GET /api/v1/gates/[id]`
- `POST /api/v1/gates/[id]/approve`
- `POST /api/v1/gates/[id]/reject`
- `POST /api/v1/gates/[id]/request-review`
- `GET /api/v1/clarifications/[id]`
- `POST /api/v1/clarifications/[id]/reply`

### 8.5 其他索引接口

- `GET /api/v1/projects`
- `GET /api/v1/projects/[projectId]/fr-matrix`
- `GET /api/v1/deliverables`
- `GET /api/v1/notifications`
- `GET /api/v1/notifications/[id]`
- `POST /api/v1/notifications/[id]/read`
- `GET /api/v1/ledger`
- `GET /api/v1/todos`
- `GET /api/v1/notification-preferences`
- `GET /api/v1/notification-preferences/[id]`

### 8.6 实时事件接口

- `GET /api/v1/events/stream`

`web/app/api/v1/events/stream/route.ts` 使用 SSE（Server-Sent Events）推送实时事件，当前逻辑包括：

- 建立连接时发送 `connected`
- 每 30 秒 heartbeat
- 示例性地每 60 秒推送一个 mock `fr.updated` 事件

如果后面要把驾驶舱做成真正的实时面板，这个接口就是连接点。

## 9. 组件说明

### 9.1 布局组件

#### `components/app-shell.tsx`

整个后台的壳层组件，负责：

- 左侧导航
- 顶部栏
- 全局搜索框
- 移动端侧边栏开合
- 退出登录
- 页面内容承载

这是驾驶舱最关键的骨架组件。

#### `components/Pagination.tsx` 与 `components/ui/pagination.tsx`

从目录看同时存在分页组件，页面里主要使用的是 `components/ui/pagination.tsx`。分页能力已经被 FR 列表、待办、通知、项目、账本等页面复用。

### 9.2 UI 基础组件

`web/components/ui/` 下主要组件：

- `badge.tsx`：标签
- `button.tsx`：按钮
- `card.tsx`：卡片容器
- `input.tsx`：输入框
- `select.tsx`：下拉选择
- `tabs.tsx`：页签切换
- `skeleton.tsx`：骨架屏

### 9.3 业务展示组件

- `page-header.tsx`：页面标题区
- `page-states.tsx`：空状态、错误状态、加载态、重试动作
- `stat-card.tsx`：统计卡片
- `health-gauge.tsx`：健康度仪表

这些组件共同支撑了驾驶舱的“卡片化 + 状态化”界面风格。

## 10. 数据层说明

### 10.1 `web/lib/api-client.ts`

这是前端数据访问入口，特点：

- 基于 `swr`
- 所有请求统一加上 basePath `/sevo`
- 提供一组 `useXxx` hooks
- 不同页面有不同的自动刷新间隔

例如：

- 仪表盘：30s 刷新
- FR 列表：15s 刷新
- FR 详情：10s 刷新
- 待办：10s 刷新
- 项目 / 交付物 / 通知 / 账本：15s 左右刷新

同时它也封装了动作请求：

- `frAction(...)`
- `gateAction(...)`
- `clarificationReply(...)`

### 10.2 `web/lib/engine-service.ts`

这是当前最需要知道的一点：

- 这个文件不是正式后端服务接入层
- 当前注释明确写着：`Stub engine service — placeholder that returns mock data`
- 里面内置了大量 mock pipeline、notification、ledger 等数据

所以现阶段 Web 驾驶舱更接近“前端交互成形 + 领域模型成形 + 假数据驱动演示”，不等于已经接上真实 SEVO 引擎。

### 10.3 `web/lib/session-store.ts`

作用：

- 在单进程内存里保存登录会话 token
- 提供 `addSession / hasSession / removeSession / clearAllSessions`

这意味着：

- 会话目前是内存态，不是持久化存储
- 进程重启后，已有登录态会失效
- 多实例部署时，这种实现不够用

### 10.4 `web/lib/api-helpers.ts`

提供：

- 标准错误响应
- 命令体解析
- 分页参数解析
- traceId 生成

这部分主要服务 API 层统一返回格式。

## 11. 使用流程建议

### 11.1 第一次打开

1. 准备 `AUTH_PASSWORD`
2. 启动 Web 服务
3. 打开 `/sevo/login`
4. 输入密码进入驾驶舱

### 11.2 日常查看顺序

建议按这个顺序看：

1. 先看 `/dashboard`
2. 再看 `/todos`
3. 有失败项时进 `/frs`
4. 要跨项目判断时进 `/projects` 或 `/analytics`
5. 要追溯证据时进 `/deliverables` 和 `/ledger`

### 11.3 操作闭环入口

- 批门禁：`/gates/[id]`
- 回澄清：`/clarifications/[id]`
- 控 FR：`/frs/[id]`
- 查结果：`/deliverables`、`/ledger`

## 12. 当前实现边界

从已读代码看，当前版本有几个边界要先心里有数：

### 12.1 数据主要是 mock

`engine-service.ts` 里已经写明是 stub / placeholder，所以：

- 页面交互可以跑通
- 统计、FR、通知、项目数据能展示
- 但默认不是实时真实生产数据

### 12.2 会话是单进程内存态

- 重启后登录态会失效
- 不适合多实例共享

### 12.3 登录 Cookie 还没按生产环境收紧

当前 `secure: false`，如果后面上 HTTPS 正式环境，应该进一步调整。

### 12.4 子路径部署依赖很强

因为配置了 `/sevo` basePath，所以代理层、静态资源、API 前缀都必须跟着保持一致。

## 13. 排查重点

如果页面不能正常使用，优先看这几项：

### 13.1 登录后仍跳回登录页

先查：

- `AUTH_PASSWORD` 是否配置
- Cookie 是否成功写入 `sevo_session`
- 访问路径是不是 `/sevo/...`
- 代理层是否把 Cookie 路径弄乱了

### 13.2 页面能开但接口报错

先查：

- 是否正确走 `/sevo/api/...`
- basePath 是否和部署路径一致
- `engine-service` 或 API route 是否返回了错误

### 13.3 刷新后登录态丢失

这通常不是前端 bug，先想到：

- 进程是否重启过
- 当前 session store 是不是内存态

### 13.4 实时事件没动静

先查：

- `/api/v1/events/stream` 是否能建立 SSE 连接
- 浏览器或代理是否拦截了长连接
- 当前是否只是 mock 事件，没有接到真实引擎

## 14. 一句话总结

这套 SEVO Web 驾驶舱已经把“登录 → 总览 → 待办 → FR → 审批 / 澄清 / 交付物 / 账本 / 分析”这条阅读和操作路径搭出来了。前端结构完整，接口骨架完整，数据层现在仍以 stub 为主。要把它变成真正可用的运营驾驶舱，下一步重点不是补页面，而是把 `engine-service` 背后的真实数据源和持久化会话接上。