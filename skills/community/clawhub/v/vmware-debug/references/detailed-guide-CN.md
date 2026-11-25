> 详细用法与架构参考。[返回简明介绍](../../../README-CN.md)。


# VMware Debug

[![PyPI](https://img.shields.io/pypi/v/vmware-debug)](https://pypi.org/project/vmware-debug/) [![License: MIT](https://img.shields.io/badge/License-MIT-green.svg)](#readme-license)

[English](detailed-guide.md) | 中文

维护者: Wei Zhou · [zhouwei008@gmail.com](mailto:zhouwei008@gmail.com)

社区维护的开源项目，非 VMware 或 Broadcom 官方产品。

[概述](#readme-overview) · [快速开始](#readme-quick-start) · [MCP 配置](#readme-mcp-configuration) · [能力与工作流](#readme-capabilities-and-workflows) · [安全与审计](#readme-safety-and-audit) · [故障排查](#readme-troubleshooting) · [配套 Skills](#readme-companion-skills) · [参考资料](#readme-reference) · [许可证](#readme-license)

<a id="readme-overview"></a>

## 概述

默认通过本地 Stdio 运行；具体数据来源和执行边界见下文。

> **声明**：本项目为社区维护的开源项目，**与 VMware, Inc. 或 Broadcom Inc. 无任何隶属、
> 背书或赞助关系。** "VMware"、"vSphere" 为 Broadcom 商标。源码以 MIT 许可证公开可审计。

VMware skill 家族的**诊断大脑**。你给出症状（报错、日志、变慢的 VM），它来跑系统化排查：
把其它 skill 取到的事件关联成一条时间线、检测突刺、给根因假设排序，并告诉你下一步该查什么。
它**不调用 VMware API**，也不执行修复；案卷操作写入 `$OPS_HOME` 下的本地案卷，每个工具还会单独记录审计。默认 stdio 不监听端口；可选的认证 HTTPS 使用调用者 token 和 TLS 证书/私钥。修复一律路由给 vmware-aiops（单步）或
vmware-pilot（多步、带审批门控），完全复刻 vmware-harden → vmware-pilot 的「顾问/执行」分工。

完整的方法论、事件信封约定和症状路由见 [`skills/vmware-debug/SKILL.md`](../../../skills/vmware-debug/SKILL.md)。

<a id="readme-quick-start"></a>

## 快速开始

需要 Python `>=3.10` 和 `uv`。

```bash
uv tool install vmware-debug==2.4.0
vmware-debug --help
```

目标、凭据和本地数据目录设置见 [setup guide](../../../skills/vmware-debug/references/setup-guide.md).

<details>
<summary>安装与配置详情（含离线安装）</summary>

### 安装

```bash
uv tool install vmware-debug==2.4.0
vmware-debug categories          # 看它能诊断哪些症状类别
```


### 离线 / 隔离网络安装（从源码）

本项目使用现代 PEP 517 构建系统（hatchling），所以**按设计就没有 `setup.py`**——这是预期行为，不是缺文件。
如果你克隆了源码后遇到 `ERROR: File "setup.py" or "setup.cfg" not found ... editable mode
currently requires a setuptools-based build`，说明你的 `pip` 低于 21.3，无法对非 setuptools 后端做*可编辑*（`-e`）安装。
可编辑模式只是开发便利，运行这个工具并不需要——任选其一：

```bash
# 在源码目录里——普通（非可编辑）安装会构建 wheel：
pip install .              # 不是  pip install -e .

# ……或者先升级 pip，可编辑安装也能用：
pip install --upgrade pip && pip install -e .
```

对于**真正隔离网络的主机**，在联网机器上构建 wheel 再拷过去——目标主机就不需要网络：

```bash
# 在联网机器上，把本包及其依赖收集成 wheel：
pip wheel . -w dist        # → dist/*.whl   （或：uv build，只构建本包）

# 把 dist/ 拷到隔离主机，然后离线安装：
pip install --no-index --find-links dist vmware-debug
```

<!-- usage: remote-and-exposure -->


</details>

<a id="readme-mcp-configuration"></a>

## MCP 配置

将以下配置复制到 MCP 客户端的本地 Stdio 配置中。客户端需要能找到 `uvx`；首次安装所需包时需要访问包源。

```json
{
  "mcpServers": {
    "vmware-debug": {
      "command": "uvx",
      "args": ["--from", "vmware-debug==2.4.0", "vmware-debug-mcp"]
    }
  }
}
```

Debug 不需要 vCenter 目标配置或 VMware 账号凭据；案卷操作写入本地账本，工具调用另有审计记录。

<a id="readme-capabilities-and-workflows"></a>

## 能力与工作流

### MCP 工具（14 个：7 读、7 写）

7 个写工具只写本地案卷，没有一个触及任何 VMware 系统。

**关联**——无状态，看一眼用：

- `build_incident_timeline`：[READ] 把已取到的事件关联成 时间线 + 突刺 + 排序后的根因假设 + 下一步检查建议
- `list_symptom_categories`：[READ] 列出能识别的症状类别 + 每类该查什么

**调查案卷**——需要持续推理的事件：

- `open_case`：[WRITE] 定义事件；返回案卷 id 和本环境能达到的结论等级
- `get_case_readiness`：[READ] 开始**之前**，按症状类别说明本环境能达到的等级
- `get_case_knowledge`：[READ] 接受哪些知识格式、挂载了什么、哪些条目适用于某个案卷
- `plan_case`：[READ] 下一步该取什么——每步给出 skill、工具和目的；按案卷当前状态重算
- `list_cases`：[READ] 案卷列表，最新的在前
- `get_case`：[READ] 单个案卷：范围、账本大小、等级历史
- `record_case_hypothesis`：[WRITE] 登记一个候选解释，或读取各假设的支持/反驳账本
- `submit_case_evidence`：[WRITE] 记录一条取到的事实，连同来源、查询和时间基准
- `record_case_gap`：[WRITE] 记录**没能**取到的东西，以及如何补上
- `record_case_timeline`：[WRITE] 把案卷收集到的一切关联成一条时间线
- `grade_case`：[WRITE] 从账本重算结论等级并记录
- `close_case`：[WRITE] 记录最终等级、归档，并写明留下了哪些未决项

**事件信封**：`{ts, source, severity, entity, text, fields}`。agent 把各源事件归一成此形状再交给
debug；debug 因此与其它包零运行时依赖。**请把每条事件的 `event_type` 保留在 `fields` 里**——
分类器除了正文之外也匹配它，而现代 vSphere 多数事件是 `EventEx`：正文是一句通用套话，
真正说明「这是什么事件」的只有 `eventTypeId`。

### 常用工作流

1. 用 `vmware-debug categories` 选择症状类别。
2. 由 Monitor、Aria 或 Log Insight 收集相关证据，按事件信封整理为 `events.json`；Debug 自身不连接这些系统。
3. 执行 `vmware-debug triage --events events.json`，检查时间线、假设及下一步调查建议。
4. 如果没有事件或数据源不可达，先检查数据源工具的配置与连通性，并保留证据缺口；不要把缺失数据视为正常。
5. 有依据的修复交给 AIops 或 Pilot 按各自门禁执行。

<a id="readme-safety-and-audit"></a>

## 安全与审计

### 安全

CLI 被策略拒绝时会显示原因和规则，以退出码 1 结束，并保留一条 `denied` 审计记录。

诊断引擎不连接 vCenter/NSX/Aria，也不需要 VMware 账号凭据。默认 stdio 不监听端口；可选 HTTPS 需要调用者 token 和 TLS 文件。每个工具都会单独写入 `~/.vmware/audit.db` 审计记录。案卷工具还会写本地案卷：证据、缺口、假设和等级历史只增不改；`timeline.md` 由证据重新生成，
`case.json` 保存当前等级和状态。多个写入者同样成立：每次写案卷都要先拿该案卷的锁文件（`.ledger.lock`，
独占创建），所以两个进程在共享的 `$OPS_HOME` 里写同一个案卷会被串行化，而不是互相丢条目；每个文件都先写到
临时文件名再移到位，读者不会读到写了一半的文件（在不支持硬链接的文件系统上，新的证据文件改为原地创建：
仍然绝不覆盖，但可能被读到写了一半）。崩溃进程留下的锁会连同持有者一起报告，从不自动删除；
确认没有进程在写该案卷后再手动删除。已发布的 1.11.3 及更早版本不拿这个锁，共享案卷目录的每台机器都要升级。
详见 [SECURITY.md](../../../SECURITY.md)。

### 远程访问（HTTPS）与限制工具

默认情况下 `vmware-debug mcp` 通过 stdio 服务一个本地客户端，并提供全部工具。以下两个选项可以改变这一点
（需 vmware-policy ≥ 1.21.0）。

**通过 HTTPS 提供服务**，让其他机器上的客户端连接。每个调用者都需要一个 bearer token：

```bash
vmware-audit token create alice          # 只显示一次，交给 alice
vmware-audit token list                  # 只列名字
vmware-audit token revoke alice          # 下一个请求起即拒绝，无需重启
vmware-debug mcp --transport https --host 0.0.0.0 --port 8443 \
    --cert /etc/vmware-mcp/server.pem --key /etc/vmware-mcp/server-key.pem \
    --public-name mcp.example.com
```

连接客户端（以 Claude Code 为例；任何支持 streamable HTTP 和自定义请求头的 MCP 客户端都可以）：

```bash
claude mcp add --transport http vmware-debug https://mcp.example.com:8443/mcp \
    --header "Authorization: Bearer $VMWARE_MCP_TOKEN"
```

```json
{
  "mcpServers": {
    "vmware-debug": {
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
- **一个端点给多人或多种角色用：** 先运行一次 `vmware-audit roles enable`，再给每个 token 指定角色（`vmware-audit token create 名字 --role reader`，或在 `roles.yaml` 里定义可用的工具和 target；需 vmware-policy ≥ 1.24.0）。角色只能限定这个 token 在本端点上能调用什么，不能超出账号本身的权限。详见 vmware-policy README 的「网络调用者的角色」一节。

**只提供读工具，加上你选定的写工具：**

```bash
vmware-debug mcp --expose read --allow-write close_case
# 或：VMWARE_DEBUG_MCP_EXPOSE=read VMWARE_DEBUG_MCP_ALLOW_WRITE=close_case vmware-debug mcp
```

未提供的工具不会出现在客户端的工具列表里。取值错误或写工具名不存在时服务直接退出（exit 2）。
这只限制提供给客户端的工具，不是授权；账号本身仍应遵循最小权限。

详见 `skills/vmware-debug/references/setup-guide.md`（"Serving MCP over HTTPS"、"Limiting which tools are offered"）。

<a id="readme-troubleshooting"></a>

## 故障排查

安装问题请查看本页安装说明；操作前先用 CLI 的 `--help` 核对参数。反馈问题时仅提供经过脱敏的最小示例。

<a id="readme-companion-skills"></a>

## 配套 Skills

VMware Skills 家族包含 14 个 MCP Server 和共享 Policy 库。按职责选择工具： [vmware-skills](https://github.com/vmware-skills).

### 配套 Skill

| 需求 | Skill |
|---|---|
| 故障关联 / 根因 | **vmware-debug**（本项目） |
| 集中日志检索 | vmware-log-insight（把 `search_logs` 结果喂给它） |
| vCenter 事件与告警 | vmware-monitor |
| 指标 / 异常 | vmware-aria |
| 执行修复 | vmware-aiops（单步）/ vmware-pilot（多步门控） |

<a id="readme-reference"></a>

## 参考资料

变更记录： [RELEASE_NOTES.md](../../../RELEASE_NOTES.md).

使用自己的模型和 Agent 宿主进行只读自测： [model-fit self-test](https://github.com/vmware-skills/marketplace/blob/main/MODEL_FIT_SELF_TEST.md).

### 升级到 2.0

2.0 把 14 个 MCP 工具中的 13 个改成动词在前（例如 `case_close` → `close_case`, `case_get` → `get_case`, `case_grade` → `grade_case`），完整的新旧名对照表见
[RELEASE_NOTES.md](../../../RELEASE_NOTES.md#v200--mcp-tools-renamed-verb-first)。其他都不变：工具、参数、安全确认门和 CLI 命令都一样。
如果 agent 提示词、脚本或 `~/.vmware/rules.yaml` 里写了工具名，请改成新名——不过用旧名写的 deny 规则在
vmware-policy ≥ 1.18.1 下仍然生效（`vmware-audit policy` 会列出因改名而多匹配的规则），vmware-pilot ≥ 1.13 也会自动转换已保存工作流里的旧名。
如果还有 2.0 之前的安装共用这个 `rules.yaml`，请把它的 vmware-policy 也升到 ≥ 1.18.2：它会按新旧两个名字匹配每条规则，一份文件两边都管用。

<a id="readme-license"></a>

## 许可证

MIT。
