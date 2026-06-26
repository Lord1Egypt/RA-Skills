---
name: ucloud-cli
description: 当用户需要通过官方 UCloud CLI 进行真实 UCloud 资源操作时使用，包括查看、创建、更新或删除云主机、网络、EIP、负载均衡器和数据库。当用户想要在 UCloud 上部署 WEB 应用或将服务上线时也使用此技能，即使用户描述的是部署任务而非明确指定云产品。
---

# UCloud CLI

通过官方 `ucloud` CLI 操作 UCloud 资源。当用户需要对 UCloud 账号执行实际云操作、资源检查或参数化自动化任务时，优先使用产品子命令；只有产品子命令不存在、能力不足或语义不明确时，才回退到 `ucloud api` 调用 OpenAPI。

将部署类请求视为该技能的强触发信号。如果用户说想要部署 WEB 程序、发布站点、将服务上线、准备云主机、开放公网访问、绑定 EIP、创建负载均衡器，或为应用配置其他 UCloud 资源，即使请求以应用部署而非原始云 API 调用的方式表述，也要使用此技能。

## 前置条件

- 执行环境中需要安装 `ucloud` CLI，且版本不低于 `v0.3.1`。
- 执行资源操作前，需要存在可用的 CLI profile；如果没有可用 profile，按“CLI 初始化与 profile 发现”流程优先使用 OAuth 授权初始化。

如果 `ucloud` CLI 未安装、不可用或版本低于 `v0.3.1`，先停止当前资源操作；检查操作系统和架构，再征得用户同意后安装或升级 CLI。
Linux 优先读取 `/etc/os-release` 并结合 `uname -m`，macOS 使用 `sw_vers` 和 `uname -m`。

**安装方法**
- macOS：按架构从 `https://ucloud-infra.cn-bj.ufileos.com/cli/darwin_{amd64,arm64}/ucloud` 下载二进制文件，在用户未指定安装路径的情况下，必须安装到 `$PATH` 中的目录，如果没有权限申请用户授权。
- Linux：按架构从 `https://ucloud-infra.cn-bj.ufileos.com/cli/linux_{amd64,arm64}/ucloud` 下载二进制文件，在用户未指定安装路径的情况下，必须安装到 `$PATH` 中的目录，如果没有权限申请用户授权。
- Windows：从 `https://ucloud-infra.cn-bj.ufileos.com/cli/windows_amd64/ucloud.exe` 下载二进制文件，在用户未指定安装路径的情况下，必须安装到 `PATH` 中的目录，如果没有权限申请用户授权。

## CLI 初始化与 profile 发现

1. 先确认 CLI 是否可用：`ucloud --version` 或 `ucloud --help`。
2. 如果用户未指定 profile，优先使用本地激活 profile；需要检查本地配置时，使用 `ucloud config list` 或 `ucloud --config`，并把输出视为敏感内容。
3. 如果检查输出包含 public key、private key、token 或其他凭据，只在内部用于判断配置是否存在；面向用户展示时必须遮盖或省略。
4. 如果没有 profile，优先使用 OAuth 授权。用户同意后直接运行 `ucloud auth login`，支持交互或非交互环境。
5. 对于脚本、CI/CD 或用户明确要求 AK/SK profile 的场景，再引导 `ucloud init` 或 `ucloud config add`。
6. 如果用户明确要求非交互式创建 AK/SK profile，只提供带占位符的命令模板，不代入真实密钥，也不执行包含真实密钥的命令：

```bash
ucloud config add \
  --profile example-profile \
  --public-key YOUR_PUBLIC_KEY \
  --private-key YOUR_PRIVATE_KEY \
  --region cn-bj2 \
  --zone cn-bj2-02 \
  --project-id org-xxxxxx \
  --active true \
  --agree-upload-log false
```

7. AK/SK 初始化需要的字段：profile 名称、public key、private key；可选默认值包括 Region、Zone、ProjectId、BaseUrl、timeout、max retry 和是否设为 active。
8. 修改已有 profile 时，先确认目标 profile 名称，避免覆盖用户当前激活配置。能通过 `--profile <name>` 精确调用时，不要为了单次操作切换 active profile。
9. 只有用户明确要求更改默认配置时，才使用 `ucloud config update --profile <name> ... --active true`。如果 CLI 要求同时提供密钥才能 update，仍然只给用户占位符模板，不在命令中嵌入真实密钥。
10. 初始化或 OAuth 授权完成后，先执行只读检查，例如 `ucloud region`、`ucloud project list` 或等价只读命令，确认 profile 可用，再继续资源操作。

## 信息来源优先级

在决定如何调用 CLI 时，按以下顺序使用信息来源：

1. 本地 CLI help 输出和 UCloud CLI 文档，用于确认产品子命令、flag、profile 用法和已安装命令的覆盖范围。
2. UCloud 产品文档，用于确认产品概念、资源关系、约束和用户术语。
3. 如 CLI 中未支持相应产品子命令，或产品子命令无法覆盖当前操作，使用 `ucloud api` 子命令进行泛化调用；从 `https://github.com/UCloudDoc-Team/api` 中获取对应产品的文档，确认 Action 名称、必填参数、请求结构和响应字段后再发送请求。
4. 如果当前上下文无法提供足够信息来确定正确的产品命令、Action、必填字段或资源范围，请在询问用户或执行请求之前先查阅官方文档。
5. `ucloud-cli` 仓库，当前述文档和本地 help 仍不足时使用。

## 产品规则

当需要识别产品别名、决定部署资源、创建资源默认值或处理产品专属约束时，先阅读 [`references/product-rules.md`](./references/product-rules.md)，再按索引读取对应产品文件。正文只保留通用 CLI、profile、安全和输出规则。

## 调用流程

1. 将用户请求优先转换为产品专用命令，例如 `ucloud uhost ...`、`ucloud eip ...` 或 `ucloud ulb ...`。
2. 先查本地 `ucloud --help`、`ucloud <product> --help`、`ucloud <product> <subcommand> --help` 和 CLI 文档，确认产品子命令是否覆盖当前任务、需要哪些 flag，以及是否需要 `ProjectId`、`Region` 或 `Zone`。
3. 只有产品子命令不存在、缺少必要能力或行为不明确时，才将请求转换为原始 OpenAPI Action，如 `DescribeULB`；如果将通过 `ucloud api` 执行请求，先在 `https://github.com/UCloudDoc-Team/api` 中找到对应接口。
4. 确认使用的 CLI profile：
   - 如果用户指定了 profile，显式使用该 profile
   - 否则使用本地激活的 profile
5. 检查目标资源标识和所选产品命令或 API Action 相关的必填字段是否齐全。
6. 如果 CLI 没有可用的激活 profile 且用户也没有指定 profile，则停止并请用户先初始化或配置一个 profile。
7. 如果存在必须补充的信息，向用户提出简洁的跟进问题，仅列出缺失的字段。
8. 将用户回复中的值解析为结构化数据，合并到产品命令 flag 或 API JSON payload 中。
9. 仅在所选命令或 API 需要且用户或环境提供时，才添加 `ProjectId`、`Region` 或 `Zone`。
10. 如果产品子命令可用，执行对应 `ucloud <product> <subcommand>`；如果必须回退到 API，将 JSON payload 写入临时文件，然后执行 `ucloud api --local-file <file>`。
11. 在执行后续变更类操作之前，先审查查询结果或响应内容。

## 调用方式选择

默认使用产品专用 CLI 子命令，因为它们更贴近用户意图、参数语义更清晰，也更符合官方 CLI 的高层操作入口，如果用户没有指定 profile，省略 `--profile` 让 CLI 使用本地激活配置。
只有当产品子命令不存在、缺少必要能力、无法表达嵌套 payload，或本地 help 与产品语义无法确认正确调用方式时，才回退到 `ucloud api --local-file` 的原始 Action 模式：

```bash
# 1. 将 payload 写入临时文件
cat > /tmp/ucloud-request.json << 'EOF'
{
  "Action": "DescribeULB",
  "ULBId": "ulb-xxxx"
}
EOF

# 2. 调用
ucloud --profile prod-account api --local-file /tmp/ucloud-request.json

# 3. 清理
rm -f /tmp/ucloud-request.json
```

对于小型 payload，inline flag 风格也可以：

```bash
ucloud --profile prod-account api --Action DescribeULB --ULBId ulb-xxxx
```

回退到 API 前，先记录为什么产品子命令不可用或不适合。对于小型 payload，inline flag 风格也可以；对于大型或嵌套 payload，使用 `--local-file`。

## 工作规则

- 当请求可能影响已有资源时，优先执行只读查询命令或只读 Action。
- 在执行写入或删除操作前，在说明文字中明确输出具体的产品命令；如果回退到 API，则明确输出具体的 Action 名称。
- 在执行写入或删除操作前，明确输出将要使用的 profile 或配置来源：
  - 用户指定时输出 `Profile: <name>`
  - 使用本地激活配置时输出 `Profile: active`
- CLI 调试日志默认关闭。仅在用户明确要求打印日志或请求详细调试输出时才开启。
- 以清晰、格式化的结构展示面向用户的结果。优先使用简短的分段、Markdown 表格和带标签的字段，而不是原始 JSON 转储。
- 绝不在说明文字、计划、命令预览、补丁文本或面向用户的摘要中打印、重复或嵌入 `UCLOUD_PUBLIC_KEY`、`UCLOUD_PRIVATE_KEY` 或原始密钥材料。
- 优先使用已有 CLI profile，而非在命令行中收集凭据。将命令行、对话、工具日志和命令预览视为可见且不安全的渠道。
- 回退到 API 且 payload 较大时，使用 `--local-file` 而非长内联 JSON。
- 不捏造参数名。如果必填参数不明确，先查阅官方文档再执行。
- 每次回退到 `ucloud api` 调用前，从 `https://github.com/UCloudDoc-Team/api` 中确认确切的接口定义，而不是凭记忆或仅凭产品命令 help 来推断参数。
- 如果产品子命令形态、必填字段或资源语义不明确，先查阅 CLI help、CLI 文档、产品文档；仍无法确认时再查阅官方 API 文档，不要臆测。
- 如果用户请求写入操作且标识模糊，先查询，然后根据返回数据确认确切的目标。
- 当缺少信息时，仅询问阻塞执行的字段，例如 `Region`、`ProjectId`、`ULBId` 或预期的 profile 名称。
- 用户回复后，将值规范化为确切的产品命令 flag 或 API 字段名，并继续执行，不要重启整个流程。
- 如果用户提供了混合的自由文本和结构化数据，提取可用的值，简要展示解析后的命令参数或 payload，然后执行。
- 即使最终需要 `ucloud api --local-file`，也应先确认没有合适的产品子命令可以完成该操作。

## 输出风格

- 默认使用简洁的 Markdown，配合明确的段落标签，如 `Action`、`Result`、`Resources`、`Errors`、`Next Steps`。
- 对于单个资源或单个操作结果，优先使用两列表格，如 `字段 | 值`。
- 对于多个资源，优先使用紧凑表格，优先展示最关键的决策相关列，如资源 ID、名称、状态、Region、Zone、IP、计费模式。
- 仅当表格不适用时才使用列表，例如列举后续操作或注意事项时。
- 除非用户明确要求原始响应，否则不要直接转储原始 JSON。先进行摘要，然后仅展示与任务相关的重要字段。
- 在执行前展示解析后的请求参数时，以简洁的标签列表或表格形式呈现，便于用户快速核对范围。
- 在所有格式化输出中，遮盖或省略密钥和敏感令牌。
- 如果结果集较大，先展示最相关的几行摘要表格并提及还有更多条目，而不是粘贴过长的响应。

## 缺失信息处理

- 缺失范围：
  仅在所选产品命令或 API Action 需要且环境尚未提供时，才向用户询问 `ProjectId`、`Region` 或 `Zone`。
- 可选默认范围：
  可以从 CLI profile、用户上下文或环境变量 `UCLOUD_PROJECT_ID`、`UCLOUD_REGION`、`UCLOUD_ZONE`、`UCLOUD_BASE_URL` 中读取默认范围。这些不是前置条件，只在命令需要且用户未明确指定时使用。
- 缺失目标资源：
  请用户提供确切的标识，如 `ULBId`、`EIPId`、`VPCId`、`InstanceId` 或其他命令/API 专用的 ID。
- 缺失命令或 Action 参数：
  仅在查阅 CLI help、CLI 文档、产品文档、必要时的 API 文档和当前上下文后仍缺失的必填字段，才向用户询问。
- 收到回复后：
  将回复转换为命令参数或 JSON 对象，与已有参数合并，直接继续同一产品命令或 API Action，而不是让用户重新陈述完整请求。

## 错误处理

- 发生错误时，如果修复方案安全且可以从当前上下文、CLI help、官方文档或 lookup API 中推导出来，首先尝试自动诊断并修复。
- 不要盲目重试。每次重试必须基于明确的诊断。
- `299 IAM permission error` 不要立即视为权限不足，先按 API 定义确认是否缺少 `ProjectId`。
- 具体重试条件、`299` 分流规则、profile 失败处理和错误报告格式见 [`references/error-handling.md`](./references/error-handling.md)。

## 通用 Lookup API

当公共参数缺失时，在询问用户之前使用 lookup API 进行发现：

- `ListRegions`：当缺少 `Region` 或用户仅给出了城市或产品名称时，查询可用 Region。
- `ListZones`：当缺少 `Zone` 且已知或可以推断所选 Region 时，查询可用 Zone。
- `GetProjectList`：当缺少 `ProjectId` 时，查询可访问的项目。
- `GetBalance`：在创建计费资源前，当配额或账单就绪情况可能影响操作时，查询账户余额。

使用这些 lookup API 先缩小缺失值的范围。如果查询后仍存在多个有效候选项，将简短列表呈现给用户并请其选择。具体调用方式、字段提取规则和示例见 [`references/common-lookups.md`](./references/common-lookups.md)。

## 使用示例

### 产品子命令优先

```bash
ucloud uhost list --region cn-bj2
ucloud eip list --region cn-bj2
```

### API inline flag 风格（产品子命令不可用且 payload 小）

```bash
ucloud api --Action DescribeInstance --region cn-bj2
```

### API local file 风格（产品子命令不可用且 payload 大或嵌套）

```bash
cat > /tmp/ucloud-request.json << 'EOF'
{
  "Action": "DescribeULB",
  "Region": "cn-bj2",
  "ULBId": "ulb-xxxx"
}
EOF
ucloud --profile prod-account api --local-file /tmp/ucloud-request.json
rm -f /tmp/ucloud-request.json
```

### 使用本地激活 profile

```bash
ucloud uhost describe --region cn-bj2
```

### 单次调用开启 CLI debug

```bash
UCLOUD_CLI_DEBUG=on ucloud uhost list --list cn-bj2
```

### 生成字母数字密码

```bash
tr -dc 'A-Za-z0-9' </dev/urandom | head -c 20
```

## 参考资料

- 当需要决定产品子命令和 `ucloud api` 兜底路径应信任哪个官方信息来源时，首先阅读 [`references/doc-sources.md`](./references/doc-sources.md)。该文件定义了查询顺序并指向 `https://github.com/UCloudDoc-Team/api`。
- 当需要将用户请求转换为实际 CLI 调用时，阅读 [`references/cli-usage.md`](./references/cli-usage.md)，包括产品子命令优先、profile 选择规则、`ucloud api --local-file` 和 payload 结构约定。
- 当需要识别产品别名、部署资源默认值或产品专属约束时，阅读 [`references/product-rules.md`](./references/product-rules.md)，再按索引读取对应产品文件。
