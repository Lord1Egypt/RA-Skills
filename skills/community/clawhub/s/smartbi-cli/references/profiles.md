# 多环境（Profile）规范

本文件为 **SmartBI CLI Skill** 的附属参考；流程性 MUST 以上级 `SKILL.md` 为准。

**用途**：环境（profile）的确定、配置与错误处理。普通业务用户只感知连接的 SmartBI 地址或业务名称；`dev`、`--profile`、默认 profile 等是内部细节，不进入用户视野。

## 核心原则

1. **隐藏内部配置**：任务开始时确定连接，普通业务对话不单独展示 profile 名
2. **连接所需信息**：复用已有配置；缺少时仅补地址和有效令牌，内部名称自动确定
3. **执行零分支**：所有 `smartbi` 命令一律带 `--profile <name>`
4. **不动默认环境**：新增环境不带 `--set-default`；用户明确要求切换默认时用 `smartbi profile set-default <name>`
5. **向后兼容**：用户未指定环境时走默认环境，行为与单环境时代一致

## 环境确定

任务开始时，按以下顺序确定环境：

1. 扫描对话识别环境/客户关键词（环境名、`prod`/`qa`/`dev` 等后缀、客户名），与 config.yaml 的 `profiles` 键匹配
2. 唯一匹配 → 使用该环境
3. 多个匹配 → 用服务器地址或用户熟悉的业务名称让用户选择，不要求识别 profile 名
4. 无匹配且用户提供了新连接的地址/令牌 → 走「连接配置流程」新建
5. 未指定任何环境信息 → 默认环境（config.yaml 的 `profile:` 字段）

确定后直接继续原业务请求；仅在连接切换会影响结果或排错时，说明所用服务器地址或业务名称。用户中途明确“切到 Y”时按上述流程重新确定，不展示内部 profile 名。

## 执行规则

- 环境确定后，所有 `smartbi` 命令（`list`/`search`/`describe`/`call`/`doc`）**一律带 `--profile <name>`**

## 连接配置流程（首次与新增统一）

触发：首次使用（无配置文件）、用户要求配置新环境、指定的环境不存在。

只对缺失的连接信息按顺序提问（一次一个）：

1. **地址**：提供 SmartBI 地址 → `serverType: smartbi`；只说要连接 SmartBI 但未指定地址时，先确认是否使用官网体验中心 `https://cloud.smartbi.com.cn/smartbi`；确认后使用 `serverType: smartbi`。拒绝体验中心或无法提供地址时，再询问 SDK Server 地址 → `serverType: sdk-server`；均无法提供 → 暂停。已有有效配置时跳过此步骤。
2. **令牌**：问令牌时一并说明获取路径和存储方式（仅一句）："请提供 SmartBI 个人访问令牌（登录 SmartBI 后，在「个人中心 → 我的设置 → 个人访问令牌」中新建）。令牌默认直接存进配置；如对安全有更高要求，也可以改用「环境变量」或「系统钥匙串」存储。"

首次配置省略 `--profile`，让 CLI 使用默认名。新增连接时，先从用户已给的业务名称生成合法且不冲突的内部名；没有名称则读取现有 profile 后按 `connection-2`、`connection-3` 等顺序选取首个未占用名。不得覆盖已有 profile，也不为内部名称单独打断用户。

写入方式：

| 场景 | 命令 | `profile:` 默认环境 |
|------|------|-------------------|
| 首次（无配置文件） | `smartbi init --server-type <sdk-server\|smartbi> --base-url <地址> --token <令牌> [--profile <环境名>]`（不指定 `--profile` 时默认 `dev`） | CLI 自动设为该环境 |
| 新增 | `smartbi profile add <name> --server-type <sdk-server\|smartbi> --base-url <地址> --token <令牌>` | 不动（用户明确要求成为默认时执行 `smartbi profile set-default <name>`，无需重建） |

完成后继续原业务请求；需要告知连接状态时说“已连接到所选 SmartBI 地址”，不展示内部名称。存储方式的说明已含于令牌问询话术内，写入后不要重复询问。

## 错误处理

| 错误 | 处理 |
|------|------|
| `PROFILE_NOT_FOUND` | `smartbi profile list` 读取现有连接；按地址或业务名称让用户选择，或走「连接配置流程」新建，不要求用户识别内部 profile 名 |
| `AUTH_FAILED` | 提示"`<name>` 环境的 token 无效或已过期"；执行 `smartbi profile show <name>` 查看凭证来源（env/keyring/字面量）与可用性，请用户确认该环境凭证 |
| 其他 | 按 SKILL.md Phase 4 通用诊断，报告本次调用所用环境 |

## 版本约束

- **版本要求**：CLI ≥ **2.0.0**（profile 命令族与 init/profile add 写盘的最低版本）。安装后验证：`smartbi --version` ≥ 2.0.0，或 `smartbi profile list --help` 可用；低于 2.0.0 时按 `references/init.md`「标准安装」升级
- **命名规则**：profile 名仅允许 `[A-Za-z0-9_-]`；"环境 × 客户"维度通过命名约定 `<客户>-<环境>` 承载（如 `customerA-test`），不强制
