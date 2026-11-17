# `init` / 安装与配置参考

本文件为 **SmartBI CLI Skill** 的附属参考；流程性 MUST 以上级 `SKILL.md` 为准。

**用途**：仅当 skill 的惰性预检（lazy preflight）触发时，用于完成标准安装、初始化与最小可用配置。

## 安装与配置边界（MUST，禁止自由发挥）

- **唯一允许的获取方式**：使用下方 **标准安装** 中的命令，通过 **npm** 全局安装 `**@smartbi/cli@latest`**，得到可在 PATH 中调用的 `smartbi`。
- **最低版本要求**：`smartbi` 版本 MUST >= `2.0.0`（profile 命令族与 init/profile add 写盘的最低版本）。安装后必须执行 `smartbi --version` 验证版本。若版本低于 2.0.0，必须重新执行 `npm install -g @smartbi/cli@latest` 升级。
- MUST NOT 使用 `yarn` / `pnpm` / `bun` / `npx` 等替代上述 **npm 全局安装** 作为本 skill 的默认安装路径（避免版本漂移与不可审计环境）。
- MUST NOT 调用项目目录内随意脚本、其它产品 CLI、或路径/名称相近的可执行文件冒充 `smartbi`。
- **配置文件唯一来源**：安装并执行 `smartbi init` 后，使用默认路径 `**~/.smartbi/config.yaml`**（或你明确使用且与 init 产物一致的 `--config` 路径）。MUST NOT 从全盘、用户主目录或其它产品中“找一个长得像的配置文件”复制或 `--config` 指向。

## CLI 不存在时（MUST 先于一切）

若执行 `smartbi` 时系统/shell 明确提示 **命令不存在**（例如 `command not found`、`'smartbi' 不是内部或外部命令`、`is not recognized as an internal or external command`、`ENOENT`、退出码 **127** 等），说明 **SmartBI CLI 尚未安装、未加入 PATH，或会话中途被卸载/破坏**。

此时 MUST：

1. **不要**继续在 skill 流程里尝试 `list`/`search`/`describe`/`call` 或猜测接口；不要换目录“盲找”可执行文件；不要用 `curl`/HTTP 等替代 CLI。
2. **直接**按下方 **标准安装** 在终端**实际执行**安装命令，然后执行 `smartbi --version` 验证。
3. 验证通过后按下方 **重装后恢复顺序** 处理 init 与配置，再回到业务 Phase。

## 重装后恢复顺序（MUST）

在 `**npm install -g @smartbi/cli@latest` 且 `smartbi --version` 已成功** 之后，按顺序执行；不得口述“已安装”、不得跳过 `--version`。

1. **检查默认配置是否存在且可读**：`~/.smartbi/config.yaml`（或用户此前声明的 `--config` 路径）。
2. **若文件不存在**：按 **生成配置文件** 与 **缺项时固定提问模板** 补齐配置。文件存在但解析失败时按具体错误处理，不能因“不确定”而覆盖配置。
3. **若已有可读配置**：复用所选环境和已知信息，无需用户再次确认配置仍可信。用原任务所需的最小只读命令继续验证；失败按原因处理：鉴权错误只处理凭证，网络错误检查连通性，权限错误核对权限，不回退全量 init。`--dry-run`只能验证本地请求构造，不能证明服务器可达或令牌有效。
4. 仅当满足 **Phase 0 退出标准** 后，才恢复 `list`/`search`/`describe`/`call` 等业务命令。

## 标准安装

```bash
npm install -g @smartbi/cli@latest
smartbi --version
```

要求：

- `smartbi` 版本 MUST >= `2.0.0`
- Node.js `>=18`
- 默认配置文件：`~/.smartbi/config.yaml`

## 生成配置文件

分「首次配置」与「新增连接」两条路径。只补问缺失的地址或令牌；内部 profile 名不向普通业务用户提问。环境确定、执行规则与错误处理见 `references/profiles.md`。

### 首次配置（无配置文件时）

1. 按「缺项时固定提问模板」只收集缺失的连接信息（一次一个问题）。
2. 执行 `smartbi init --server-type <sdk-server|smartbi> --base-url <地址> --token <令牌> [--profile <环境名>]`（不指定 `--profile` 时默认 `dev`）。默认字面量存储；若用户选择「环境变量」→ 改用 `--token-env <VAR>`（提醒用户该环境变量后续需保持可用）；「系统钥匙串」→ 使用当前 shell 的安全 stdin 管道传入令牌并带 `--token-keyring --token-stdin`，不要把字面令牌写进命令历史（裸 `--token-keyring` 会失败并提示补值方式）。
3. CLI 原子写盘 `~/.smartbi/config.yaml`（该环境同时为默认环境）。stderr 的 "prefer tokenEnv or keyring" 提示属正常输出。
4. 不向用户展示配置文件路径、内部 profile 名或内容；配置成功后继续原业务请求。需要区分多个连接时按 `references/profiles.md` 用服务器地址或业务名称说明。

存储方式的说明已含于「缺项时固定提问模板」第二步的令牌问询话术内，写入后不要再重复询问。

### 新增环境（已有配置文件时）

1. 按「缺项时固定提问模板」只收集缺失的连接信息（一次一个问题）。
2. 执行 `smartbi profile add <name> --server-type <sdk-server|smartbi> --base-url <地址> --token <令牌>`（默认环境保持不变）。用户选择「环境变量」→ 以 `--token-env <VAR>` 替代 `--token`（提醒该环境变量后续需保持可用）；「系统钥匙串」→ 使用当前 shell 的安全 stdin 管道传入令牌并带 `--token-keyring --token-stdin`，不要把字面令牌写进命令历史。
3. 需要新环境成为默认时——先经用户确认，再执行 `smartbi profile set-default <name>`。
4. 写入后继续原业务请求；需要告知连接状态时说“已连接到所选 SmartBI 地址”，不展示内部 profile 名或配置内容。存储方式的说明已含于令牌问询话术（「缺项时固定提问模板」第二步），写入后不要再重复询问。

### 修复已有环境

缺少地址才询问地址；地址已知而令牌不可用时仅补凭证。配置了tokenEnv或tokenKeyring不等于缺少令牌，先检查对应来源可用性，不打印凭证。环境变量缺失时恢复该变量，不擅自改为字面量存储。更新已有环境按当前CLI契约使用profile操作，保留其他环境和默认选择，不使用`init --force`。`profile add --force`会替换所选profile，不能假设它只更新令牌；执行前核对需要保留的地址、服务器类型及其他设置，不可静默丢失自定义配置。

### 配置字段说明

- **`baseUrl`**：SmartBI 或 SDK Server 的根 URL。用户提供 SmartBI 地址（如 `http://127.0.0.1:8080/smartbi`）→ `serverType: smartbi`；用户提供 SDK Server 地址（如 `http://127.0.0.1:8086`）→ `serverType: sdk-server`。
- **`token`**：SmartBI 个人访问令牌（登录 SmartBI 后，在「个人中心 → 我的设置 → 个人访问令牌」中新建）。token 存储三选一（schema 互斥，只能配其一）：`token` 字面量（默认）/ `tokenEnv`（环境变量名）/ `tokenKeyring: true`（系统钥匙串，service=smartbi-cli、account=profile 名）。
- **`serverType`**：只能为 `sdk-server` 或 `smartbi` 两个值之一，不得使用其他大小写或命名变体（如 `smartbi-server`、`sdk_server` 等）。

约束：
- 不得臆造配置值；缺失时必须先向用户提问并等待补齐。
- 用自然语言提问，不要暴露 `baseUrlEnv` / `tokenEnv` 等配置键名；如需提及更安全的存储方式，用「环境变量 / 系统钥匙串」的口语表述（存储说明见「缺项时固定提问模板」第二步）。
- 写入后不向普通业务用户展示配置文件路径或内部 profile 名；直接继续原业务请求。
- **内部 profile 名**：首次配置省略 `--profile`，由 CLI 使用默认值；新增连接按 `references/profiles.md` 在内部生成不冲突的名称，不为此单独提问。

### 缺项时固定提问模板（MUST）

当所选环境缺少必要连接信息时，只补问尚未确认的项目；已知项跳过。凭证来源不可用按上方“修复已有环境”处理。**一次只问一个问题**，以下模板按实际缺项选择，不要求每次从第一步重新开始：

**第一步——先问地址：**

```text
继续执行前需要配置服务器连接。是否连接 SmartBI 官网体验中心 https://cloud.smartbi.com.cn/smartbi？如果要连接自己的环境，请提供 SmartBI 地址。
```

- 用户提供地址 → `serverType` 直接设为 `smartbi`（无需检测 URL 格式），写入 `baseUrl`
- 无现成地址、用户只说连接 SmartBI 时第一问就按上方话术提供体验中心选项；确认后使用 `https://cloud.smartbi.com.cn/smartbi`，`serverType` 设为 `smartbi`。已有地址或配置时不重复推荐；确认前不写入配置或发起连接。
- 用户明确说"没有 SmartBI 地址"、"不知道"、"无法提供" → 使用以下**精确话术**回复：
  "了解。也可以使用 SDK Server 地址代替（如 http://127.0.0.1:8086）。请问有 SDK Server 地址吗？"
  - 用户提供 SDK Server 地址 → `serverType` 设为 `sdk-server`
  - 用户仍无法提供 → 暂停，等待用户找到地址后再继续
- 高级用户可直接说 `sdkserver: http://xxx` → `serverType` 直接设为 `sdk-server`，跳过上述流程
- 两项都拿到后，按上方「生成配置文件」流程在后台生成配置，不向用户展示配置细节

**第二步——再问令牌：**

```text
已记录服务器地址。请提供 SmartBI 个人访问令牌（登录 SmartBI 后，在「个人中心 → 我的设置 → 个人访问令牌」中新建）。令牌默认直接存进配置；如对安全有更高要求，也可以改用「环境变量」或「系统钥匙串」存储。
```

在你补齐前，我会先暂停，不会继续调用 `smartbi` 命令。

**内部命名（不向普通业务用户提问）：** 首次配置省略 `--profile`；CLI 的默认 profile 名为 `dev`，仅用于命令和配置。用户明确要求新增连接时，按 `references/profiles.md` 从已提供的业务名称或连接顺序生成不冲突的内部名称。客户无需理解或设置该名称。

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
    # 可选替代（三选一，勿与 token 并存）：
    # tokenEnv: SMARTBI_TOKEN_DEV
    # tokenKeyring: true
registry:
  source: remote
  checkIntervalSeconds: 300
```

## Phase 0 退出标准

- `smartbi --version` 可执行；
- 所选profile的地址与服务器类型已确定，且所选凭证来源（token/tokenEnv/tokenKeyring之一）可用；不要求环境变量或钥匙串模式另配字面token。
- 配置可用于后续 `list/search/describe/call`。
