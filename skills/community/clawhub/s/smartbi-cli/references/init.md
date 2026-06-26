# `init` / 安装与配置参考

本文件为 **Smartbi CLI Skill** 的附属参考；流程性 MUST 以上级 `SKILL.md` 为准。

**用途**：仅当 skill 的惰性预检（lazy preflight）触发时，用于完成标准安装、初始化与最小可用配置。

## 安装与配置边界（MUST，禁止自由发挥）

- **唯一允许的获取方式**：使用下方 **标准安装** 中的命令，通过 **npm** 全局安装 `**@smartbi/cli@latest`**，得到可在 PATH 中调用的 `smartbi`。
- **最低版本要求**：`smartbi` 版本 MUST >= `1.1.0`（`--tmpl` 占位符模板的最低版本）。安装后必须执行 `smartbi --version` 验证版本。若版本低于 1.1.0，必须重新执行 `npm install -g @smartbi/cli@latest` 升级。
- MUST NOT 使用 `yarn` / `pnpm` / `bun` / `npx` 等替代上述 **npm 全局安装** 作为本 skill 的默认安装路径（避免版本漂移与不可审计环境）。
- MUST NOT 调用项目目录内随意脚本、其它产品 CLI、或路径/名称相近的可执行文件冒充 `smartbi`。
- **配置文件唯一来源**：安装并执行 `smartbi init` 后，使用默认路径 `**~/.smartbi/config.yaml`**（或你明确使用且与 init 产物一致的 `--config` 路径）。MUST NOT 从全盘、用户主目录或其它产品中“找一个长得像的配置文件”复制或 `--config` 指向。

## CLI 不存在时（MUST 先于一切）

若执行 `smartbi` 时系统/shell 明确提示 **命令不存在**（例如 `command not found`、`'smartbi' 不是内部或外部命令`、`is not recognized as an internal or external command`、`ENOENT`、退出码 **127** 等），说明 **Smartbi CLI 尚未安装、未加入 PATH，或会话中途被卸载/破坏**。

此时 MUST：

1. **不要**继续在 skill 流程里尝试 `list`/`search`/`describe`/`call` 或猜测接口；不要换目录“盲找”可执行文件；不要用 `curl`/HTTP 等替代 CLI。
2. **直接**按下方 **标准安装** 在终端**实际执行**安装命令，然后执行 `smartbi --version` 验证。
3. 验证通过后按下方 **重装后恢复顺序** 处理 init 与配置，再回到业务 Phase。

## 重装后恢复顺序（MUST）

在 `**npm install -g @smartbi/cli@latest` 且 `smartbi --version` 已成功** 之后，按顺序执行；不得口述“已安装”、不得跳过 `--version`。

1. **检查默认配置是否存在且可读**：`~/.smartbi/config.yaml`（或用户此前声明的 `--config` 路径）。
2. **若文件不存在、明显损坏、或不确定是否仍有效**：直接按 **生成配置文件** 与 **缺项时固定提问模板** 补齐配置。
3. **若用户明确确认配置文件未被删除且仍可信**：可先不重复 `smartbi init`，但必须用一次最小只读命令（例如带 `--dry-run` 若 CLI 支持，否则 `smartbi list --agent` 在配置已齐的前提下）验证 CLI 与配置可用；**一旦失败**，回到步骤 2 全量 init + 补齐流程。
4. 仅当满足 **Phase 0 退出标准** 后，才恢复 `list`/`search`/`describe`/`call` 等业务命令。

## 标准安装

```bash
npm install -g @smartbi/cli@latest
smartbi --version
```

要求：

- `smartbi` 版本 MUST >= `1.1.0`
- Node.js `>=18`
- 默认配置文件：`~/.smartbi/config.yaml`

## 生成配置文件

当用户已提供 `baseUrl` 和 `token`，需要生成 `~/.smartbi/config.yaml` 时，按以下流程（用户无感知中间过程）：

### 步骤 1：获取占位符模板

执行 `smartbi init --tmpl`，将 stdout 内容读取到内存（MUST NOT 展示模板内容给用户）：

### 步骤 2：替换占位符

模板使用 `{{PLACEHOLDER}}` 语法，做以下精确字符串替换：

| 占位符 | 替换为 |
|--------|--------|
| `{{SERVER_TYPE}}` | `smartbi` 或 `sdk-server` |
| `{{BASE_URL}}` | 用户提供的地址 |
| `{{TOKEN}}` | 用户提供的令牌 |

约束：
- MUST 精确匹配占位符文本（含双花括号），不做模糊搜索。
- 仅替换上述三个占位符，不修改 `timeoutMs`、`registry` 等其他配置。

### 步骤 3：写入文件

将替换后的内容写入 `~/.smartbi/config.yaml`（父目录不存在时创建）。写入后告知用户"配置已写入 `~/.smartbi/config.yaml`"，不展示文件内容。

### 配置字段说明

- **`baseUrl`**：Smartbi 或 SDK Server 的根 URL。用户提供 Smartbi 地址（如 `http://127.0.0.1:8080/smartbi`）→ `serverType: smartbi`；用户提供 SDK Server 地址（如 `http://127.0.0.1:8086`）→ `serverType: sdk-server`。
- **`token`**：Smartbi 个人令牌（可登录 Smartbi，在个人中心申请）。
- **`serverType`**：只能为 `sdk-server` 或 `smartbi` 两个值之一，不得使用其他变体（如 `Smartbi`、`smartbi-server`、`sdk_server` 等）。

约束：
- 不得臆造配置值；缺失时必须先向用户提问并等待补齐。
- 用自然语言提问，不要暴露 `baseUrlEnv` / `tokenEnv` 等内部技术术语。
- 写入后仅告知用户"配置已写入 `~/.smartbi/config.yaml`"。MUST NOT 向用户建议改为环境变量方式。

### 缺项时固定提问模板（MUST）

当检测到 `baseUrl` / `token` 任一必要项缺失时，必须先向用户提问，禁止继续执行业务命令。**一次只问一个问题**，按以下顺序：

**第一步——先问地址：**

```text
继续执行前需要配置服务器连接。请提供您的 Smartbi 地址（如 http://127.0.0.1:8080/smartbi）。
```

- 用户提供地址 → `serverType` 直接设为 `smartbi`（无需检测 URL 格式），写入 `baseUrl`
- 用户明确说"没有 Smartbi 地址"、"不知道"、"无法提供" → 使用以下**精确话术**回复：
  "了解。也可以使用 SDK Server 地址代替（如 http://127.0.0.1:8086）。请问有 SDK Server 地址吗？"
  - 用户提供 SDK Server 地址 → `serverType` 设为 `sdk-server`
  - 用户仍无法提供 → 暂停，等待用户找到地址后再继续
- 高级用户可直接说 `sdkserver: http://xxx` → `serverType` 直接设为 `sdk-server`，跳过上述流程
- 两项都拿到后，按上方「生成配置文件」流程在后台生成并写入 `~/.smartbi/config.yaml`，告知用户"配置已写入"

**第二步——再问令牌：**

```text
已记录服务器地址。请提供 Smartbi 个人令牌（可登录 Smartbi，在个人中心申请）。
```

在你补齐前，我会先暂停，不会继续调用 smartbi 命令。

## 最小可用配置（示例）

```yaml
profile: dev
profiles:
  dev:
    serverType: sdk-server
    baseUrl: "http://127.0.0.1:8086"
    token: "your-api-token"
    allowPlainToken: true
    timeoutMs: 300000
registry:
  source: remote
  checkIntervalSeconds: 300
```

## Phase 0 退出标准

- `smartbi --version` 可执行；
- YAML 中已为 profile 配置了 **`baseUrl`**、**`token`** 和 **`serverType`**，且 `serverType` 正确匹配用户服务器类型。
- 配置可用于后续 `list/search/describe/call`。

