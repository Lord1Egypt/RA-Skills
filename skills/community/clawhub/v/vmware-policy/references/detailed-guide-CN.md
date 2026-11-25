> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。

# VMware Policy

[![PyPI](https://img.shields.io/pypi/v/vmware-policy)](https://pypi.org/project/vmware-policy/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [库的使用](#readme-library-usage) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

共享库，不提供独立 MCP Server。

VMware MCP 技能家族的统一审计日志、策略执行与输入消毒基础设施层。

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.10` 和 `uv`。

```bash
uv tool install vmware-policy==1.26.0
vmware-audit --help
```

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 安装

```bash
pip install vmware-policy==1.26.0
```


</details>

<a id="readme-library-usage"></a>

## 库的使用

Policy 随其他 VMware 工具作为共享依赖使用，不要为它创建独立 MCP 市场条目。

### 使用方法

```python
from vmware_policy import vmware_tool

@vmware_tool(risk_level="high", sensitive_params=["password"])
def delete_segment(name: str, env: str = "") -> dict:
    ...
```

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### 撤销记录存储可用性

撤销记录写入失败时，已完成的平台操作仍返回成功，并在 stderr 显示警告。
存储会在下一次操作时重新尝试初始化，修复目录或磁盘后无需重启进程。
`vmware-audit undo-list` 和 `undo-show` 会将存储不可用报告为错误，不会显示成空记录。
返回的 `_undo_id` 才是逆操作已实际记录的证据。

### 报告工具*返回*的失败

大多数工具用抛异常表示失败，`@vmware_tool` 会记录下来。而捕获异常、返回一个错误载荷的工具，
看起来和一次成功调用一模一样——很长时间里它也确实被记成了成功，这同时意味着会为从未发生的变更
写入撤销令牌，熔断器也从来看不到失败。

现在 dict 形状的载荷会被自动识别。工具只要返回家族约定的形状，就什么都不用做：

```python
return {"error": msg, "hint": "Run 'vmware-nsx doctor'."}   # 记为失败
```

返回类型带不了这个标记的工具——比如返回控制台文本的——必须显式说明：

```python
from vmware_policy import report_tool_failure

except Exception as exc:
    report_tool_failure(str(exc))
    return f"Error: {msg}"
```

字符串是刻意不去嗅探的：返回控制台输出的 skill 可能把以 "Error:" 开头的文本当作*数据*输出，
把这些调用标为失败，就是方向相反的同一种误报。

### CLI 命令

```bash
vmware-audit log --last 20
vmware-audit log --status denied --since 2026-03-28
vmware-audit stats --days 7
vmware-audit policy          # 查看当前生效的规则
```

审计 CLI 的 `log --last`、`export --limit`、`undo-list --last` 必须大于 0；零或负值会在访问存储前被拒绝。

### 核心组件

| 组件 | 说明 |
|------|------|
| `@vmware_tool` | 装饰器 -- 包裹技能的 MCP 工具，负责策略前置检查 + 执行 + 写一条审计记录 |
| `AuditEngine` | 基于 SQLite WAL 的追加式审计日志引擎，支持日志轮转（100MB 阈值，保留 5 个归档） |
| `PolicyEngine` | 基于 YAML 的规则引擎：拒绝规则、维护窗口，文件变更时自动热加载。`change_limits` 根据后端读取的当前状态约束 AIops VM CPU/内存调整 |
| `sanitize()` | 提示注入防御 -- 清理 C0/C1 控制字符与 Unicode 格式字符后截断（默认 500 字符） |
| `vmware-audit` | Typer CLI -- 查询审计日志、导出 JSON、统计分析、查看规则状态 |

### 策略规则配置

读写授权由 vCenter/NSX 账号的 RBAC 决定。策略引擎只在其上叠加运维人员自己写的
拒绝规则和维护窗口，规则文件为 `~/.vmware/rules.yaml`（设置了 `$OPS_HOME` 时为
`$OPS_HOME/rules.yaml`）。`vmware-audit policy` 会报告当前生效的规则来源：

| 来源 | 条件 | 放行范围 |
|------|------|----------|
| `user` | 你的规则文件存在且加载成功 | 按你的规则 |
| `packaged-default` | 没有规则文件 | 使用随包附带的基线，它不拒绝任何操作 -- 策略层面全部放行 |
| `user-unreadable` | 你的文件存在但无法加载（YAML 错误、非 UTF-8） | 全部拒绝 -- 直到文件可加载为止；不会改用基线 |
| `baseline-unreadable` | 没有用户文件，且随包基线也无法加载 | 全部拒绝 |

PyYAML 是声明的依赖；若缺失，被装饰的工具调用会失败而不是被执行。规则文件变更后自动热加载。

`VMWARE_POLICY_DISABLED=1` 是运维人员的应急开关：在设置了它的进程中（MCP 宿主，
或 CLI 所在 shell），所有策略检查都会跳过，包括"规则无法加载时全部拒绝"。审计不受
影响 -- 每次跳过都会记录一条警告，两个入口的审计行 -- `@vmware_tool` 的 MCP 调用和
`@guarded` 的 CLI 命令 -- 状态都带 `_bypassed` 后缀（`ok_bypassed`、`error_bypassed`）。
请限制谁能修改 MCP 宿主进程的环境变量。

将默认规则复制到 `~/.vmware/rules.yaml` 并自定义：

```yaml
# 拒绝规则 -- 阻止特定操作
deny:
  - name: no-delete-in-prod
    operations: ["delete_*", "remove_cluster_host"]
    environments: ["production"]
    reason: "生产环境禁止破坏性操作"

# 维护窗口 -- 高/危险操作仅在窗口内允许
maintenance_window:
  start: "22:00"
  end: "06:00"

# 仅约束 AIops VM CPU/内存调整：相对真实当前配置的绝对变化百分比
# 同时约束增减，需使用已接入后端检查的新版本 AIops。
change_limits:
  max_cpu_change_pct: 20
  max_memory_change_pct: 50
```

规则修改后自动热加载，无需重启任何服务。

### 工具暴露范围

每个 skill 的 MCP server 都可以只提供一部分工具。`<cli> mcp --expose read`（或环境变量
`VMWARE_<SKILL>_MCP_EXPOSE=read`）只保留标注了 `readOnlyHint: true` 的工具；`--allow-write a,b`（或
`VMWARE_<SKILL>_MCP_ALLOW_WRITE`）在此基础上再保留指定的写工具。没有这个标注的工具一律算写工具。取值不认识，或者名字
不是这个 server 的写工具，server 会在开始服务前退出（退出码 2）。2.0 之前的旧工具名也可以用。

直接导入 server 对象的启动程序，可以调用同一段代码，不必去改 SDK 的私有注册表：

```python
from vmware_policy.exposure import restrict_tools

restrict_tools(mcp, skill="storage", expose="read", allow_write=["enable_iscsi"])
mcp.run(transport="streamable-http")
```

在已经运行的事件循环里请用 `await arestrict_tools(...)`。server 对象只需要有 SDK 公开的 `list_tools()` 和
`remove_tool()` 两个方法。`restrict_tools` 不读环境变量；如果要像 `<cli> mcp` 一样读取 `VMWARE_<SKILL>_MCP_*`，
请传入 `*settings("storage")`（或调用 `apply_or_exit`）。只要给了任一命令行选项，两个环境变量都会被忽略，两种来源不会混用。

会执行其他步骤的工具（计划、工作流或批量工具）能执行的所有写操作都会随它一起暴露，包括被这个设置隐藏的写操作。

这只决定向客户端提供哪些工具，**不是授权**：一次调用能改什么由账号权限决定，deny 规则对所有暴露出来的工具照样生效。

### 通过 HTTPS 提供 MCP

`vmware_policy.serve` 可以让 skill 的 MCP server 跑在 stdio（默认）、HTTPS，或者跑在本机 HTTP 上、由前面负责 TLS 的
反向代理转发。两种网络方式都必须先有 bearer token，没有 token 就不会绑定端口。

```bash
vmware-audit token create alice      # token 只显示这一次；文件里只存 sha256（权限 0600）
vmware-audit token list
vmware-audit token revoke alice      # 正在运行的 server 从下一个请求起就拒绝它
```

- token 存在 `$OPS_HOME/mcp-tokens`（默认 `~/.vmware`）。客户端发送 `Authorization: Bearer <token>`。
- `https` 需要 `--cert`/`--key`（PEM），以及客户端访问时用到的每一个主机名 `--public-name`；其他 Host 或 Origin 的请求
  一律拒绝（防 DNS 重绑定）。`http` 只能绑定 127.0.0.1、::1 或 localhost。
- 每条审计记录都写明调用者 `token:<名字>` 和接入方式（`mcp-https`、`mcp-http-loopback`）。
- 写明同一个 `target` 的调用依次执行，写明不同 target 的调用并行；没有写 target 的调用（即用 skill 的默认 target，
  或工具本身没有 `target` 参数）独占执行。等待中的调用按先来先服务处理，哪一类都不会把另一类饿死；想要并行，
  请写明 target。失控熔断按调用者分别计算。使用会话池的 skill（见下）不受这些限制。
- 一个会话只能由创建它的那个 token 名字使用（由 SDK 保证）。吊销一个 token 后用同样的名字新建，新 token 可以接着用
  旧会话，所以 token 泄露时请换一个新名字。空闲会话 30 分钟后过期。
- deny 规则可以按调用者限定：在 `$OPS_HOME/rules.yaml` 里写 `clients: ["intern-*"]`，只对这些 token 名字生效
  （stdio 和 CLI 调用不受这类规则影响）。
- 绑定端口之前，server 会先向自己发送不带 token 的 POST/GET/DELETE 请求，三个都得到 401 才会启动。
- `GET`/`HEAD /healthz` 不需要 token，返回 `{"status": "ok"}`，供负载均衡做健康检查；它不透露任何其他信息，
  也不校验 `Host`。其他所有路径都需要 token。
- 每条审计记录都带上调用方的关联 ID：`traceparent` 头里的 trace-id，没有则取 `X-Request-ID`，再没有取
  `X-Correlation-ID`（只保留安全字符，最长 128）。`vmware-audit log --correlation-id ID` 可以查出平台上某一次请求
  对应的记录。这个 ID 由调用方提供，只用于关联追踪，不能作为证明。
- 会读写本机文件的工具（虚拟机文件传输、OVA 和部署 spec 文件、kubeconfig 输出）永远碰不到本机的配置、token、审计日志
  和 TLS 私钥。通过网络访问时，这些工具默认完全不能访问本机文件，除非用 `VMWARE_MCP_FILE_ROOT` 指定一个目录；
  指定后只允许访问该目录里的路径。
- **同一个端点的所有调用者都以该 server 的账号执行操作。** token 用来识别调用者，在平台上不授予任何权限。按权限等级、
  按可以互相看到工作内容的人群，各开一个端点。

### 网络调用者的角色

多个人或 agent 可以按不同职责共用一个 HTTPS 端点（vmware-policy ≥ 1.24.0，HLD §18）。角色限定某个 token 在**这个端点上**
能用哪些工具和 target。它只能收窄 server 账号的用途，不能超出账号本身的权限，平台账号仍然是边界。

```bash
vmware-audit roles enable                      # 启用角色；已有 token 变成 admin
vmware-audit token create ops-agent --role reader
vmware-audit token create storage-team --role storage-operator
vmware-audit token set-role ops-agent admin    # 从它的下一个请求起生效
vmware-audit token list --long                 # 名字、角色、所在文件
vmware-audit roles check                       # 有不可用的角色或 token 时退出码为 1
```

- **内置角色：** `reader`（所有只读工具、所有 skill、所有 target）和 `admin`（server 提供的全部工具）。自定义角色写在
  `$OPS_HOME/roles.yaml`（仅属主可读写，属主须是运行 server 的用户）。每个键都必须写，「全部」要写成 `"*"`，这样编辑到一半
  被截断的文件只会让该角色不可用，而不会把它放宽：

  ```yaml
  roles:
    storage-operator:
      skills:
        storage:
          tools: read                    # read | "*"
          allow_write: [rescan_storage]  # 额外放开的写工具
          allow_escape: []               # 会绕开角色的工具，须逐个列名
          targets: ["vc-prod-*"]         # 该 skill 的 target 名（可用通配），或 "*"
        monitor: { tools: read, allow_write: [], allow_escape: [], targets: "*" }
      approve: none                      # vmware-pilot 审批：none | any | others
  ```

- **启用只需一条命令。** 执行 `roles enable` 之前，所有 token 照旧以 `admin` 身份工作，`token create --role` 会被拒绝。它把所有 token 移到 `$OPS_HOME/mcp-tokens.v2`（默认 `admin`，
  或用 `--assign 名字=角色` 指定），旧文件清空。此后同一台机器上仍在运行旧版 vmware-policy 的 server 会拒绝所有请求，
  所以要在同一次变更里一起升级。启用后 `token create` 必须带 `--role`。`$OPS_HOME/mcp-tokens.v2` 必须属于运行 server 的用户，
  所在目录不能让其他用户写。
- **每次调用都检查：** 工具本身，以及它解析出的 target（没给时用默认 target 的真实名字）。会读所有 target 的工具，
  除非角色对该 skill 的 targets 是 `"*"`，否则拒绝。会运行其他工具的工具（AIops 计划、批量操作、到期删除的 TTL），
  只有角色放开了它能运行的每一个工具才允许。被拒的调用记为 `denied`、`rule=role:<角色>`，并计入该调用者的失控熔断预算；每条审计记录都带调用者的角色。
- **绕开角色的工具**会给持有者超出角色的能力：凭据（`issue_*_kubeconfig`）、在虚机里执行代码、任意 API 路径（Aria
  `get_api_path`）、设置了 `VMWARE_MCP_FILE_ROOT` 时读写服务器本机文件。`reader` 永远不含这些；自定义角色只有在
  `allow_escape` 里逐个列名才拿得到。**持有绕开角色工具的角色，等同于这个账号本身。**
- **`tools/list` 按调用者过滤**：每个 token 只看到它的角色能调用的工具。server instructions 里的 target 地址只给 `admin` 看。角色不可用（`roles.yaml` 损坏、角色未定义）的原因写在 server 日志里，
  不告诉调用者。
- 没有声明角色元数据的 skill（在新版 Policy 下运行的旧版 skill）只允许 `admin` 使用。
- 网络模式的 server 里，没有已认证调用者的调用一律拒绝——从本版本起，不论是否启用角色。
- deny 规则可以按角色写：在 `rules.yaml` 里和 `clients:` 并列写 `roles: [reader]`。
- vmware-pilot：`approve: none` 不能审批；`others` 不能审批自己的 token 创建、或在草稿阶段编辑/确认过的工作流。
- token 和角色的变更（`token create/revoke/set-role`、`roles enable`）都会写入审计；`roles.yaml` 在 server 运行中每次变化，
  server 都会写一条 `roles_reload` 记录（文件的 SHA-256 和其中的角色）。
- `roles check` 检查 `roles.yaml` 和 token。它看不到各 skill 的工具，所以 `allow_write` 里拼错的工具名、或角色没覆盖组合工具
  能运行的工具，要等 server 拒绝调用时才会暴露。
- **角色只能区分只通过这个端点访问平台的人。** 持有账号凭据的人，或自己有 shell 并且网络能直达 vCenter 的 agent，
  都不在角色的约束之内。某个团队绝对不能写，最可靠的做法仍是给它一个只读账号、单独一个端点。

### 会话池

连接平台的 skill 可以为每个 target 维护一个小的会话池（`vmware_policy.pool.SessionPool`，`VMWARE_MCP_POOL_SIZE`，
默认 2），并用 `run_server(..., pooled=True)` 启动 server。通过网络方式访问时，每个调用在整个执行过程中独占自己在每个 target 上的会话
（工具返回的是普通数据，返回之后不再从会话读取任何东西），所以同一 target 的调用可以并行，最多到池的大小；没有写 target 的调用也不再
逐个执行。已经持有会话的调用不会等待另一个 target：那个 target 的池满时，它会拿到一个临时的额外会话，所以跨 target
的调用不会死锁。等会话超过 300 秒的调用会收到一条写明 target 的错误。每个会话都是 target 上的一次登录。stdio 和 CLI
仍然每个 target 缓存一个会话，与池里的会话分开。

### 权限自诊断

`vmware_policy.access.vsphere_access_info(si, target=, requirements=, tool=)` 是各 vSphere skill 的 `get_access_info`
工具的实现：target 使用哪个账号、每个工具需要哪些权限（来自 skill 的需求表），以及当前会话在根文件夹上是否持有这些
权限（`AuthorizationManager.HasPrivilegeOnEntities`，只需要 System.View）。"根上未授予"不等于"没有权限"：具体对象
上的授权不在检查范围内。查询失败记为 `undetermined`，绝不当作已授予。

### 风险等级

工具声明的等级会写入审计行，可被 deny 规则的 `min_risk_level` 匹配，并决定已配置的
维护窗口是否适用。等级本身不会拦截执行。

| 等级 | 示例 |
|------|------|
| `low` | list、get、info、status |
| `medium` | reconfigure、update |
| `high` | power off、migrate、snapshot revert |
| `critical` | delete VM、delete cluster |

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 安全

- 审计数据库（`~/.vmware/audit.db`，仅本地，目录 `0700` / 文件 `0600`）记录工具参数、结果、状态、操作系统用户和推断的 agent -- 请将其及归档视为敏感数据
- `sensitive_params` 中列出的参数存为 `***`；声明了 `sensitive_result=True` 的工具，其结果整体替换；参数和结果中的凭据类键名（`password`、`token`、`kubeconfig` 等）以及报错文本中的凭据样式内容，在 MCP 和 CLI 两条路径上都会被脱敏。键名不在该列表中的凭据必须在 `sensitive_params` 中声明
- `sanitize()` 防止通过 API 响应文本进行提示注入
- 策略旁路（`VMWARE_POLICY_DISABLED=1`）只跳过策略检查，不跳过审计

<a id="readme-troubleshooting"></a>

## 故障排查

安装问题请查看本页安装说明；操作前先用 CLI 的 `--help` 核对参数。反馈问题时仅提供经过脱敏的最小示例。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

### VMware 技能家族

| 技能 | 定位 | 安装命令 |
|------|------|---------|
| **vmware-aiops** | VM 生命周期 + 部署 + Guest Ops | `uv tool install vmware-aiops` |
| **vmware-monitor** | 只读监控 | `uv tool install vmware-monitor` |
| **vmware-storage** | 存储管理（iSCSI + vSAN） | `uv tool install vmware-storage` |
| **vmware-vks** | Tanzu Kubernetes | `uv tool install vmware-vks` |
| **vmware-nsx** | NSX 网络管理 | `uv tool install vmware-nsx-mgmt` |
| **vmware-nsx-security** | NSX 安全（DFW + 安全组） | `uv tool install vmware-nsx-security` |
| **vmware-aria** | Aria Ops 指标/告警/容量 | `uv tool install vmware-aria` |
| **vmware-avi** | AVI/ALB 负载均衡 | `uv tool install vmware-avi` |
| **vmware-harden** | 合规基线 + Drift 检测 | `uv tool install vmware-harden` |
| **vmware-vdi** | Horizon VDI 运维 | `uv tool install vmware-vdi` |
| **vmware-privateai** | Private AI GPU / 模型服务运维 | `uv tool install vmware-privateai` |
| **vmware-debug** | 故障关联 / 根因 | `uv tool install vmware-debug` |
| **vmware-log-insight** | 集中日志检索 | `uv tool install vmware-log-insight` |
| **vmware-pilot** | 多步骤工作流编排 | `uv tool install vmware-pilot` |
| **vmware-policy** | 审计 + 策略（本包） | `uv tool install vmware-policy==1.26.0` |

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### 架构

```
AI Agent -> vmware-pilot（按需编排）-> @vmware_tool 前置检查 -> skill 操作 -> 写一条审计记录 -> ~/.vmware/audit.db
```

vmware-policy 是所有 VMware 技能的**强制依赖**，提供：

- **审计日志**：经 `@vmware_tool` 包裹的 MCP 工具，其调用记录写入统一数据库 `~/.vmware/audit.db`
- **策略引擎**：deny 规则、维护窗口，热加载无需重启（变更限制为预留字段，不强制执行）
- **输入消毒**：所有来自 vSphere/NSX/Aria API 的文本经过 `sanitize()` 处理
- **AI Agent 检测**：根据环境变量记录调用方：`claude`、`codex`、`deerflow`、`local`（Ollama 主机）或 `unknown`

### 开发

```bash
git clone --branch v1.26.0 https://github.com/vmware-skills/VMware-Policy.git
cd VMware-Policy
uv venv && source .venv/bin/activate
uv pip install -e ".[dev]"
pytest --cov=vmware_policy
```

<a id="readme-license"></a>

## 许可证

MIT

### VM 配置调整限额

Policy 1.25.0 与 AIops 2.5.0 在后端提交任务前强制检查 CPU/内存变更百分比。
例如 CPU 4→8 变化 100%，4→3 变化 25%，均会被 20% 上限拒绝；恰好等于上限
则允许。检查范围内的配置调整遇到无效或未知限额、缺少当前配置或
`changeVersion` 时拒绝执行。ConfigSpec 绑定该版本，防止并发变更使比较基数
过期。调用方提供的百分比不可信；通用 `check_allowed(params=...)` 只做入口授权，
不代替后端状态检查。初始创建/克隆任务、存储及其他产品不在范围内；经该后端进行的部署后扩缩容仍会检查。旧版 AIops
不执行此限制，依赖该保护前必须升级两个包。并发拒绝已有合成契约测试，
尚待正向真机验证。

通过同一后端进行的部署后扩缩容仍会检查限额。拒绝时，新建 VM 可能已经存在，
且保持原始规格；重试前应先查看结果。最初的创建/克隆任务本身不执行百分比
限额检查，本轮不引入自动删除或重复克隆。
