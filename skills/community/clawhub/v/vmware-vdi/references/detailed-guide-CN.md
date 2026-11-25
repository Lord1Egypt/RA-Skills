> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。


# VMware VDI

[![PyPI](https://img.shields.io/pypi/v/vmware-vdi)](https://pypi.org/project/vmware-vdi/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [MCP 配置](#readme-mcp-configuration) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

默认通过本地 Stdio 运行；请在本机配置所需目标和凭据。

AI 驱动的 VMware / Omnissa **Horizon VDI** 智能运维 —— 桌面池、RDS 农场、**用户会话**、桌面机器、授权、
事件/健康/统计、即时克隆金像推送,通过 **Horizon 8 Connection Server REST API**(以 Horizon 8 为主,
兼容最新 Omnissa Horizon,同一套 `/rest/v1` API)。MCP server + CLI,VMware skill 家族成员。

> **声明**:社区维护的开源项目,**与 VMware, Inc.、Broadcom Inc.、Omnissa, LLC. 无任何隶属、背书或赞助关系。**
> "VMware"、"Horizon"、"Omnissa" 为各自商标。源码遵循 MIT 许可,公开可审计。

> **状态:v1.0.0(beta)。** REST 端点已对照官方 Horizon Server API 核实;GET 响应字段投影为防御式,
> 待真机 Connection Server 验证(在真实 Horizon 上跑一次 `vmware-vdi init` 即可确认)。由家族 harness
> 治理(审计 + 策略 + 教学性错误);读写授权交由 Horizon 管理账号的角色(RBAC)。

字段投影异常只需提交最小化、脱敏后的诊断示例。发布 issue 前去掉用户身份、会话 ID、机器/主机名、内部地址和凭据。

完整的 Agent 指令见 [`skills/vmware-vdi/SKILL.md`](../../../skills/vmware-vdi/SKILL.md).

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.10` 和 `uv`。

```bash
uv tool install vmware-vdi==2.4.6
vmware-vdi --help
```

目标、凭据和本地数据目录设置见 [setup guide](../../../skills/vmware-vdi/references/setup-guide.md).

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 快速开始

```bash
uv tool install vmware-vdi==2.4.6
vmware-vdi init      # 友好向导:连接 Connection Server 并发现你的桌面池
vmware-vdi doctor
```


</details>

<a id="readme-mcp-configuration"></a>

## MCP 配置

将以下配置复制到 MCP 客户端的本地 Stdio 配置中。客户端需要能找到 `uvx`；首次安装所需包时需要访问包源。

```json
{
  "mcpServers": {
    "vmware-vdi": {
      "command": "uvx",
      "args": ["--from", "vmware-vdi==2.4.6", "vmware-vdi-mcp"],
      "env": {
        "VMWARE_VDI_CONFIG": "~/.vmware-vdi/config.yaml"
      }
    }
  }
}
```

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### 能力(27 工具:16 读 / 11 写)

| 类别 | 工具 |
|------|------|
| **监控** | 健康速览、会话 列表/详情、机器 列表/详情、事件列表 |
| **统计** | 会话并发统计、按池利用率 |
| **管理** | 池/农场/应用池/授权/镜像 列表、AD 搜索;池 启用/禁用、授权 增/删 |
| **运维动作** | 会话 注销/断开/发消息、机器 重置/维护/移除 |
| **任务** | 任务状态;镜像推送、任务取消 |

授权查询支持 Horizon 的单个 `EntitlementInfo` 对象和分页的用户/组列表。
接口只返回 SID 时，名称保留为空、类型标为 `UNKNOWN`；无法读取的响应会报错，不能解释为无人获授权。

破坏性写操作预览爆炸半径、CLI 双重确认、`--dry-run`、统一审计到 `~/.vmware/audit.db`。
`push_desktop_pool_image` 重建整池桌面,爆炸半径最高,预览报受影响桌面数 + 在线会话数,并给出 `occupancy`:
`determined` 表示这两个数可信,`unknown` 表示存在既不属于任何桌面池、也不属于任何农场的会话行。
`unknown` 时在线会话数只是下限,confirm 会被拒绝而不是按"未经核实的 0"放行;要强推须显式
`--acknowledge-unknown-occupancy`,该确认会写进审计记录。存在不带桌面池 id 的机器行时,
受影响桌面数同样只是下限("至少 N 台"),confirm 会被拒绝,且没有覆盖开关。

MCP 侧每个受控写工具都有 `confirm` 参数(默认 `false`)。不带它调用时返回 `blast_radius` ——
对象身份、数量、最多 20 个标识符、`blockers` 与 `unmeasured` —— 不做任何改动;真正执行时的返回也带
同一个字典。agent 应先把它给用户看,用户同意后才传 `confirm=true`。只要爆炸半径依赖的某项读不到 ——
机器状态、会话用户、任务类型或状态、池的启用标志、池当前的授权名单 —— `confirm=true` 就会被拒绝,
错误信息会说明该去查什么。

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 远程访问（HTTPS）与限制工具

默认情况下 `vmware-vdi mcp` 通过 stdio 服务一个本地客户端，并提供全部工具。以下两个选项可以改变这一点
（需 vmware-policy ≥ 1.21.0）。

**通过 HTTPS 提供服务**，让其他机器上的客户端连接。每个调用者都需要一个 bearer token：

```bash
vmware-audit token create alice          # 只显示一次，交给 alice
vmware-audit token list                  # 只列名字
vmware-audit token revoke alice          # 下一个请求起即拒绝，无需重启
vmware-vdi mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

连接客户端（以 Claude Code 为例；任何支持 streamable HTTP 和自定义请求头的 MCP 客户端都可以）：

```bash
claude mcp add --transport http vmware-vdi https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-vdi": {
      "type": "http",
      "url": "https://mcp.example.com:8443/mcp",
      "headers": { "Authorization": "Bearer ${VMWARE_MCP_TOKEN}" }
    }
  }
}
```

- 没有 token 时服务不会启动；`--public-name` 之外的 Host/Origin 一律拒绝；绑定端口前会自检，确认未认证请求得到 401。
  证书要用客户端信任、且覆盖这些名字的证书。
- 在同一台机器上由反向代理终结 TLS 时，用 `--transport http --host 127.0.0.1 --public-name mcp.example.com`，
  并让代理透传 `Authorization` 头。
- 负载均衡或网关在另一台机器上时，保持 `--transport https`（自签证书也可以），在 `--public-name` 里写上负载均衡
  转发时带的 `Host` 名，并让它透传 `Authorization`。健康检查可以用 `GET /healthz`：不需要 token，只返回
  `{"status": "ok"}`（需 vmware-policy ≥ 1.23.0）。
- 每个请求带上 `traceparent` 或 `X-Request-ID`，它会记进审计记录；用 `vmware-audit log --correlation-id ID`
  就能查到平台上某一次请求对应的调用。
- 审计日志把每个调用者记为 `token:<名字>`。无论是否指定 target，调用都并行执行：每个 target 最多保持
  `VMWARE_MCP_POOL_SIZE` 个会话（默认 2），每个会话都是在该 target 上的一次登录。会话全被占用时，
  调用最多等待 300 秒。
- **能连到这个端点的人，都以该 server 配置的账号操作。** token 只用来识别调用者，不在平台上授予任何权限。
  每个权限级别单独起一个端点。
- **一个端点给多人或多种角色用：** 先运行一次 `vmware-audit roles enable`，再给每个 token 指定角色（`vmware-audit token create 名字 --role reader`，或在 `roles.yaml` 里定义可用的工具和 target；需 vmware-policy ≥ 1.24.0）。角色只能限定这个 token 在本端点上能调用什么，不能超出账号本身的权限。详见 vmware-policy README 的「网络调用者的角色」一节。

**只提供读工具，加上你选定的写工具：**

```bash
vmware-vdi mcp --expose read --allow-write add_entitlement
# 或：VMWARE_VDI_MCP_EXPOSE=read VMWARE_VDI_MCP_ALLOW_WRITE=add_entitlement vmware-vdi mcp
```

未提供的工具不会出现在客户端的工具列表里。取值错误或写工具名不存在时服务直接退出（exit 2）。
这只限制提供给客户端的工具，不是授权；账号本身仍应遵循最小权限。

详见 `skills/vmware-vdi/references/setup-guide.md`（"Serving MCP over HTTPS"、"Limiting which tools are offered"）。

<a id="readme-troubleshooting"></a>

## 故障排查

### 系统代理绕过

Horizon REST 客户端按操作系统的代理绕过列表直连配置的目标地址。
TLS 校验仍由 `verify_ssl` 控制，`SSL_CERT_FILE` 等 CA 环境设置继续生效；其他地址保留原有代理路由。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

### Companion Skills

- [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) —— 桌面背后的 vCenter 虚机
- [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) —— 只读 vSphere 监控
- [vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security) —— 桌面微隔离

<!-- usage: remote-and-exposure -->

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### 升级到 2.0

2.0 把全部 27 个 MCP 工具改成动词在前（例如 `ad_user_search` → `search_ad_users`, `app_pool_list` → `list_app_pools`, `entitlement_add` → `add_entitlement`），完整的新旧名对照表见
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first)。其他都不变：工具、参数、安全确认门和 CLI 命令都一样。
如果 agent 提示词、脚本或 `~/.vmware/rules.yaml` 里写了工具名，请改成新名——不过用旧名写的 deny 规则在
vmware-policy ≥ 1.18 下仍然生效（`vmware-audit policy` 会列出因改名而多匹配的规则），vmware-pilot ≥ 1.13 也会自动转换已保存工作流里的旧名。
如果还有 2.0 之前的安装共用这个 `rules.yaml`，请把它的 vmware-policy 也升到 ≥ 1.18.2：它会按新旧两个名字匹配每条规则，一份文件两边都管用。

<a id="readme-license"></a>

清单响应无法识别或分页安全上限耗尽时，会在写预览或确认执行使用不完整清单之前拒绝。confirm 和未知占用确认都不能绕过；Horizon 正向真机验证仍待补。

## 许可证

MIT

### 瞬时请求恢复

仅 GET 请求会在传输故障或 502/503/504 响应后自动重试。写请求即使显式提供
重试次数也只发送一次：未收到响应时，变更可能已经生效。再次写入前应先检查
目标状态。明确认证拒绝后的单次认证恢复单独处理。该边界已通过合成 HTTP
契约测试，不能据此宣称获得真实设备兼容性结论。
