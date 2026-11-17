# REA-CN 安装与自更新指引

> 本指南面向国内网络环境，全部走 `npmmirror` 镜像，避免 npm 官方源慢/失败。
> 所有操作仅使用 Node 内置能力与 npm；REA 安装**不会**自动安装/升级 Ghidra、IDA、JADX 等 provider（需你自备）。
> 这些外部二进制的**下载地址、体积、平台、安装步骤与配置键**见 `references/providers.md`（全装齐约 2GB+，建议按目标类型选装）。

## 0. 前置要求

- **Node.js**：引擎要求 `^22.19.0 || ^24.11.0 || >=26.0.0`。建议用本机已装 Node 22/24，或用 WorkBuddy 管理的运行时。
- **包管理器**：npm（本技能脚本已对国内镜像做适配）。

## 1. 安装 rea-agents（首次）

方式一 · 用内置安装脚本（推荐，走镜像，装进 engine/）：
```bash
cd <本技能目录>
node scripts/cn-installer.mjs            # 把 6.4.0 的依赖装进 engine/node_modules
node scripts/cn-installer.mjs --dry-run # 只打印命令不执行
node scripts/cn-installer.mjs --check   # 仅检查依赖是否已就绪
```
> `cn-installer.mjs` 采用「干净临时目录安装 → 复制到 engine/」的稳健路径，
> 规避了直接对 engine 跑 `npm install` 时 npm 偶发的 `edgesOut` bug（已实测 143 包约 15s）。

方式二 · 直接 npm（国内镜像，仅当你想用独立 `rea` CLI）：
```bash
npm install -g rea-agents@6.4.0 --registry=https://registry.npmmirror.com --no-audit --no-fund
```

方式三 · 临时使用（免安装）：
```bash
npx -y rea-agents@6.4.0          # 等价于 `rea` CLI
```

> **注意**：方式一安装的是「让 `engine/` 这个随包副本能运行」的**依赖**，不是再装一份 rea-agents。
> MCP 服务器实际从本技能的 `engine/` 启动（见第 3 节），版本与文档严格一致（6.4.0）。

## 2. 自更新引擎基线（engine/）

技能内 `engine/` 是一份离线基线副本。需要升级时：
```bash
node scripts/rea-selfupdate.mjs            # 更新到 config 默认版本
node scripts/rea-selfupdate.mjs 6.4.0     # 指定版本
node scripts/rea-selfupdate.mjs --dry-run # 预览步骤
```
自更新器会：① 临时安装目标版本 → ② 把 `dist/skills/bridge/native/LICENSE/package.json` 同步进 `engine/` → ③ 校验 `engine/package.json` 版本。
**不会**覆盖 `references/`、`scripts/`、`config/`、`SKILL.md`、`SKILL.en.md`（本地化成果安全）。

## 3. 挂载为 MCP 服务器（路线 A）

1. 在支持 MCP 的客户端（如 WorkBuddy）中添加服务器，启动命令指向本技能的 **单一入口**：
   ```json
   {
     "mcpServers": {
       "rea-cn": {
         "command": "node",
         "args": ["<技能目录绝对路径>/scripts/run-mcp.mjs"]
       }
     }
   }
   ```
   （完整可直接复制的示例见仓库内 `mcp.config.example.json`。）
2. `run-mcp.mjs` 会先**自动检查并安装依赖**（缺失时走 npmmirror 装进 `engine/node_modules`，即"智能体自动查缺补漏"），随后以 stdio 启动 REA MCP 服务器。
3. 客户端加载 `SKILL.md`（中文）与本地化文档；LLM 读取 `glossary-zh-en.md` 理解语义。
4. LLM 调用工具时**逐字使用英文原名**（见 `tool-invocation-contract.md`）。

## 3.1 默认瘦身包 vs 离线打包（依赖是否进包？）

- **默认（推荐）：瘦身包，约 10MB，`engine/` 内不含 `node_modules`。**
  首次经 `run-mcp.mjs` 启动时会自动联网安装依赖（约 15s），**用户无需手动操作**。
- **可选离线包**：若需**无网/内网**部署，先跑一次：
  ```bash
  node scripts/vendor-offline.mjs
  ```
  它会把约 91MB 依赖固化进 `engine/node_modules`，之后无论有无网络都能直接运行。
- **为什么不默认把依赖塞进包**：
  ① 会让技能包体积膨胀约 10 倍；② `node-pty` 等原生模块与平台绑定（Windows 构建无法在 macOS/Linux 运行），而自动安装会按当前平台拉取正确原生二进制；③ 依赖会随上游补丁过时，自动安装总取到当前版本。
  因此**默认瘦身 + 首次自动安装**是最稳的选择；离线场景用 `vendor-offline.mjs` 显式固化即可。

## 4. 直接用 CLI（路线 B）

```bash
rea open <本地路径>                 # 打开二进制/归档/APK
rea inspect-evidence-bundle --help  # 查看证据包命令
```
未安装 `rea` 时用 `npx -y rea-agents@6.4.0` 代替。

## 5. 环境/provider 探测

```bash
node scripts/route.mjs
```
该脚本会报告 Node 版本、engine 是否存在、rea CLI 是否在 PATH、provider 相关环境变量，并给出接入建议。

## 6. 常见安装问题

- **npm 报错 `Cannot read properties of null (reading 'edgesOut')`**：npm 10.x 已知偶发 bug。解决：在**空目录**（无 package.json）中安装，或用 `npm install --no-package-lock`；本技能 `cn-installer.mjs` 已在干净临时目录模式下规避。
- **镜像不通**：检查 `config/cn-config.json` 中 `npmRegistry`，可换 `https://registry.npmmirror.com` 或公司内网镜像。
- **provider 不可用**：属正常（需自备 Ghidra 等）；下载与安装方法见 `references/providers.md`，并用 `binary_session`（入参 `{}`）查看 `tool_availability`。
