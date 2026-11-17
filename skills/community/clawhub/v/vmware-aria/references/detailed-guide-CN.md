> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。


# VMware Aria

[![PyPI](https://img.shields.io/pypi/v/vmware-aria)](https://pypi.org/project/vmware-aria/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [MCP 配置](#readme-mcp-configuration) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

默认通过本地 Stdio 运行；请在本机配置所需目标和凭据。

通过 Model Context Protocol (MCP) 为 VMware Aria Operations（原 vRealize Operations）提供 AI 辅助的监控与容量规划能力。

MCP 默认使用本地 stdio。启用可选 HTTPS 后会打开配置的监听端口，并要求 TLS 与调用者认证；此时属于网络服务。凭据示例先创建仅当前用户可读写的占位文件，拒绝覆盖已有文件，再由用户在本地编辑秘密值。

容器示例先在本地构建带版本标签的镜像，再用 `--pull=never` 运行，避免回退到镜像仓库拉取。本地版本标签不等于不可变的镜像摘要。

### 产品版本与功能证据

支持识别 Aria Operations / vRealize Operations 8.x 与更名后的 VCF Operations 9.x。
9.1.1.0 属于 9.x；文档示例未逐个列出补丁号，不代表不支持。先用 `get_aria_health` / CLI
`health status` 读取产品版本，再按具体接口响应判断。查询成功只证明该次查询范围可用，不代表全部
功能已验证；401/403 是认证/权限问题，404 或原始路径未入索引也不能直接概括为整个产品不兼容。
原有最低版本限制、Policy 与索引路径白名单继续生效；本文不宣称已完成 9.1.1.0 全功能真机验证。

### 概述

`vmware-aria` 提供 46 个 MCP 工具，支持通过自然语言 AI Agent（Claude Code、Cursor、Goose 等）与 Aria Operations 交互：

| 类别 | 工具 | 类型 |
|------|------|------|
| **资源** | 列表、详情、指标、健康评分、高消耗排名、指标键、属性、关联关系 | 只读 (8) |
| **告警** | 列表、详情、溯源（告警→资源）、确认、取消、告警定义、备注（查看 / 添加）、处置建议 | 读+3写 (9) |
| **告警定义** | 症状定义、创建、启用/禁用、删除 | 读+3写 (4) |
| **容量** | 概览、剩余容量、时间预测、虚拟机调整 | 只读 (4) |
| **报表** | 模板、生成、列表、状态、删除 | 读+2写 (5) |
| **异常** | 异常列表、风险评分 | 只读 (2) |
| **健康** | 平台健康、采集器状态、Aria 节点内存/交换/堆、适配器采集状态 | 只读 (4) |
| **维护** | 开始 / 结束资源维护模式、维护计划 | 读+2写 (3) |
| **Fleet / PromQL**（VCF Ops 9.1） | Fleet 证书、密码账户、VCF 域、诊断发现、实时 PromQL 查询 | 只读 (5) |
| **原始 API** | 搜索 API 操作索引、GET 一个索引内的路径 —— 用于上面工具都覆盖不到的读取 | 只读 (2) |

**共 46 个工具** — 36 只读、10 写操作

完整的 Agent 指令见 [`skills/vmware-aria/SKILL.md`](../../../skills/vmware-aria/SKILL.md).

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.10` 和 `uv`。

```bash
uv tool install vmware-aria==2.4.7
vmware-aria --help
```

目标、凭据和本地数据目录设置见 [setup guide](../../../skills/vmware-aria/references/setup-guide.md).

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 快速开始

```bash
# 安装
uv tool install vmware-aria==2.4.7

# 配置
mkdir -p ~/.vmware-aria
cat > ~/.vmware-aria/config.yaml << 'EOF'
targets:
  prod:
    host: aria-ops.example.com
    username: admin
    port: 443
    verify_ssl: true
    auth_source: LOCAL
default_target: prod
EOF

# 设置密码（绝不存入 config.yaml）
(
  umask 077
  set -C  # 拒绝覆盖已有文件；已有 .env 请直接用本地编辑器修改
  cat > ~/.vmware-aria/.env <<'EOF'
VMWARE_ARIA_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# 继续前，先用本地编辑器填写 .env；不要在终端命令中输入真实秘密值。

# 验证配置
vmware-aria doctor
```

模板只写入占位符。创建后用本地编辑器填写密码或令牌；不要把真实凭据粘贴到终端命令、聊天或提交中。若文件已存在，上述命令会拒绝覆盖；直接编辑现有文件并先确认权限为 `600`。

macOS 上的 v2.4.3 会遵守系统代理对 Aria 目标的绕过规则。如果旧版本能连通 TCP/443，
但获取认证 token 时 TLS 连接被关闭，请升级后重新运行 `vmware-aria doctor`。
`doctor --skip-auth` 只检查 TCP 连通性。

#### 离线 / 气隙环境安装（从源码）

本项目采用现代 PEP 517 构建系统（hatchling），因此**没有 `setup.py`**——这是
有意为之，不是缺失文件。如果你克隆源码后遇到 `ERROR: File "setup.py" or
"setup.cfg" not found ... editable mode currently requires a setuptools-based
build`，说明你的 `pip` 早于 21.3，无法对非 setuptools 后端做*可编辑*（`-e`）
安装。可编辑模式只是开发便利，运行本工具并不需要——任选其一：

```bash
# 从源码树安装——普通（非可编辑）安装会构建 wheel：
pip install .              # 不是  pip install -e .

# ……或先升级 pip，之后可编辑安装也能用：
pip install --upgrade pip && pip install -e .
```

对于**真正的气隙主机**，在联网机器上构建 wheel 再拷贝过去——目标主机无需联网：

```bash
# 在联网机器上，把本包及其依赖收集为 wheel：
pip wheel . -w dist        # → dist/*.whl   （或：uv build，仅构建本包）

# 把 dist/ 拷到气隙主机，然后离线安装：
pip install --no-index --find-links dist vmware-aria
```


### 认证机制

Aria Operations 使用 **vRealizeOpsToken** 认证：

```
POST /suite-api/api/auth/token/acquire
Body: {"username": "admin", "password": "...", "authSource": "LOCAL"}
响应: {"token": "abc123", "validity": 1765182896000}

后续请求 Header: Authorization: vRealizeOpsToken abc123
```

Token 为 6 小时滑动有效期（每次调用自动延长，官方规范行为），客户端在到期前 60 秒自动重新获取。响应中的 `validity` 字段是到期时间戳（epoch 毫秒），不是时长。


### 密码命名规则

| 目标名 | 环境变量 |
|--------|---------|
| `prod` | `VMWARE_ARIA_PROD_PASSWORD` |
| `aria-lab` | `VMWARE_ARIA_ARIA_LAB_PASSWORD` |
| `staging-01` | `VMWARE_ARIA_STAGING_01_PASSWORD` |

规则：`VMWARE_ARIA_<TARGET大写>_PASSWORD`，连字符转为下划线。

#### 配套 Skill

| Skill | 功能范围 | 工具数 | 安装 |
|-------|---------|:-----:|------|
| **[vmware-aiops](https://github.com/vmware-skills/VMware-AIops)** ⭐ 入口 | VM 生命周期、部署、Guest 操作、集群管理 | 60 | `uv tool install vmware-aiops` |
| **[vmware-monitor](https://github.com/vmware-skills/VMware-Monitor)** | 只读监控：告警、事件、VM 信息 | 32 | `uv tool install vmware-monitor` |
| **[vmware-nsx](https://github.com/vmware-skills/VMware-NSX)** | NSX 网络：Segment、网关、NAT、IPAM | 33 | `uv tool install vmware-nsx-mgmt` |
| **[vmware-nsx-security](https://github.com/vmware-skills/VMware-NSX-Security)** | DFW 微分段、安全组、Traceflow | 22 | `uv tool install vmware-nsx-security` |
| **[vmware-avi](https://github.com/vmware-skills/VMware-AVI)** | AVI / NSX ALB 负载均衡、AKO K8s 运维 | 28 | `uv tool install vmware-avi` |
| **[vmware-storage](https://github.com/vmware-skills/VMware-Storage)** | 数据存储、iSCSI、vSAN | 12 | `uv tool install vmware-storage` |
| **[vmware-vks](https://github.com/vmware-skills/VMware-VKS)** | Tanzu 命名空间、TKC 集群生命周期 | 23 | `uv tool install vmware-vks` |
| **[vmware-harden](https://github.com/vmware-skills/VMware-Harden)** | 合规基线、Drift 检测 | 8 | `uv tool install vmware-harden` |


</details>

<a id="readme-mcp-configuration"></a>

## MCP 配置

将以下配置复制到 MCP 客户端的本地 Stdio 配置中。客户端需要能找到 `uvx`；首次安装所需包时需要访问包源。

```json
{
  "mcpServers": {
    "vmware-aria": {
      "command": "uvx",
      "args": ["--from", "vmware-aria==2.4.7", "vmware-aria-mcp"],
      "env": {
        "VMWARE_ARIA_CONFIG": "~/.vmware-aria/config.yaml"
      }
    }
  }
}
```

以下保留预先安装 CLI 的用法及各工具特有的 MCP 选项。

<details>
<summary>预先安装的 CLI 与其他 MCP 选项</summary>

### MCP 配置（Claude Code）

完成 `uv tool install vmware-aria==2.4.7` 后，在 `~/.claude.json` 中添加：

```json
{
  "mcpServers": {
    "vmware-aria": {
      "command": "vmware-aria",
      "args": ["mcp"],
      "env": {
        "VMWARE_ARIA_CONFIG": "~/.vmware-aria/config.yaml"
      }
    }
  }
}
```

> **v1.5.15+** 推荐使用单命令 `vmware-aria mcp`。旧的 `vmware-aria-mcp` 入口仍然
> 保留以向后兼容。如必须使用 `uvx --from vmware-aria==2.4.7 vmware-aria mcp`（不安装）
> 且公司 TLS 代理报 `invalid peer certificate: UnknownIssuer`，请设置
> `UV_NATIVE_TLS=true`，或直接使用上面的 `vmware-aria mcp` 形式。

然后即可使用自然语言：
- *"显示当前 CPU 占用最高的 10 台虚拟机"*
- *"列出所有严重告警并逐一确认"*
- *"生产集群的内存还够用多少天？"*
- *"哪些虚拟机资源配置过多？给出调整建议"*
- *"vm-web-01 上有没有异常检测结果？"*


</details>

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### 常用 CLI 示例

```bash
# 查看 CPU 消耗排名前 10 的虚拟机
vmware-aria resource top --metric 'cpu|usage_average' --top 10

# 查看所有严重告警
vmware-aria alert list --criticality CRITICAL

# 确认告警
vmware-aria alert acknowledge <alert-id>

# 查询虚拟机 CPU 和内存指标（最近 4 小时；"missing" 说明某个指标为何没有数据点）
vmware-aria resource metrics <vm-id> --metrics 'cpu|usage_average,mem|usage_average' --hours 4

# 集群容量规划
vmware-aria capacity remaining <cluster-id>
vmware-aria capacity time-remaining <cluster-id>

# 查找虚拟机资源调整建议（vCPU / 内存 当前 → 建议、调整方向、是否可执行）
vmware-aria capacity rightsizing

# Aria 平台自身健康检查：HEALTHY / DEGRADED / DOWN / UNKNOWN、逐服务状态、产品版本
vmware-aria health status

# Aria 节点是否内存不足？哪个适配器停止了采集？
vmware-aria health node
vmware-aria health adapters

# 查询指标前，先查出虚拟机实际上报的指标键
vmware-aria resource keys <vm-id> --filter 'mem|'

# 计划内操作前将主机置于维护模式 2 小时，之后结束维护（确认一次；--dry-run 只打印 API 调用）
vmware-aria maintenance start <host-id> --duration 120
vmware-aria maintenance end <host-id>

# 记录谁在处理某条告警，并查看 Aria 给出的处置建议
vmware-aria alert note-add <alert-id> "Taking this: rebooting esx-03"
vmware-aria alert recommendations <alert-id>
```

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 安全性

- 密码仅从环境变量或 `.env` 文件加载，不存入 `config.yaml`
- 每次 MCP 工具调用和每条访问 Aria 的 CLI 命令记录审计日志至 `~/.vmware/audit.db`（经 vmware-policy）；CLI 写操作（告警确认/取消、告警备注、告警定义管理、报表生成/删除、资源维护开始/结束）另写 `~/.vmware-aria/audit.log`
- API 响应经过净化处理（去除控制字符，截断至 500 字符），防止提示注入攻击
- MCP 的破坏性写操作（告警确认/取消、删除告警定义和报表、开始/结束维护）带 `confirm` 参数（默认 `false`）：不传 `confirm=true` 时只返回将改变什么的 `blast_radius`，不做任何修改；遇到阻断项（如资源已在维护中）或有字段读不到时，`confirm=true` 会被拒绝。旧的 `confirmed` 别名已在 2.4.2 移除，仍传它的调用会被当作未知参数拒绝
- 默认开启 TLS 校验；私有 CA 请把 `SSL_CERT_FILE` 指向包含你 CA 的证书包（见 setup guide）。`verify_ssl: false` 仅用于隔离的自签名实验环境

<!-- usage: remote-and-exposure -->

### 远程访问（HTTPS）与限制工具

默认情况下 `vmware-aria mcp` 通过 stdio 服务一个本地客户端，并提供全部工具。以下两个选项可以改变这一点
（需 vmware-policy ≥ 1.21.0）。

**通过 HTTPS 提供服务**，让其他机器上的客户端连接。每个调用者都需要一个 bearer token：

```bash
vmware-audit token create alice          # 只显示一次，交给 alice
vmware-audit token list                  # 只列名字
vmware-audit token revoke alice          # 下一个请求起即拒绝，无需重启
vmware-aria mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

连接客户端（以 Claude Code 为例；任何支持 streamable HTTP 和自定义请求头的 MCP 客户端都可以）：

```bash
claude mcp add --transport http vmware-aria https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-aria": {
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
- 审计日志把每个调用者记为 `token:<名字>`。调用并行执行：每个调用独占一个到 target 的会话，每个 target 最多
  `VMWARE_MCP_POOL_SIZE`（默认 2）个会话。每个会话都是在 target 上的一次登录；调用最多等待 300 秒拿到空闲会话。
- **能连到这个端点的人，都以该 server 配置的账号操作。** token 只用来识别调用者，不在平台上授予任何权限。
  每个权限级别单独起一个端点。
- **一个端点给多人或多种角色用：** 先运行一次 `vmware-audit roles enable`，再给每个 token 指定角色（`vmware-audit token create 名字 --role reader`，或在 `roles.yaml` 里定义可用的工具和 target；需 vmware-policy ≥ 1.24.0）。角色只能限定这个 token 在本端点上能调用什么，不能超出账号本身的权限。详见 vmware-policy README 的「网络调用者的角色」一节。

**只提供读工具，加上你选定的写工具：**

```bash
vmware-aria mcp --expose read --allow-write acknowledge_alert
# 或：VMWARE_ARIA_MCP_EXPOSE=read VMWARE_ARIA_MCP_ALLOW_WRITE=acknowledge_alert vmware-aria mcp
```

未提供的工具不会出现在客户端的工具列表里。取值错误或写工具名不存在时服务直接退出（exit 2）。
这只限制提供给客户端的工具，不是授权；账号本身仍应遵循最小权限。

详见 `skills/vmware-aria/references/setup-guide.md`（"Serving MCP over HTTPS"、"Limiting which tools are offered"）。

<a id="readme-troubleshooting"></a>

## 故障排查

安装问题请查看本页安装说明；操作前先用 CLI 的 `--help` 核对参数。反馈问题时仅提供经过脱敏的最小示例。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### 升级到 2.0

2.0 把 MCP 工具名改成动词在前（共改名 4 处）（例如 `findings_list` → `list_findings`, `fleet_certificate_list` → `list_fleet_certificates`, `fleet_domain_list` → `list_fleet_domains`），完整的新旧名对照表见
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first)。其他都不变：工具、参数、安全确认门和 CLI 命令都一样。
如果 agent 提示词、脚本或 `~/.vmware/rules.yaml` 里写了工具名，请改成新名——不过用旧名写的 deny 规则在
vmware-policy ≥ 1.18 下仍然生效（`vmware-audit policy` 会列出因改名而多匹配的规则），vmware-pilot ≥ 1.13 也会自动转换已保存工作流里的旧名。
如果还有 2.0 之前的安装共用这个 `rules.yaml`，请把它的 vmware-policy 也升到 ≥ 1.18.2：它会按新旧两个名字匹配每条规则，一份文件两边都管用。

<a id="readme-license"></a>

## 许可证

MIT

### 瞬时请求恢复

仅 GET 请求会在传输故障或 502/503/504 响应后自动重试。写请求即使显式提供
重试次数也只发送一次：未收到响应时，变更可能已经生效。再次写入前应先检查
目标状态。明确认证拒绝后的单次认证恢复单独处理。该边界已通过合成 HTTP
契约测试，不能据此宣称获得真实设备兼容性结论。
