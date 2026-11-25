> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。


# VMware NSX Security

[![PyPI](https://img.shields.io/pypi/v/vmware-nsx-security)](https://pypi.org/project/vmware-nsx-security/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [MCP 配置](#readme-mcp-configuration) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

默认通过本地 Stdio 运行；请在本机配置所需目标和凭据。

VMware NSX DFW 微分段与安全管理 MCP skill — 22 个工具，涵盖分布式防火墙策略与规则、安全组、VM 标签、DFW 排除列表、Traceflow 数据包追踪和 IDPS。

> **配套 skill**：[vmware-nsx](https://github.com/vmware-skills/VMware-NSX)（网络）、[vmware-aiops](https://github.com/vmware-skills/VMware-AIops)（VM 生命周期）、[vmware-monitor](https://github.com/vmware-skills/VMware-Monitor)（监控）

MCP 默认使用本地 stdio。启用可选 HTTPS 后会打开配置的监听端口，并要求 TLS 与调用者认证；此时属于网络服务。凭据示例先创建仅当前用户可读写的占位文件，拒绝覆盖已有文件，再由用户在本地编辑秘密值。

完整的 Agent 指令见 [`skills/vmware-nsx-security/SKILL.md`](../../../skills/vmware-nsx-security/SKILL.md).

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.10` 和 `uv`。

```bash
uv tool install vmware-nsx-security==1.17.4
vmware-nsx-security --help
```

目标、凭据和本地数据目录设置见 [setup guide](../../../skills/vmware-nsx-security/references/setup-guide.md).

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 快速开始

```bash
uv tool install vmware-nsx-security==1.17.4

mkdir -p ~/.vmware-nsx-security
cp config.example.yaml ~/.vmware-nsx-security/config.yaml
# 编辑 config.yaml，填写 NSX Manager 地址

(
  umask 077
  set -C  # 拒绝覆盖已有文件；已有 .env 请直接用本地编辑器修改
  cat > ~/.vmware-nsx-security/.env <<'EOF'
VMWARE_NSX_SECURITY_NSX_PROD_PASSWORD=REPLACE_IN_LOCAL_EDITOR
EOF
)
# 继续前，先用本地编辑器填写 .env；不要在终端命令中输入真实秘密值。

vmware-nsx-security doctor
```

模板只写入占位符。创建后用本地编辑器填写密码或令牌；不要把真实凭据粘贴到终端命令、聊天或提交中。若文件已存在，上述命令会拒绝覆盖；直接编辑现有文件并先确认权限为 `600`。

#### 离线 / 隔离网络安装（从源码）

本项目采用现代 PEP 517 构建系统（hatchling），因此**没有 `setup.py`**——这是
预期设计，而非缺失文件。如果你克隆源码后遇到
`ERROR: File "setup.py" or "setup.cfg" not found ... editable mode
currently requires a setuptools-based build`，说明你的 `pip` 版本早于 21.3，
无法对非 setuptools 后端做 *editable*（`-e`）安装。Editable 模式只是开发便利，
运行本工具并不需要它——任选其一：

```bash
# 在源码目录中——普通（非 editable）安装会构建 wheel：
pip install .              # 不要用  pip install -e .

# ……或先升级 pip，editable 也可用：
pip install --upgrade pip && pip install -e .
```

若目标是**完全隔离网络的主机**，在联网机器上构建好 wheel 再拷贝过去，目标主机即无需联网：

```bash
# 在联网机器上，将本包及其依赖收集为 wheel：
pip wheel . -w dist        # → dist/*.whl   （或用 uv build 仅构建本包）

# 将 dist/ 拷到隔离主机，离线安装：
pip install --no-index --find-links dist vmware-nsx-security
```


</details>

<a id="readme-mcp-configuration"></a>

## MCP 配置

将以下配置复制到 MCP 客户端的本地 Stdio 配置中。客户端需要能找到 `uvx`；首次安装所需包时需要访问包源。

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
      "command": "uvx",
      "args": ["--from", "vmware-nsx-security==1.17.4", "vmware-nsx-security-mcp"],
      "env": {
        "VMWARE_NSX_SECURITY_CONFIG": "~/.vmware-nsx-security/config.yaml"
      }
    }
  }
}
```

以下保留预先安装 CLI 的用法及各工具特有的 MCP 选项。

<details>
<summary>预先安装的 CLI 与其他 MCP 选项</summary>

### MCP 服务器配置

**v1.5.15+ 推荐方式**：完成 `uv tool install vmware-nsx-security==1.17.4` 后，**一条命令启动 MCP**：

```bash
# 推荐 — 单命令，无网络依赖
vmware-nsx-security mcp

# 指定配置路径
VMWARE_NSX_SECURITY_CONFIG=/path/to/config.yaml vmware-nsx-security mcp
```

添加到 `~/.claude.json`：

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
      "command": "vmware-nsx-security",
      "args": ["mcp"],
      "env": {
        "VMWARE_NSX_SECURITY_CONFIG": "~/.vmware-nsx-security/config.yaml"
      }
    }
  }
}
```

<details>
<summary>备选方案：uvx（不安装）或 legacy 入口</summary>

```bash
# 不想安装，临时运行（每次需要联网 resolve 依赖）
uvx --from vmware-nsx-security==1.17.4 vmware-nsx-security mcp

# 旧 entry point（仍可用，向后兼容）
vmware-nsx-security-mcp
```

> **公司 TLS 代理网络下？** uvx 可能报 `invalid peer certificate: UnknownIssuer`。
> 推荐使用上面的 `vmware-nsx-security mcp`（无需联网），或 `export UV_NATIVE_TLS=true`。

</details>


</details>

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### 功能

| 类别 | 工具数 |
|------|--------|
| DFW 策略 | 列出、获取、创建、更新、删除、列出规则（6 个） |
| DFW 规则 | 创建、更新、删除、统计（4 个） |
| 安全组 | 列出、获取、创建、删除（4 个） |
| VM 标签 | 列出标签、应用标签、移除标签（3 个） |
| Traceflow | 运行追踪、获取结果（2 个） |
| IDPS | 列出 Profile、签名状态 + 全局设置（2 个） |
| DFW 排除列表 | 列出被排除的成员（1 个） |

**共 22 个 MCP 工具**（11 只读 + 11 写入）

#### DFW 排除列表

在 NSX 分布式防火墙排除列表上的虚拟机，其数据路径中没有 DFW：指名它的规则依然存在，但一条都不生效。
在 VCF 环境中，管理类虚拟机（vCenter、VCF Operations、NSX Manager）通常都在该列表上——某套真实的
NSX 9.1 环境中 12 台虚拟机有 10 台被排除。`list_dfw_exclusions` 列出该列表，`list_vm_tags` /
`get_group` / `list_dfw_policies` 会指出成员是否被排除，因此绝不会对 DFW 根本看不到的虚拟机报告
「受 DFW 策略保护」。`dfw_excluded: null` 表示无法读取该列表——这与 `false` 不是一回事。

### 常见操作

#### 对应用进行微分段

```bash
# 1. 按标签创建安全组 — 使用 create_group MCP 工具
#    （tag_scope=tier, tag_value=web → Condition value 为 "tier|web"；
#      多个条件类型（标签/IP/Segment）之间为 OR 关系）

# 2. 创建 DFW 策略
vmware-nsx-security policy create web-app-policy --name "Web to App" --category Application
```

#### 为 VM 打标签

```bash
# 查询 VM 及其 external ID
vmware-nsx-security tag list my-vm-01

# 使用 external ID 应用标签
vmware-nsx-security tag apply <external-id> --scope tier --value web
```

#### 追踪数据包路径

```bash
vmware-nsx-security traceflow run <src-lport-id> \
  --src-ip 10.0.1.5 --dst-ip 10.0.2.10 --proto TCP --dst-port 443
```

输出包含 `operation_state`（`IN_PROGRESS`/`FINISHED`/`FAILED`）、按
`resource_type` 区分的逐跳 `observations`（Dropped* 条目携带 `reason` +
`acl_rule_id`）以及 `dfw_hits` 命中摘要。

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 安全性

- **依赖检查**：有活跃规则时不允许删除策略；被 DFW 或网关防火墙规则/作用域引用、或属于某个父组的安全组不允许删除；引用扫描失败时中止删除
- **审计日志**：所有写操作记录到 `~/.vmware-nsx-security/audit.log`（JSON Lines 格式）
- **输入验证**：ID 字符集校验；API 返回文本经过 `_sanitize()` 清洗，防止提示注入
- **Dry-run 模式**：CLI 写命令均支持 `--dry-run` 预览
- **MCP 删除预览**：`delete_dfw_policy`、`delete_dfw_rule`、`delete_group` 默认只预览 —— 不传 `confirm=True` 时返回 `blast_radius`（将删除什么、`blockers`、`unmeasured`），不删除任何东西；仍有阻塞项或有读取失败时，`confirm=True` 会被拒绝
- **凭据安全**：密码仅从环境变量读取，永不写入 config.yaml

#### 配套 Skill

| Skill | 功能范围 | 工具数 | 安装 |
|-------|---------|:-----:|------|
| **[vmware-aiops](https://github.com/vmware-skills/VMware-AIops)** ⭐ 入口 | VM 生命周期、部署、Guest 操作、集群管理 | 49 | `uv tool install vmware-aiops` |
| **[vmware-monitor](https://github.com/vmware-skills/VMware-Monitor)** | 只读监控：告警、事件、VM 信息 | 27 | `uv tool install vmware-monitor` |
| **[vmware-nsx](https://github.com/vmware-skills/VMware-NSX)** | NSX 网络：Segment、网关、NAT、IPAM | 33 | `uv tool install vmware-nsx-mgmt` |
| **[vmware-storage](https://github.com/vmware-skills/VMware-Storage)** | 数据存储、iSCSI、vSAN | 11 | `uv tool install vmware-storage` |
| **[vmware-vks](https://github.com/vmware-skills/VMware-VKS)** | Tanzu 命名空间、TKC 集群生命周期 | 20 | `uv tool install vmware-vks` |
| **[vmware-aria](https://github.com/vmware-skills/VMware-Aria)** | Aria Ops 指标、告警、容量规划 | 28 | `uv tool install vmware-aria` |

<!-- usage: remote-and-exposure -->

### 远程访问（HTTPS）与限制工具

默认情况下 `vmware-nsx-security mcp` 通过 stdio 服务一个本地客户端，并提供全部工具。以下两个选项可以改变这一点
（需 vmware-policy ≥ 1.21.0）。

**通过 HTTPS 提供服务**，让其他机器上的客户端连接。每个调用者都需要一个 bearer token：

```bash
vmware-audit token create alice          # 只显示一次，交给 alice
vmware-audit token list                  # 只列名字
vmware-audit token revoke alice          # 下一个请求起即拒绝，无需重启
vmware-nsx-security mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

连接客户端（以 Claude Code 为例；任何支持 streamable HTTP 和自定义请求头的 MCP 客户端都可以）：

```bash
claude mcp add --transport http vmware-nsx-security https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-nsx-security": {
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
vmware-nsx-security mcp --expose read --allow-write apply_vm_tag
# 或：VMWARE_NSX_SECURITY_MCP_EXPOSE=read VMWARE_NSX_SECURITY_MCP_ALLOW_WRITE=apply_vm_tag vmware-nsx-security mcp
```

未提供的工具不会出现在客户端的工具列表里。取值错误或写工具名不存在时服务直接退出（exit 2）。
这只限制提供给客户端的工具，不是授权；账号本身仍应遵循最小权限。

详见 `skills/vmware-nsx-security/references/setup-guide.md`（"Serving MCP over HTTPS"、"Limiting which tools are offered"）。

<a id="readme-troubleshooting"></a>

## 故障排查

### 系统代理绕过

NSX Manager REST 客户端按操作系统的代理绕过列表直连配置的目标地址。
TLS 校验仍由 `verify_ssl` 控制，`SSL_CERT_FILE` 等 CA 环境设置继续生效；其他地址保留原有代理路由。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

<a id="readme-license"></a>

## 许可证

MIT
