# UnifyPort Node.js SDK Skill（简体中文）

[English](SKILL.md) | [简体中文](SKILL.zh-CN.md)

本文档是 canonical `SKILL.md` 的简体中文说明，不是独立的可执行 skill 入口。

## 适用场景

当任务涉及以下任一内容时使用本 skill：

- 在 Node.js 或 TypeScript 中调用 UnifyPort Device API；
- 新增、更新或排查 `@unifyport/sdk-node` operation；
- 更新公开契约、修复生成漂移或审查公开类型；
- 调整认证、timeout、retry、pagination、错误或 JavaScript 整数边界。

这是一个开发与集成 skill。安装它不会把 Device API operation 暴露成 OpenClaw tools，也不会安装
MCP Server 或提供任何凭据。

开始前先选择一种模式：

- **项目使用**：在应用中安装或使用公开的 `@unifyport/sdk-node` package；
- **仓库维护**：修改 SDK 仓库、公开契约、生成代码或测试。

只有在 SDK 仓库内处理 MCP 专属行为时，才同时使用仓库本地的 `unifyport-mcp` skill。该 MCP
skill 不属于 ClawHub 发布边界。

## 所有任务的准备步骤

1. 确认当前任务属于项目使用还是仓库维护。
2. 安装或调整依赖前，先检查目标项目及其现有 package manager。
3. 从已安装类型或公开文档确认真实 package exports 与 operation 名称。
4. 不要求用户粘贴、打印或持久化真实 API key。实时请求所需凭据只能由用户或部署系统通过运行环境提供。

## 项目使用流程

1. 确认 Node.js `>=22.12.0`。
2. 沿用目标项目已有的 package manager 安装 SDK。使用 npm 时执行：

   ```bash
   npm install @unifyport/sdk-node
   ```

3. 从 package 根入口导入 `UnifyPortDeviceClient` 和公开类型。
4. 从运行环境读取 base URL 和 API key，不得把它们写入源码、生成文件、日志、tool input 或提交的配置。
5. 使用类型化 operation 方法，不手拼 path、query string 或认证 header。
6. 集成后运行目标项目已有的测试和类型检查。

最小配置：

```ts
import { UnifyPortDeviceClient } from "@unifyport/sdk-node";

function requiredEnv(name: string): string {
  const value = process.env[name];
  if (!value) throw new Error(`Missing required environment variable: ${name}`);
  return value;
}

const device = new UnifyPortDeviceClient({
  baseUrl: requiredEnv("UNIFYPORT_DEVICE_API_BASE_URL"),
  apiKey: requiredEnv("UNIFYPORT_DEVICE_API_KEY")
});
```

不要仅为验证安装而执行实时请求。除非用户明确要求实时调用并提供获批的测试环境，否则优先使用类型检查和
mock transport 测试。

## 仓库维护准备

仅当 workspace 同时存在 SDK 仓库标记 `AGENTS.md`、`contracts/device.openapi.yaml`，且根
`package.json` 对应 `unifyport-sdk-node-workspace` 时，才执行本节步骤。

1. 阅读仓库根 `AGENTS.md`。
2. 阅读 `docs/zh-CN/architecture.md`、`docs/zh-CN/security.md`；涉及 API 变化时再读 `docs/zh-CN/contract-maintenance.md`。
3. 用 `rg` 确认实际 operationId、客户端导出和现有测试，不猜测 API 名称。
4. 检查工作区状态，保留用户及其他代理已有改动。
5. 确认协议变化有经批准的公开 API schema 与 release notes。

## 公开契约与范围

代码生成只接受一份仓库内契约：

- Device API：`contracts/device.openapi.yaml`。

契约更新只能依据经批准的公开 API schema 与 release notes。公开资料没有定义的字段、状态码、认证或安全规则不能靠推测加入 SDK。

契约中的 `/v1/accounts/...` 是 Device API 内的 provider 账号资源；账号管理、授权和运行态 operation 仍属于 SDK 范围，不应与独立认证服务混淆。

## 选择客户端

- 使用 `UnifyPortDeviceClient` 调用 Device API。配置类型是 `DeviceClientConfig`，认证为 `X-Api-Key`。

不要把 API key 或 base URL 作为普通 operation 参数。provider 账号授权所需的 password、code 或 session payload 只能通过对应的类型化 operation 传入，并按敏感输入处理。

## 共用规则

### 使用现有 operation

1. 从 package 根入口导入客户端和类型。
2. 使用类型化 operation 方法，不手拼 path 或 header。
3. 捕获 SDK 的公开错误类型，只记录 status、服务端 code 与 request ID；不要记录完整请求、响应或 config。
4. 需要遍历 cursor 时优先使用已提供的 pagination helper；否则显式设置上限并处理重复 cursor。
5. 不把 `uint64` 风格 ID 转成 `number`，除非契约明确保证安全范围。

### 在 SDK 仓库中新增或变更 API

1. 审查经批准的公开 API schema 与 release notes。
2. 更新 `contracts/device.openapi.yaml`。
3. 执行 `pnpm contracts:lint`。
4. 为 operation 明确填写 auth、side effect、retry、secret、destructive 与 MCP policy。
5. 执行 `pnpm generate`，审查 generated diff；不要直接修改 generated 文件。
6. 添加边界测试并执行 `pnpm generate:check` 与 `pnpm check`。
7. 执行 `pnpm public:check`，确认公开内容与发布边界。

## 安全决策

- 自动重试采用显式 allowlist。普通写操作、验证码/密码/session 提交和一次性 secret operation 默认不重试。
- 认证 header 由 client 注入，operation 级 header 不得覆盖。
- 默认 HTTPS；loopback HTTP 仅在调用方明确 opt in 时允许。
- API key create/rotate secret 只交给直接 SDK 调用方，不缓存、不记录、不发送到 MCP。
- webhook 签名协议必须由经批准的公开 API schema 与 release notes 完整定义，不能猜测。
- 错误解析要兼容空 body、非 JSON 和非标准 envelope，并保留 HTTP status；原始 cause 可能含敏感 URL 或请求值，不能直接公开。

## 修改标准

- 默认最小 diff，不做无关重构。
- 代码注释使用简短中文解释 why、兼容边界或风险；行为变化时同步更新注释。
- operation path 和 types 来自生成，不复制一套手写类型。
- 新的 convenience API 不能掩盖重要 wire 语义，例如 `204` 或一次性 secret。
- 公开 API 变化需要判断 semver 影响，并验证 ESM exports 与声明文件。
- 面向公开用户的文档发生变化时，在同一次变更中同步更新完整的简体中文对应版本。

## 验证与交付

完整验证：

```bash
pnpm clawhub:check
pnpm check
pnpm public:check
```

按需单独运行：

```bash
pnpm contracts:lint
pnpm generate:check
pnpm lint
pnpm format:check
pnpm test
pnpm typecheck
pnpm build
pnpm package:check
```

交付时先说明结果，再列出采用的公开 API schema/release notes、修改文件、认证/重试/MCP 分类变化、实际执行命令及未覆盖风险。不要声称未执行的命令已通过。
