# UCloud CLI 用法

## 规范模式

本技能的核心执行路径是官方 CLI 的产品子命令：

- 产品子命令风格：`ucloud uhost describe --region cn-bj2`
- 产品子命令风格：`ucloud eip list --region cn-bj2`

`ucloud api` 是产品子命令不可用、能力不足或语义不明确时的兜底路径：

- Inline flag 风格：`ucloud api --Action DescribeULB --ULBId ulb-xxxx`
- JSON 文件风格：`ucloud api --local-file ./request.json`

围绕这三种模式设计本技能：

1. 先查产品子命令 help，优先使用 `ucloud <product> <subcommand>` 执行查询、创建、更新或删除操作。
2. 当产品子命令不存在、缺少必要参数能力，或 payload 较大、嵌套层级深且产品命令无法表达时，回退到 `ucloud api --local-file`。
3. 回退到 API 时，保持 `Action` 和参数名称与官方 OpenAPI 文档一致。
4. 每次回退到 `ucloud api` 调用前，先在 `https://github.com/UCloudDoc-Team/api` 中找到对应接口，然后基于该文档构建 payload。
5. 如果 CLI help 或文档无法明确给出正确的产品命令、Action、必填字段或范围信息，在臆测之前先查阅 `references/doc-sources.md`。

## 凭据约定

官方 CLI 将 profile 存储在 `~/.ucloud/config.json` 和 `~/.ucloud/credential.json` 中。
将 profile 作为本技能的主要凭据来源。

CLI 提供 `ucloud auth login`、`ucloud init`、`ucloud config add`、`ucloud config update` 和 `ucloud config list`。优先使用 OAuth 登录处理交互式人工授权；AK/SK 初始化和配置变更是敏感操作，因为 `config add/update` 的 flag 包含 public key 和 private key。

Profile 选择规则：

- 如果用户明确指定了 profile，使用 `--profile <name>` 调用 CLI。
- 如果用户没有指定 profile，使用本地激活的 CLI 配置。
- 如果没有可用的激活配置，优先询问用户是否使用 OAuth 授权；用户同意后运行 `ucloud auth login`，无浏览器环境运行 `ucloud auth login --no-browser`。

将 shell 命令、注释文字和工具调用 payload 视为可能被暴露的内容。
不要将 `UCLOUD_PUBLIC_KEY` 或 `UCLOUD_PRIVATE_KEY` 直接放入命令字符串、CLI flag、日志、计划或面向用户的摘要中。
优先复用已有 profile，而非在命令行中收集凭据。

初始化规则：

- 缺少 profile 时，优先提示 OAuth 授权。用户同意后直接运行 `ucloud auth login`；无浏览器或 SSH 环境使用 `ucloud auth login --no-browser`。
- OAuth 适合交互式人工使用。脚本、CI/CD 或用户明确要求 AK/SK 时，再引导 `ucloud init` 或 `ucloud config add`。
- 需要展示非交互式 AK/SK 配置方式时，只展示带占位符的 `ucloud config add` 模板，不代入真实密钥。
- 需要查看 profile 时，可以使用 `ucloud config list` 或 `ucloud --config`，但输出按敏感内容处理；只汇报 profile 名称、active 状态和非敏感默认范围，遮盖任何 key。
- 修改已有 profile 前先确认 profile 名称。单次操作优先使用 `--profile <name>`，不要为了方便切换 active profile。
- 只有用户明确要求更改默认 profile 时，才使用 `ucloud config update --profile <name> --active true`。
- OAuth 登录、初始化或更新后，先执行只读命令验证 profile 可用，再继续资源操作。

## 调用行为

使用产品子命令作为自动化默认执行路径。

- 当用户明确指定 profile 名称时，使用 `--profile <name>`。
- 否则依赖本地激活的 profile。
- 对于产品子命令无法表达的复杂或嵌套请求，将请求 payload 保存在 JSON 文件中，并通过 `ucloud api --local-file` 执行。

如果需要调试输出，为该次调用设置 `UCLOUD_CLI_DEBUG=on`。

## Payload 文件约定

1. 将 JSON payload 写入临时文件（如 `/tmp/ucloud-request.json`）。
2. 执行 `ucloud api --local-file /tmp/ucloud-request.json`。
3. 调用完成后删除临时文件。

示例：

```bash
cat > /tmp/ucloud-request.json << 'EOF'
{
  "Action": "CreateUHostInstance",
  "Region": "cn-bj2",
  "Zone": "cn-bj2-05",
  "ImageId": "uimage-xxx",
  "LoginMode": "Password",
  "Password": "GENERATED_PASSWORD"
}
EOF
ucloud --profile prod-account api --local-file /tmp/ucloud-request.json
rm -f /tmp/ucloud-request.json
```

## 参数处理

- 产品子命令可用时，将用户输入映射为明确的 CLI flag。
- 回退到 `ucloud api` 时，将请求 payload 保持为 JSON 对象。
- 仅在字段缺失且当前上下文中有可用默认值时，才注入 `ProjectId`、`Region` 和 `Zone`。
- 产品命令 flag 使用本地 help 和 CLI 文档中的名称；API payload 保持与 UCloud OpenAPI 完全一致的官方字段名。
- `ucloud <product> <subcommand> --help` 是选择默认执行路径的首要依据。除非产品命令不存在、能力不足或语义不明确，否则不要默认回退到 `ucloud api --local-file`。

## 密码生成

使用 shell 工具生成字母数字密码：

```bash
tr -dc 'A-Za-z0-9' </dev/urandom | head -c 16
```

通过修改 `-c` 参数调整长度。

## 操作指南

- 从只读产品查询命令开始进行发现；没有合适命令时再使用只读 Action。
- 对于变更类操作，先检查目标资源，确保标识精确。
- 将原始 API 响应保持为 JSON 格式，以便后续解析和摘要。
- 产品相关的创建默认值、部署资源选择和产品专属约束见 [`product-rules.md`](./product-rules.md)。
