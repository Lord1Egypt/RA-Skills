---
name: unkey-cli
description: 使用 Unkey CLI 在终端中管理 API namespaces、keys、identities、permissions、rate limits 和 analytics 查询。当用户提到 unkey 命令、API key 管理、限流、RBAC 权限、身份分组或 key 验证排查时触发。Use this skill for Unkey CLI operations and troubleshooting.
metadata:
  openclaw:
    requires:
      bins: ["bash", "unkey", "jq"]
user-invocable: true
argument-hint: "可选参数：resource, action, flags, output(json), root_key_source"
---

# Unkey CLI Skill

使用 Unkey 官方 CLI 在终端执行管理操作，不要臆造命令输出。

> 注意：CLI 处于 early 阶段，命令和输出格式可能变化；底层 Unkey API 是稳定版本化的。

## 何时使用

以下场景应触发本技能：
- 创建、查询、删除 API namespace
- 创建、校验、更新、删除 API keys
- 管理 identities（按用户/团队分组 key）
- 管理 permissions / roles（RBAC）
- 配置或排查 ratelimit
- 查询 key verification analytics（SQL）
- 用户明确要求使用 `unkey` 命令行

## 文档发现规则

在扩展命令细节（参数、边界行为）前，先读取文档索引：
- `https://unkey.com/docs/llms.txt`

再根据索引进入对应 CLI 子页面（如 `docs/cli/keys/create-key.md`）。

## 安装检查与安装

先检查是否已安装：

```bash
unkey --help
```

若未安装，优先提示以下方式之一：

```bash
npm install -g unkey
```

或从 GitHub Releases 下载对应平台二进制。

## 鉴权与密钥来源优先级

执行命令前确认 root key 来源，优先级如下：
1. 命令参数 `--root-key`
2. 环境变量 `UNKEY_ROOT_KEY`
3. 本地配置 `~/.unkey/config.toml`（来自 `unkey auth login`）

首次登录命令：

```bash
unkey auth login
```

如果三者都没有，停止执行并提示用户提供 root key 或先登录。

## 标准命令形态

所有 API 操作遵循：

```bash
unkey api <resource> <action> [flags]
```

### Resources

- `apis`: API namespace 的创建、查询、删除、列 key
- `keys`: key 创建/校验/更新/删除、权限与角色绑定
- `identities`: identity 创建/查询/更新/删除
- `permissions`: permission 与 role 管理
- `ratelimit`: 限流检查与 override 管理
- `analytics`: SQL 查询 key verification 数据

## 常用命令示例

```bash
# 创建 API namespace
unkey api apis create-api --name=payment-service-prod

# 创建 key
unkey api keys create-key --api-id=api_1234abcd --name='Production Key' --enabled

# 校验 key
unkey api keys verify-key --key=sk_1234abcdef

# 单标识限流检查
unkey api ratelimit limit --namespace=api.requests --identifier=user_123 --limit=100 --duration=60000

# analytics 查询
unkey api analytics get-verifications --query="SELECT COUNT(*) as total FROM key_verifications_v1 WHERE outcome = 'VALID' AND time >= now() - INTERVAL 7 DAY"

# 创建 permission 并绑定到 key
unkey api permissions create-permission --name=documents.read --slug=documents-read
unkey api keys add-permissions --key-id=key_1234abcd --permissions=documents.read,documents.write
```

## 输出与脚本模式

默认输出通常包含：
- 请求 ID 和耗时（例如 `req_xxx (took 45ms)`）
- 返回数据对象

用于脚本时，强制使用 JSON：

```bash
unkey api apis create-api --name=my-api --output=json | jq '.data.id'
```

## 全局参数

所有命令都可使用：
- `--root-key`: 覆盖 root key
- `--api-url`: 覆盖 API 地址（默认 `https://api.unkey.com`）
- `--config`: 指定配置文件路径（默认 `~/.unkey/config.toml`）
- `--output`: 输出格式（脚本场景建议 `json`）

## 帮助与自检

优先使用内置帮助确定 flags：

```bash
unkey --help
unkey api --help
unkey api keys --help
unkey api keys create-key --help
```

## 执行准则

- 在未确认鉴权来源前，不执行会修改资源的命令。
- 对删除类命令（二次不可逆）先提醒用户确认再执行。
- 不回显完整 root key；如需展示命令，脱敏处理密钥。
- 不伪造执行结果；失败时返回原始错误并给出下一步修复建议。

## 失败处理

常见失败与建议：
- `authentication missing/forbidden`: 检查 `UNKEY_ROOT_KEY`、`--root-key`、`unkey auth login`
- `api_not_found` 或 `key_not_found`: 核对 `api-id`/`key-id` 是否属于当前 workspace
- `workspace_rate_limited`: 加退避重试并减少高频调用
- `invalid_analytics_query`: 修复 SQL 语法，仅允许 `SELECT`

## 建议回复格式

```markdown
# Unkey CLI 执行结果
- command: <实际执行命令（脱敏后）>
- auth_source: <flag | env | config>
- output_mode: <default | json>

## Result
<关键输出/对象>

## Next Step
<一个可执行的后续动作>
```
