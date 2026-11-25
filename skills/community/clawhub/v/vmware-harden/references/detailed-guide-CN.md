> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。


# VMware Harden

[![PyPI](https://img.shields.io/pypi/v/vmware-harden)](https://pypi.org/project/vmware-harden/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [MCP 配置](#readme-mcp-configuration) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

默认通过本地 Stdio 运行；请在本机配置所需目标和凭据。

> **声明**：本项目为社区维护的开源项目，**与 VMware, Inc. 或 Broadcom Inc. 无任何隶属、
> 背书或赞助关系。** "VMware"、"vSphere"、"ESXi"、"NSX" 为 Broadcom 商标。源码以 MIT 许可证
> 公开可审计，见 [github.com/vmware-skills/VMware-Harden](https://github.com/vmware-skills/VMware-Harden)。


AI 原生的 VMware 合规与基线核查工具，`vmware-*` skill 家族成员。

- **对 vSphere 只读**：全部 8 个 MCP 工具均带 `[READ]` 标记，没有任何一个会修改受管的 VMware
  基础设施；`scan_target` 只写本地 twin DB（它自己观测结果的缓存）。详见[只读设计](#只读设计)。

容器示例先在本地构建带版本标签的镜像，再用 `--pull=never` 运行，避免回退到镜像仓库拉取。本地版本标签不等于不可变的镜像摘要。

完整的 Agent 指令见 [`skills/vmware-harden/SKILL.md`](../../../skills/vmware-harden/SKILL.md).

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.10` 和 `uv`。

```bash
uv tool install "vmware-harden[collectors]==1.20.1"
vmware-harden --help
```

目标、凭据和本地数据目录设置见 [setup guide](../../../skills/vmware-harden/references/setup-guide.md).

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 快速开始

```bash
# scan 依赖 collectors extra：harden 通过 vmware-aiops / vmware-storage /
# vmware-nsx-security 读取清单，而 `uv tool install` 为每个工具单独建环境——
# 单独安装这些兄弟包，harden 是 import 不到的。
uv tool install "vmware-harden[collectors]==1.20.1"

# 只在已有 twin DB 上出报告，则不需要 collectors：
#   uv tool install vmware-harden==1.20.1

# 列出内置基线
vmware-harden baseline list

# 执行一次扫描
vmware-harden scan --target <vcenter-name> --baseline cis-vmware-esxi-8.0-subset

# 或使用等保 2.0 三级（国内合规独家）
vmware-harden scan --target <vc> --baseline dengbao-2.0-level3-vmware

# 查看结果
vmware-harden report
vmware-harden drift

# 生成修复建议
export ANTHROPIC_API_KEY=...  # 可选；未设置时回落到 mock 模板
vmware-harden advise --all-critical

# Web dashboard
vmware-harden web --port 8080  # → http://127.0.0.1:8080
```

#### 读结果：只看 violations 不构成结论

规则只能判定「真的采到了的配置」，而这件事有两种独立的失败方式。**没有任何采集器产出**
该属性的规则，压根不会执行。而**能执行**的规则，仍可能对某一台主机什么都没判定——
那台主机上取回的是空值或 `N/A` 哨兵（主机失联、账号权限不足、该 ESXi 版本没有这个设置）。
两种情况都不算通过：

```
$ vmware-harden report
No violations among the checks that could be made.

16 of 20 rules could not be evaluated — no collector provides the data they
check, so their result is unknown, not compliant. 6 of 8 per-node checks could
not be made across 2 node(s): the rules ran, but the values they read were
missing on those nodes, so those nodes are unknown rather than compliant.
Not evaluated:
  cis-esxi-2.1.1   no collector writes host.ntp_enabled
  ...
Not judged on these nodes (data missing):
  cis-esxi-2.2.1   esx-02    esxi_build
  ...
```

`--format json` 返回 `{"violations": [...], "coverage": {...}}`，MCP 工具返回同样的
`coverage` 块——所以 agent 读到 `violations: 0` 也不能据此判定合规。v1.9.0 之前，
「无人采集」那类规则匹配 0 行并被静默算作通过；v1.10.0 之前，「按节点缺数据」那类同样如此。
详见 RELEASE_NOTES.md。

两份清单对应的处理动作不同：前者等采集器补齐，后者查那台节点的连通性与扫描账号权限。


#### VMRC 复制粘贴的显式配置

VM 安全采集读取 `isolation.tools.copy.disable` 与 `isolation.tools.paste.disable`。
两个开关均显式为 true 时，`isolation_copy_disabled` 才为 true；任一显式为 false 时为 false；
其他情况保持缺失（无法判定），重复设置也不取最后值猜测。SCG 规则 `scg-vm-5` 及 v9 继承规则
检查这项显式配置，不验证实际复制粘贴行为、主机默认值或 guest/Tools 状态。
不会存储或返回无关的 `extraConfig` 值。


</details>

<a id="readme-mcp-configuration"></a>

## MCP 配置

将以下配置复制到 MCP 客户端的本地 Stdio 配置中。客户端需要能找到 `uvx`；首次安装所需包时需要访问包源。

```json
{
  "mcpServers": {
    "vmware-harden": {
      "command": "uvx",
      "args": ["--from", "vmware-harden[collectors]==1.20.1", "vmware-harden-mcp"],
      "env": {
        "VMWARE_AIOPS_CONFIG": "~/.vmware-aiops/config.yaml"
      }
    }
  }
}
```

Harden 的实时采集复用 `~/.vmware-aiops/config.yaml`；保留 `[collectors]` 以安装采集依赖。

以下保留预先安装 CLI 的用法及各工具特有的 MCP 选项。

<details>
<summary>预先安装的 CLI 与其他 MCP 选项</summary>

### MCP Server

```bash
vmware-harden mcp  # stdio MCP server（旧入口 vmware-harden-mcp 仍兼容）
```

MCP 客户端配置模板见 `examples/mcp-configs/*.json`。8 个 MCP 工具全部只读：
`list_baselines`、`list_violations`、`get_remediation`、`list_drift_events`、
`get_baseline_rules`、`scan_target`。

> **公司 TLS 代理网络下？** 不要用 `uvx` 启动 MCP server（可能报
> `invalid peer certificate: UnknownIssuer`）。改用 `uv tool install` 装好后的入口
> `vmware-harden mcp`（无需联网 resolve），或 `export UV_NATIVE_TLS=true`。


</details>

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### 内置基线

| 基线 ID | 规则数 | 适用对象 | 来源 |
|---------|-------|---------|------|
| `cis-vmware-esxi-8.0-subset` | 20 | host | CIS Benchmark v1.0 |
| `vsphere-scg-v8-subset` | 15 | host, vm | [VMware vcf-security-and-compliance-guidelines](https://github.com/vmware/vcf-security-and-compliance-guidelines) |
| `dengbao-2.0-level3-vmware` | 20 | host, vm, datastore, dfw_rule | GB/T 22239-2019 三级 |
| `pci-dss-4.0-vmware` | 10 | host, dfw_rule | PCI-DSS v4.0 |
| `eu-nis2-vmware` | 12 | host, dfw_rule | EU NIS2 指令（第 21/23 条，附件 I） |
| `bsi-itgs-basisabsicherung-vmware` | 10 | host | BSI IT-Grundschutz（OPS.1.1.4 + SYS.1.1） |
| `vmsa-advisories` | 3（每条收录的公告一条） | host, vcenter | 离线 VMSA 公告目录 —— 见[已知漏洞](#已知漏洞vmsa) |
| `vsphere-stig-v9-subset` ⚠️ *实验性* | 12 | host | vSphere 9 STIG 对齐的主机高级设置（[DoD/DISA STIG 内容](https://github.com/vmware/dod-compliance-and-automation)）—— 采集路径已在 ESXi 8.0.3 真机验证；9.x 尚未跑过 |
| `cis-vmware-esxi-9.0-subset` | 20 | host | 通过 `extends:` 继承 `cis-vmware-esxi-8.0-subset` |
| `vsphere-scg-v9-subset` | 15 | host, vm | 通过 `extends:` 继承 `vsphere-scg-v8-subset` |

`baseline list` 返回 10 个 ID：上表 7 组含规则的 YAML 基线（共 **99 条规则**）、两个 v9 别名（自身不含规则，解析为其 v8 父基线的规则），以及由公告目录生成、不读文件的 `vmsa-advisories`。

#### 已知漏洞（VMSA）

`vmsa-advisories` 用每台 ESXi 主机和 vCenter 本身的版本与 build 号，对照随包发布的**离线 VMware 安全公告目录**
（`vmware_harden/advisories/catalog.yaml`，在目录日期当天对照来源核对过）。每条公告一条规则；规则说明里引用它所对应的
等保 2.0 三级控制项（安全计算环境·入侵防范：应能发现可能存在的已知漏洞，并在经过充分测试评估后，及时修补漏洞）。

```bash
vmware-harden scan --target prod-vc --baseline vmsa-advisories
vmware-harden report                    # 每个受影响组件：修复版本，以及该 CVE 是否在 CISA KEV 中
vmware-harden report --format csv > vmsa.csv
```

| 结论 | 含义 |
|---|---|
| **affected（受影响）** | 记为违规，证据里写明修复它的版本。 |
| **fixed（已修复）** | 同一版本线，build 已达到或超过修复版本。 |
| **unknown（未知）** | 按节点列出原因：build 读不到、公告未列出该版本线或该线已停止支持、来源对某分支说法不一、目录尚未收录该产品。**从不算通过。** |

没有报出问题，意思是**截至目录日期没有已知的未修复公告**，不是"没有漏洞"：之后发布的公告不在目录里。build 号只在同一条
`major.minor` 版本线内比较（7.0 U3 的 build 数值可能大于 8.0 GA）。

**目录怎么来的。** 每条数据记录公告、CVE 和 build 号来源。首版在无法读取 Broadcom 公告时，使用 NVD、CISA KEV
和引用公告的独立来源。VMSA-2026-0006 现已直接对照 Broadcom 响应矩阵及 build 知识库核查，覆盖 vCenter 和 ESXi。
每个修复 build 均对照 `builds.yaml` 校验；修复版本可以早于汇总公告的发布日期。

跨产品公告按适用于该产品的 CVE 分别判断。节点证据的 `cves` 仅列仍受影响的 CVE，`cve_results` 保留每条结论/CVSS，
并提供 `max_affected_cvss`；已修复或属于其他产品的 CVE 不会影响该节点的 KEV 标记。规则仍使用公告本身的严重级别。
结论描述 build 暴露面；客户机配置和可利用性需要额外证据。缺少映射仍返回未知。

公告覆盖边界仍为 **2026-10-19**。随包 KEV 标记于 2026-11-08 对照 CISA **2026.11.06** 快照核查，
其来源与用户可选的在线刷新分开记录。更新单条公告不意味着已经收录之后的所有公告。

**可选的在线刷新。** `vmware-harden advisories update` 下载 CISA KEV 清单（加 `--nvd` 时还下载 NVD 评分），写入
`~/.vmware-harden/advisories-cache.json`，由目录加载器叠加：KEV 标记只增不减，CVSS 只补缺失值，修复版本永远不从这里取。
它还会列出 KEV 里有、但目录没有任何公告覆盖的 ESXi/vCenter CVE。KEV 拉取失败以退出码 1 结束，原有缓存保持不变；某条 NVD
记录读不到只会报告出来，不阻断 KEV 刷新。正在运行的 MCP server 在下一次调用时就会读到新缓存。报告会写明 KEV 最近一次核对的时间。
`vmware-harden advisories show` 显示目录日期和最近一次刷新时间。

#### 等保 2.0 三级（国内合规）

`dengbao-2.0-level3-vmware` 依据 **GB/T 22239-2019《信息安全技术 网络安全等级保护基本要求》第三级**
编写，把标准条款映射为可在 VMware 环境中自动取证的检查项，20 条规则按标准章节组织：

| 标准章节 | 规则数 | 覆盖内容（举例） |
|---------|:-----:|-----------------|
| 8.1.2 网络与通信安全 | 5 | 区域边界访问控制：DFW 默认拒绝策略是否存在、是否残留 ANY-to-ANY 放行规则 |
| 8.1.3 设备和计算安全 | 9 | 主机身份鉴别与访问控制：lockdown 模式、SSH 姿态、DCUI/Shell 超时、远程日志 |
| 8.1.3 恶意代码防范 + 可信验证（VM 级） | 2 | VM 层可信启动与防护相关配置 |
| 8.1.4 应用和数据安全 | 2 | 数据完整性/保密性：存储与传输加密 |
| 8.1.5 安全管理中心 | 1 | 集中审计与日志留存 |
| 8.1.6 安全管理制度 | 1 | 制度落地的可见证据 |

每条规则都带 `rationale`（引用标准原文表述）、`remediation`（含 `manual_steps` 与 `risk` 风险提示）
以及 `review_policy`（高危项要求人工复核 `human_review_required: true`）。因此扫描输出可以直接作为
等保测评的**佐证材料**，而不只是一个通过/失败的布尔值。

规则跨越多个 collector（vCenter 高级设置 + ESXi NTP + NSX DFW）。若只跑了 vCenter collector，
缺少对应采集器时，那些规则没有节点可匹配 —— 这是预期行为，不是误报。另需区分：属性无人采集的规则会记为「无法判定」(`coverage.undetermined`)，报告会点名是哪个属性。

```bash
vmware-harden scan --target <vc> --baseline dengbao-2.0-level3-vmware
vmware-harden report --format json > dengbao-violations.json
```

#### VCF 9.0 / 9.1 兼容性

现有基线（`cis-vmware-esxi-8.0-subset`、`vsphere-scg-v8-subset`、`dengbao-2.0-level3-vmware`、
`pci-dss-4.0-vmware`）可以正常扫描 VCF 9.0 / 9.1 集群 —— 多数规则针对的是在 8.x → 9.x 之间保持
稳定的主机高级设置。此外还提供 `cis-vmware-esxi-9.0-subset` 与 `vsphere-scg-v9-subset` 两个基线，
它们通过 `extends:` **逐条继承**对应的 v8 规则（不臆造 v9 专属编号），可直接用于 9.x 环境；
待 CIS / Broadcom 发布正式的 vSphere 9 基准后再替换为官方编号规则。

##### Broadcom 官方参考

- **Security Configuration Guides**：<https://core.vmware.com/security/> —— vSphere SCG v8 / 未来的 v9
- **SDKs**：<https://developer.broadcom.com/sdks> —— VCF Python SDK（通过 REST 获取主机配置）
- **CIS Benchmarks**：<https://www.cisecurity.org/cis-benchmarks/> —— CIS VMware ESXi Benchmark v1.0

### 自定义基线

```bash
vmware-harden baseline validate ./my-strict.yaml
vmware-harden baseline import ./my-strict.yaml --name my-strict-cis
vmware-harden scan --target <vc> --baseline my-strict-cis
```

YAML 支持 `extends:` 从内置基线继承。用户目录下的同名基线优先于内置基线，因此可以复制一份内置基线到
`~/.vmware-harden/baselines/` 再按站点要求覆写个别规则。schema 详见
`skills/vmware-harden/references/cli-reference.md`。

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 只读设计

vmware-harden 在设计上就是只读的 —— 8 个 MCP 工具全部带 `[READ]` 标记，没有任何一个会修改受管的
VMware 基础设施。`scan_target` 也只写本地 twin DB（`~/.vmware-harden/twin.duckdb`，观测结果的缓存，
不是受管基础设施）。本 skill 从不执行修复，修复一律交由 vmware-pilot。

### 远程访问（HTTPS）与限制工具

默认情况下 `vmware-harden mcp` 通过 stdio 服务一个本地客户端，并提供全部工具。以下两个选项可以改变这一点
（需 vmware-policy ≥ 1.21.0）。

**通过 HTTPS 提供服务**，让其他机器上的客户端连接。每个调用者都需要一个 bearer token：

```bash
vmware-audit token create alice          # 只显示一次，交给 alice
vmware-audit token list                  # 只列名字
vmware-audit token revoke alice          # 下一个请求起即拒绝，无需重启
vmware-harden mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

连接客户端（以 Claude Code 为例；任何支持 streamable HTTP 和自定义请求头的 MCP 客户端都可以）：

```bash
claude mcp add --transport http vmware-harden https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-harden": {
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
- 审计日志把每个调用者记为 `token:<名字>`。指定不同 target 的调用并行执行；不指定 target 的调用逐个执行，
  所以多人共用一个 server 时请写明 target。
- **能连到这个端点的人，都以该 server 配置的账号操作。** token 只用来识别调用者，不在平台上授予任何权限。
  每个权限级别单独起一个端点。
- **一个端点给多人或多种角色用：** 先运行一次 `vmware-audit roles enable`，再给每个 token 指定角色（`vmware-audit token create 名字 --role reader`，或在 `roles.yaml` 里定义可用的工具和 target；需 vmware-policy ≥ 1.24.0）。角色只能限定这个 token 在本端点上能调用什么，不能超出账号本身的权限。限定 target 的角色：`scan_target` 的 target 按 vmware-aiops 的配置检查；数据存储和 DFW 采集器会在 vmware-storage 和 vmware-nsx-security 的配置里查同一个名字，所以同一个名字在三份配置里必须指同一套系统。详见 vmware-policy README 的「网络调用者的角色」一节。

**限制工具：**本 server 的工具全部只读，所以 `--expose read` 在这里不改变任何东西，它是为有写工具的 skill
准备的。最小权限来自 server 使用的账号。

详见 `skills/vmware-harden/references/setup-guide.md`（"Serving MCP over HTTPS"、"Limiting which tools are offered"）。

<a id="readme-troubleshooting"></a>

## 故障排查

安装问题请查看本页安装说明；操作前先用 CLI 的 `--help` 核对参数。反馈问题时仅提供经过脱敏的最小示例。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

### 家族成员

- **vmware-aiops** —— 主机清单 + 运维（harden 的 HostCollector 依赖它）
- **vmware-monitor** —— 只读监控对照组
- **vmware-storage** —— 数据存储清单
- **vmware-nsx-security** —— DFW 清单
- **vmware-pilot** —— 执行修复（写操作；不在 harden 职责范围内）
- **vmware-policy** —— `@vmware_tool` 审计装饰器

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### GA 家族成员（自 v1.5.18 起）

生产可用的合规平台：**9 个内置基线**（CIS ESXi 8.0/9.0、vSphere SCG v8/v9、**等保 2.0 三级**、PCI-DSS 4.0、
**EU NIS2**、**BSI IT-Grundschutz**）、**99 条规则**、面向 ESXi 与 vCenter build 号的 **VMSA 已知漏洞比对**、多 vCenter Twin、drift 检测、
**LLM Remediation Advisor**、带 8 个受审计工具的 **MCP server**、Web dashboard，以及
`vmware-harden doctor` 环境诊断。

### 架构

- **Estate Digital Twin** —— 单文件 DuckDB，位于 `~/.vmware-harden/twin.duckdb`。所有 node ID 带
  target 前缀，多 target 并存安全。
- **Collectors** —— 惰性导入兄弟 `vmware-*` skill（无进程 spawn 开销）。所有采集都是 READ，写操作
  一律交由 vmware-pilot。
- **Baseline schema** —— Pydantic v2 严格模式（`extra="forbid"`），支持 `extends:` 继承与用户目录覆盖。
- **Drift** —— 纯 diff 函数，持久化可选；每次扫描后自动运行。
- **Advisor** —— LLM 驱动的 Suggestion 生成；Anthropic provider 带 prompt caching，无 API key
  或测试环境下回落到 mock。
- **Audit** —— 每个 MCP 工具都由家族 vmware-policy 的 `@vmware_tool` 包裹，写入 `~/.vmware/audit.db`。
- **Web** —— FastAPI + Jinja2 + Tailwind/HTMX/ECharts（CDN）。

### 实验室回归测试

```bash
export VMWARE_HARDEN_LAB_TARGET=<your-vc>
pytest tests/eval/regression -v -m lab
```

### GA 验收标准（v1.5.18）

- 221 项测试通过
- Bandit：任意严重级别下 0 issue
- 全部 8 个 MCP 工具均被审计
- SKILL.md ≤ 3000 词，符合家族规范
- SECURITY.md 含 6 个要素 + Broadcom 声明
- 6 组内置基线（99 条规则）
- `vmware-harden doctor` 环境诊断
- `vmware-*` 家族 GA 成员（版本对齐至 1.5.28）

### 参考

- 家族规范：monorepo 根目录 `CLAUDE.md`

<!-- usage: remote-and-exposure -->

<a id="readme-license"></a>

## 许可证

MIT

### DFW 父策略证据与验证范围

DFW 规则现在将真实父策略的 `display_name` 保存为 `section_name`。父名称缺失时
保持未知，不能用规则自己的名字代替。一个内置规则因此具备结构上的可判定
条件，冻结的待采集规则由 15 条降为 14 条；逐节点缺失证据仍为未判定。NSX
正向真机验证仍待补。聚合与缺失检查仅使用当前快照；父名称未知保留为覆盖缺口，
不会报成策略缺失，已成功采集的空 DFW 清单仍可判定缺失。

`posture_drift` 是有单元测试的预留基线演进辅助函数，尚无 CLI/MCP 入口；
`diff_snapshots` 保留为成对快照比较的库接口，已有持久化与扫描范围测试，CLI
使用当前漂移路径。不能仅因没有 CLI 入口就认定为死代码并删除库接口。
没有权威控制定义及证据来源时，不补写 9.x 专属控制；继承基线也不能证明
9.x 真机验证通过。
