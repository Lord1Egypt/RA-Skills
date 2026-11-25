> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。


# VMware Private AI

[![PyPI](https://img.shields.io/pypi/v/vmware-privateai)](https://pypi.org/project/vmware-privateai/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [MCP 配置](#readme-mcp-configuration) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

默认通过本地 Stdio 运行；请在本机配置所需目标和凭据。

VMware skill 家族的 **GPU / AI 基础设施** 视角 —— GPU 主机与设备清点、vGPU 消费者、实时 GPU 利用率、
vGPU / DirectPath 配置目录、vGPU 分配,以及 **Private AI Service(PAIS)** 的已服务模型与知识库,
覆盖 **vSphere 9.x / VCF 9.1** Web Services API(pyVmomi)与 PAIS REST API。MCP server + CLI。

> **声明**:社区维护的开源项目,**与 VMware, Inc.、Broadcom Inc.、NVIDIA Corporation 无任何隶属、背书或
> 赞助关系。** "VMware"、"vSphere"、"VCF" 为 Broadcom 商标;"NVIDIA"、"vGPU" 为 NVIDIA 商标。源码遵循
> MIT 许可,公开可审计:[github.com/vmware-skills/VMware-PrivateAI](https://github.com/vmware-skills/VMware-PrivateAI)。

> **状态:beta。** 家族第 15 个 skill,走独立版本线。每条 API 路径在使用前都对照官方
> Broadcom/NVIDIA 资料核实(见 `tests/eval/spec/privateai_endpoints.py`)——不凭记忆编写端点。GET 响应
> **字段名** 与部分 PAIS 路径为防御式,待真机 9.x 硬件验证(见 `skills/vmware-privateai/SKILL.md` 里的 beta 活口)。由家族 harness 治理
> (审计 + 策略 + 教学性错误);读写授权交由 vCenter 服务账号的 RBAC 角色。

配套命令还提供 GPU 就绪与访问检查、本地模型容量估算及本地气隙 bundle 检查。本地估算不调用模型提供方，也不消耗推理配额。提交 issue 的诊断示例须最小化并脱敏，去掉标识符、内部地址、敏感硬件/容量信息和凭据。

完整的 Agent 指令见 [`skills/vmware-privateai/SKILL.md`](../../../skills/vmware-privateai/SKILL.md).

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.11` 和 `uv`。

```bash
uv tool install vmware-privateai==2.5.4
vmware-privateai --help
```

目标、凭据和本地数据目录设置见 [setup guide](../../../skills/vmware-privateai/references/setup-guide.md).

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 快速开始

```bash
uv tool install vmware-privateai==2.5.4
vmware-privateai version
vmware-privateai gpu host-list        # 第一条读命令 —— 列出有 GPU 的主机
```

配置位于 `~/.vmware-privateai/config.yaml`(targets + 可选 `pais:` 段);密码与 PAIS bearer token 存于
`~/.vmware-privateai/.env`(chmod 600)。详见 `skills/vmware-privateai/references/setup-guide.md`。


</details>

<a id="readme-mcp-configuration"></a>

## MCP 配置

将以下配置复制到 MCP 客户端的本地 Stdio 配置中。客户端需要能找到 `uvx`；首次安装所需包时需要访问包源。

```json
{
  "mcpServers": {
    "vmware-privateai": {
      "command": "uvx",
      "args": ["--from", "vmware-privateai==2.5.4", "vmware-privateai-mcp"],
      "env": {
        "VMWARE_PRIVATEAI_CONFIG": "~/.vmware-privateai/config.yaml"
      }
    }
  }
}
```

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### 能力(20 个 MCP 工具 —— 19 读 / 1 写)

| 类别 | 工具 | 读/写 |
|------|------|:----:|
| **GPU 清点** | 主机 列表/详情、设备列表、vGPU 消费者列表 | 4 读 |
| **GPU 利用率** | 每台 vGPU 虚机实时利用率(GPU %、显存 %、温度) | 1 读 |
| **GPU 就绪** | 每台主机 vGPU/PAIS 就绪判定 + 阻塞原因 | 1 读 |
| **配置目录** | vGPU 配置列表、DirectPath 配置列表 | 2 读 |
| **配置校验** | 改 vGPU 配置前只读预检(电源态 + 主机是否提供) | 1 读 |
| **vGPU 分配** | 设置虚机 vGPU 配置(虚机须已关机) | 1 写 |
| **Private AI Service** | 已服务模型、模型目录、知识库、数据源 列表 | 4 读 |
| **PAIS MCP 工具目录** | 已注册 MCP 服务、工具批准状态与可用性 | 2 读 |
| **PAIS 监控** | 集群 GPU 汇总(利用率/显存/温度、热点/空闲、最忙) | 1 读 |
| **选型与 air-gap** | LLM GPU/存储选型顾问、本地 pais.yml 镜像清单 | 2 读 |
| **权限自检** | server 使用哪个账号,以及它在根文件夹上是否拥有各工具所需的 vSphere 权限 | 1 读 |

读操作严格无破坏性。唯一的写(`assign_vgpu`)会预览爆炸半径、拒绝已开机虚机、**绝不自行关机**、
CLI 双重确认、统一审计到 `~/.vmware/audit.db`;可先用 `validate_vgpu_profile` 预检。
`assign_vgpu` 的 `confirm` 默认 `false`:不带它调用时返回 `blast_radius` —— 虚机名称与 id、当前与目标配置、
是修改已有 vGPU 设备还是新增一个、电源状态、`blockers` 与 `unmeasured` —— 不做任何改动。已开机或挂起的虚机、
多台虚机同名、电源状态或设备列表读不到时,`confirm=true` 会被拒绝。
`get_pais_model_catalog` / `list_pais_data_sources` 走未确认的 PAIS 控制面路径(踩坑 #36:404 返回 base-URL
教学提示,不当 bug);`advise_pais_sizing` / `verify_pais_bundle` 无需连接(纯计算 / 本地文件解析)。
`list_pais_mcp_servers` 与 `list_pais_mcp_tools` 使用[官方 PAIS MCP API](https://developer.broadcom.com/xapis/vmware-private-ai-service-api/latest/mcp-servers/)
公开的路径；只返回有界的名称、可用性和批准状态，不返回服务 URL、请求头或原始工具 schema。
PAIS 批准控制目录可见性，后端 VMware Policy 与产品 RBAC 仍决定实际权限。这两个路径尚未在
真实 PAIS 设备上验证。

### 典型工作流

**1. 找空闲 GPU 并给虚机换 vGPU 配置**
```bash
vmware-privateai gpu device-list --vendor NVIDIA   # vm_count 0 = 空闲
vmware-privateai gpu consumer-list                 # 谁持有 vGPU、什么配置
vmware-privateai vgpu profile-list --host esx-07   # 该主机可分配的配置
vmware-privateai gpu vgpu-assign fin-train-01 grid_a100-4c --dry-run   # 预览
# 先用 vmware-aiops 关机,再:
vmware-privateai gpu vgpu-assign fin-train-01 grid_a100-4c            # 双重确认 + 审计
```
*失败分支*:提示 "VM is powered on" 时,先用 vmware-aiops 的 `power_off_vm`（CLI：`vmware-aiops vm power-off fin-train-01`）关机;提示配置不被主机
提供 / 显存不足时,`vmware-privateai gpu host-get <该主机>` 查看有效配置。

**2. 全域 GPU 利用率巡检**
```bash
vmware-privateai gpu utilization --top 10
```
*失败分支*:显示 `metrics unavailable` 不是错误 —— NVIDIA 主机 GPU 驱动未暴露该虚机的计数器。更深的
per-SM / MIG-slice 遥测 vSphere 不提供(需 NVIDIA DCGM)。

**3. 查看 PAIS 正在服务什么**
```bash
vmware-privateai pais model-list
vmware-privateai pais kb-list
```
*失败分支*:HTTP 404 通常是 base-URL 不匹配(`/api/v1` 前缀随部署而异、beta 未确认),查 `pais.endpoint`;
HTTP 401/403 表示 `VMWARE_PRIVATEAI_PAIS_TOKEN` 过期或缺权限,重新取 token。

**4. 查看 PAIS MCP 注册与批准状态（只读）**
```bash
vmware-privateai pais mcp-servers
vmware-privateai pais mcp-tools --server-id <PAIS_SERVER_ID>
```
若页面打印 `next --after`，可用 `--after <游标>` 取下一页。这些命令不注册或批准工具，
也不能证明后端调用者有权限；真实 PAIS 响应仍待验证。

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 安全

详见仓库根目录 `SECURITY.md`。要点:凭据仅存 `.env`(chmod 600、`b64:` 混淆);默认开启 TLS 校验;
所有 vSphere/PAIS 文本经 `vmware_policy.sanitize()` 防注入;读写授权交由 vCenter RBAC;
`assign_vgpu` 关机门控 + 双重确认 + 审计。

<!-- usage: remote-and-exposure -->

### 远程访问（HTTPS）与限制工具

默认情况下 `vmware-privateai mcp` 通过 stdio 服务一个本地客户端，并提供全部工具。以下两个选项可以改变这一点
（需 vmware-policy ≥ 1.21.0）。

**通过 HTTPS 提供服务**，让其他机器上的客户端连接。每个调用者都需要一个 bearer token：

```bash
vmware-audit token create alice          # 只显示一次，交给 alice
vmware-audit token list                  # 只列名字
vmware-audit token revoke alice          # 下一个请求起即拒绝，无需重启
vmware-privateai mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

连接客户端（以 Claude Code 为例；任何支持 streamable HTTP 和自定义请求头的 MCP 客户端都可以）：

```bash
claude mcp add --transport http vmware-privateai https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-privateai": {
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
- 会读写本机文件的工具（这里是：`verify_pais_bundle` 的 manifest 文件）永远碰不到本机的配置、token、审计日志和 TLS 私钥；通过网络访问时，
  除非用 `VMWARE_MCP_FILE_ROOT` 指定一个目录，否则这些工具不能访问本机文件（需 vmware-policy ≥ 1.23.1）。
- 审计日志把每个调用者记为 `token:<名字>`。调用并行执行，同一 target 上也一样：server 为每个 target 最多保持 `VMWARE_MCP_POOL_SIZE`（默认 2）个会话，每个会话都是在该 target 上的一次登录；一个调用最多等 300 秒拿到空闲会话（vmware-policy ≥ 1.22.0）。
- **能连到这个端点的人，都以该 server 配置的账号操作。** token 只用来识别调用者，不在平台上授予任何权限。
  每个权限级别单独起一个端点。`vmware-privateai access-info` 可查看是哪个账号、它能做什么。
- **一个端点给多人或多种角色用：** 先运行一次 `vmware-audit roles enable`，再给每个 token 指定角色（`vmware-audit token create 名字 --role reader`，或在 `roles.yaml` 里定义可用的工具和 target；需 vmware-policy ≥ 1.24.0）。角色只能限定这个 token 在本端点上能调用什么，不能超出账号本身的权限。详见 vmware-policy README 的「网络调用者的角色」一节。

**只提供读工具，加上你选定的写工具：**

```bash
vmware-privateai mcp --expose read --allow-write assign_vgpu
# 或：VMWARE_PRIVATEAI_MCP_EXPOSE=read VMWARE_PRIVATEAI_MCP_ALLOW_WRITE=assign_vgpu vmware-privateai mcp
```

未提供的工具不会出现在客户端的工具列表里。取值错误或写工具名不存在时服务直接退出（exit 2）。
这只限制提供给客户端的工具，不是授权；账号本身仍应遵循最小权限。

详见 `skills/vmware-privateai/references/setup-guide.md`（"Serving MCP over HTTPS"、"Limiting which tools are offered"）。

<a id="readme-troubleshooting"></a>

## 故障排查

### 系统代理绕过

PAIS REST 客户端按操作系统的代理绕过列表直连配置的目标地址。
TLS 校验仍由 `verify_ssl` 控制，`SSL_CERT_FILE` 等 CA 环境设置继续生效；其他地址保留原有代理路由。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

### Companion Skills

- [vmware-aiops](https://github.com/vmware-skills/VMware-AIops) —— AI 负载背后的 vCenter 虚机(开关机/快照/克隆/迁移)
- [vmware-vks](https://github.com/vmware-skills/VMware-VKS) —— GPU 使能的 Tanzu Kubernetes
- [vmware-monitor](https://github.com/vmware-skills/VMware-Monitor) —— 只读 vSphere 健康

本 skill 是这三者之上的 GPU 视角。

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### 升级到 2.0

2.0 把当时的全部 MCP 工具改成动词在前（例如 `directpath_profile_list` → `list_directpath_profiles`, `gpu_consumer_list` → `list_gpu_consumers`, `gpu_device_list` → `list_gpu_devices`），完整的新旧名对照表见
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first)。其他都不变：工具、参数、安全确认门和 CLI 命令都一样。
如果 agent 提示词、脚本或 `~/.vmware/rules.yaml` 里写了工具名，请改成新名——不过用旧名写的 deny 规则在
vmware-policy ≥ 1.18 下仍然生效（`vmware-audit policy` 会列出因改名而多匹配的规则），vmware-pilot ≥ 1.13 也会自动转换已保存工作流里的旧名。
如果还有 2.0 之前的安装共用这个 `rules.yaml`，请把它的 vmware-policy 也升到 ≥ 1.18.2：它会按新旧两个名字匹配每条规则，一份文件两边都管用。

<a id="readme-license"></a>

PAIS 清单的容器形状无法识别或包含非对象行时会返回可读错误，不能据此认定清单为空。已识别的空数组仍表示确实为空；PAIS 正向真机验证仍待补。

## 许可证

MIT

### PAIS 广场分页续查

广场分页游标是不透明标识。游标缺失、重复、过长或需要修改才能消毒时，停止
续查并返回 `status=partial`、`next_after=null`，不能据此判断注册表为空或已完整
读取。有效游标通过查询编码原样传递。这些边界已有合成 HTTP 响应测试，PAIS
正向真机验证仍待补。
