---
name: tialink-tia-portal
slug: tialink-tia-portal
version: 1.0.8
displayName: TIA Portal automation over MCP (TiaLink)
summary: Drive a real Siemens TIA Portal (V19 / V20 / V21) project through the TiaLink MCP gateway - configure hardware and networks, create FB/FC/DB/UDT with SCL, compile, download to PLCSIM and read back to verify. Ships pre-flight checks and failure triage, so the agent verifies instead of guessing.
description: Operate a Siemens TIA Portal (V19 / V20 / V21) project from an AI agent - hardware and network configuration, FB/FC/DB/UDT creation with SCL, compile, download to S7-PLCSIM, read-back verification. Use when the user mentions TIA Portal, Siemens PLC automation, SCL programming, rack configuration or Openness, or wants an agent to work inside a PLC project. Requires the TiaLink gateway on the TIA Portal machine (commercial software; read-only without a licence).
license: CC-BY-4.0
tags: [tia-portal, siemens, plc, scl, openness, ladder, automation, industrial, mcp]
homepage: https://tia.hubwiz.com/tia-link?utm_source=clawhub&utm_medium=skill
metadata:
  publisher: hubwiz.com
  repository: https://github.com/tia-forge/tialink
  requires: TiaLink gateway on the TIA Portal machine (Windows + TIA Portal V19 / V20 / V21 + Siemens Openness user group; V21 needs TiaLink 1.5.0+)
  supported-tia-versions: V19, V20, V21
  transport: MCP Streamable HTTP (/mcp + Bearer token)
  body-language: zh-CN (checklists and triage), en (this summary)
---

# TIA Portal automation over MCP (TiaLink)

**Language note:** the checklists and failure triage below are in Chinese, because that is the working language of the
TIA Portal / Siemens PLC audience this skill was written for. This summary is in English so the skill is discoverable
and usable by English-speaking agents too.

## What the agent gets

One MCP endpoint (Streamable HTTP, Bearer token) that talks to a TiaLink gateway running **on the TIA Portal machine**.
Through it the agent can: inspect the open project (devices, slots, block list), configure hardware and networks,
create FB/FC/DB/UDT blocks and write SCL, compile, download to S7-PLCSIM, run the CPU, and read values back.

## 30-second check before anything else

```bash
curl -sS -o /dev/null -w "%{http_code}
" http://127.0.0.1:8080/mcp
```

**A 4xx answer means the gateway is reachable** (it is just refusing an unauthenticated call). `Connection refused`
or a timeout means network/gateway trouble - fix that before reading further.

## When to use it

- The user wants an agent to work inside a real TIA Portal project (V19 / V20 / V21), not to produce code in the abstract.
- Verification matters: compile errors, download failures and read-back values are reported by the real toolchain.

## When NOT to use it

- No TIA Portal on any machine the agent can reach - use the cloud documentation / simulation / rendering skills instead.
- The user only wants SCL text: create it locally, no gateway needed.

## If the client is not on the gateway machine

Run the gateway on the TIA Portal machine and put the client behind a **local port forward**, so the token never
crosses the network in clear text:

```bash
# on the client machine: 8080 locally -> gateway's loopback
ssh -L 8080:127.0.0.1:8080 <user>@<gateway-host>
```

Then every example below keeps using `http://127.0.0.1:8080/mcp`. On a trusted, isolated OT network you may point the
client directly at the gateway's LAN address instead - understand that the bearer token then travels unencrypted, and
prefer the tunnel when the network is shared, segmented or remote.

## Security & network posture (read this before wiring a token)

- The gateway speaks **plain HTTP** on port `8080` by design and belongs on the **same machine or the same LAN** as
  TIA Portal. **Do not expose that port to the internet** and do not port-forward it from a router.
- Client on another network? Do not open the port. Use an **SSH tunnel**
  (`ssh -L 8080:127.0.0.1:8080 <user>@<gateway-host>`) or a VPN, or terminate **TLS in front** of the gateway and
  point the client at `https://...`.
- The bearer token is a **long-lived credential**: keep it in an environment variable or the client's own config,
  never in the prompt text, never in a commit, never in a screenshot or a shared log. If it leaks, rotate it in the
  gateway console - the old token stops working immediately.
- **Least privilege:** without an activated licence the gateway is read-only; writing, compiling and downloading need
  a licence. Keep the token on a machine that already has TIA Portal/Openness access - do not copy it around.
- **What moves where:** the skill itself uploads nothing to a cloud service - it is a local gateway on your network.
  The conversation is still handled by whichever model vendor your agent uses, so keep project names, paths and
  values out of the prompt unless the task needs them.

> 中文一句话：网关默认明文 HTTP，只用于同机/局域网，别把 8080 映射到公网；跨网用 SSH 隧道或前置 TLS 反代；
> 令牌放环境变量、别贴进对话或提交记录，泄漏就到控制台换掉；未授权时网关只读。

## Safety habits (the short version)

1. Work in a scratch project until the flow is proven; TIA Portal has no undo for a bad download.
2. One block per change; export the old block first so you have a rollback point.
3. Never assume success from the agent's own words - ask for the raw tool output (compile status, downloaded block
   list, read-back values) and compare it against what is on screen.

---

# TiaLink —— 用 MCP 操作博途（TIA Portal）

## 30 秒自检（先确认能不能连，再去读后面的检查清单）

1. **网关在不在跑**（在客户端机器上一条命令）：

   ```bash
   curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/mcp
   ```

   **返回 4xx 也算通**（网络到了、只是缺 token）；`Connection refused` / 超时才是网络问题。
2. **把下面这段贴进你的 MCP 客户端**（WorkBuddy：`~/.workbuddy/mcp.json`）：

```json
{"mcpServers":{"tialink":{"type":"http","url":"http://127.0.0.1:8080/mcp",
  "headers":{"Authorization":"Bearer <你的令牌>"}}}}
```

3. **成功标准**：`list tools` 有返回 → 读一个 scratch 工程 → 建一个块并要编译结果。三步都过，才算装好了。

> 还没装/没授权：https://tia.hubwiz.com/tia-link?utm_source=skillhub&utm_medium=skill （¥99/月，扫码付款后立即给下载与许可步骤）。**未授权时网关只读**，不会改你的工程。令牌在网关控制台配置（包内 `README.txt` §6）。

**它解决的事**：把"AI 给一段 SCL 代码"变成"AI 在博途里把一个块建出来、编译通过、下载到仿真、再读回来核对"。

```
AI 客户端 ──MCP(Streamable HTTP, /mcp + Bearer)──► TiaLink 网关 ──► 博途 Openness ──► 工程
                     （与博途同一台 Windows）           （本机，不出内网）
```

**先说清楚三件事，省掉一半的无效尝试：**

| 是 | 不是 |
|---|---|
| 一个 **MCP 网关**，任何支持 Streamable HTTP + Bearer 的客户端都能用 | ❌ 不是某个 AI 厂商的插件，不绑定 Claude / WorkBuddy / DeepSeek |
| 需要 **本机装了博途 V19 / V20 / V21** | ❌ 不是云端服务，不能"上传 .ap19 帮你改" |
| **未授权也能只读**：连上就能读工程、读块、读硬件树 | ❌ 不替你做安全设计，不碰安全回路 |

---

## 0. 先判断这台机器能不能用（90% 的失败卡在这一步）

在写任何提示词之前，逐条确认。**任一条不满足，后面的步骤一定失败**，别往下走。

> **给智能体的操作约束（省时间、少打扰）**：本技能**不含任何可执行程序**，不要在本机搜索文件、找安装包或翻目录。
> 唯一允许的本地探测是**一次只读 HTTP 请求**到 `http://127.0.0.1:8080/mcp`（`initialize`），
> 返回 401/403/404 也算"网关在跑"；连不上就直接把下面五条检查清单给用户，**不要重试、不要装任何东西**。

| # | 硬条件 | 怎么验（不用装东西） |
|---|---|---|
| 1 | Windows 64 位，**已装且已授权** 博途 **V19 / V20 / V21** | 打开博途 → 帮助 → 关于；版本号必须是 V19.x / V20.x / V21.x |
| 2 | 运行网关的 **Windows 账号在本地 `Siemens TIA Openness` 用户组** | `whoami` 拿到账号 → 计算机管理 → 本地用户和组 → 组 → `Siemens TIA Openness` → 成员里有它。**没有这一条，Openness 一律报授权错误** |
| 3 | 客户端与网关之间 **TCP 端口可达**（示例用 `8080`） | 客户端机器上 `curl -sS -o /dev/null -w "%{http_code}\n" http://127.0.0.1:8080/mcp` —— 返回 **4xx 也算通**（说明网络到了，只是缺 token/路径）；`Connection refused` / 超时才是网络问题 |
| 4 | 客户端支持 **Streamable HTTP 且能发 `Authorization: Bearer`** | 只能跑 stdio 的客户端 → 用第 1 节的 `tialink-mcp` 适配器 |
| 5 | 要仿真才需要 **S7-PLCSIM Advanced**（已装已授权，且有一个运行中的虚拟实例） | 只做读/建块/编译，第 5 条可以不满足 |

> 现场网络没有外网？这正是设计场景：网关和客户端放同一网段，**不要**把端口映射到公网。

---

## 1. 连接（三选一，都只要一份配置）

### 1.1 客户端支持 HTTP（推荐）

```json
{
  "mcpServers": {
    "tialink": {
      "type": "http",
      "url": "http://127.0.0.1:8080/mcp",
      "headers": { "Authorization": "Bearer <你的令牌>" }
    }
  }
}
```

- 地址**必须以 `/mcp` 结尾**，不是 `http://host:8080`。
- 网关和客户端同机就写 `127.0.0.1`；跨机写那台机器的局域网 IP。
- WorkBuddy：写进 `~/.workbuddy/mcp.json`（用户级）或 `<项目>/.workbuddy/mcp.json`（项目级），或用「插件 → MCP 服务器 → 配置 MCP」粘贴。
- 令牌别进 git：客户端支持环境变量就用 `${TIALINK_API_TOKEN}` 这类写法。

### 1.2 客户端只支持 stdio

```bash
TIALINK_URL=http://127.0.0.1:8080/mcp TIALINK_TOKEN=<你的令牌> npx tialink-mcp
```

```json
{
  "mcpServers": {
    "tialink": {
      "command": "npx",
      "args": ["-y", "tialink-mcp"],
      "env": { "TIALINK_URL": "http://127.0.0.1:8080/mcp", "TIALINK_TOKEN": "<你的令牌>" }
    }
  }
}
```

适配器只是 stdio ↔ HTTP 的转发，**不解锁任何能力**；网关没装/没授权，它第一步就失败，这是预期行为。

### 1.3 冒烟测试（连不上时先跑这个，别猜）

```bash
# 有 Node：一条命令出「服务器名 + 协议版本 + 工具列表」
TIALINK_URL=http://127.0.0.1:8080/mcp TIALINK_TOKEN=<你的令牌> npx tialink-mcp --check
```

```bash
# 没有 Node：curl 也行
curl -sS -X POST "http://127.0.0.1:8080/mcp" \
  -H "Authorization: Bearer <你的令牌>" \
  -H "Content-Type: application/json" \
  -H "Accept: application/json, text/event-stream" \
  -d '{"jsonrpc":"2.0","id":1,"method":"initialize","params":{"protocolVersion":"2025-06-18","capabilities":{},"clientInfo":{"name":"smoke","version":"1.0"}}}'
```

| 返回 | 含义 | 下一步 |
|---|---|---|
| JSON-RPC result 里有 `serverInfo` | 通了 | 继续第 2 节 |
| `401` / `403` | 令牌缺失或写错（含尾部换行） | 重新复制令牌，确认是 `Bearer <token>` |
| `404` | 路径不对 | 补 `/mcp` |
| `406 Not Acceptable` | `Accept` 少了 `text/event-stream` | 按上面的 curl 原样发 |
| 连接被拒 / 超时 | 网关没起、只绑了 `localhost`、或防火墙挡了 | 查网关主机防火墙与监听地址 |

---

## 2. 首次会话的固定语序（照抄，别跳）

**核心原则：先读 → 再预演 → 再写 → 必编译 → 必读回。**
"AI 说改好了"不是证据，**编译输出和读回结果才是**。

```text
第一步，只读热身（不发任何写操作）：
1) 连上 TiaLink，列出你能用的工具，按「设备/模块、子网与 IO 系统、块与 SCL 导入、编译、HMI、仿真」分组报给我；
2) 打开工程 <工程名>，报设备清单和块清单（名字 + 类型 + 编号），只读；
3) 告诉我这个工程用的是哪个 TIA 版本、有没有 PLCSIM 实例在线。
确认以上三项都成功，再等我下一步指令。
```

验收物：设备清单 + 块清单 + 版本 + 仿真可用性。**四项缺一，不要进入写操作。**

```text
第二步，一个小写入闭环（用来验证链路，不做业务）：
新建一个 FC 名为 FB_Smoke，语言 SCL，内容只有一句注释和一条赋值；
编译它，把编译结果的原文贴出来；
然后把它的接口读回来贴给我。
任何一步失败就停下，把错误原文给我，不要重试超过一次。
```

写操作只在**临时/草稿工程**里做第一次。**不要拿产线工程练手。**

---

## 3. 四条常用工作流（动作序列 + 验收物）

### 3.1 机架与硬件组态

| 步骤 | 动作 | 验收物 |
|---|---|---|
| 1 | 读硬件树，确认目标设备名与现有槽位 | 槽位表（槽号 / 型号 / 订货号） |
| 2 | 在硬件目录里**搜索**型号（"CPU 1511-1 PN"、"DI 16x24VDC"），列出候选（含固件版本） | 候选清单，**不许凭记忆写订货号** |
| 3 | 预演：确认设备名、类型、分组不冲突 | 预演结果 |
| 4 | 创建 CPU（此时才有机架和 PLC 软件） | 新设备 + 机架 |
| 5 | 按槽位插入模块 | 逐槽插入结果 |
| 6 | 分配 IP / 子网 / IO 系统 | 网络视图摘要 |
| 7 | 编译硬件 + 读回硬件树 | 编译输出 + 读回的槽位表（与第 1 步对照） |

**CPU 单独一段提示词**：它和槽位模块不是一类东西，且选错等于整台设备重建。

### 3.2 建块与写 SCL

1. 读块清单（避免重名/重复编号）→ 2. 建 FB/FC/DB/UDT（先定接口）→ 3. 写 SCL（或导入 SimaticML，含 LAD）→
4. **编译** → 5. 读回接口与调用关系 → 6. 报改动清单。

提示词模板：

```text
在工程 <名> 里新建一个 FB：FB_MotorCtrl，SCL。
接口：输入 Start/Stop/Feedback（Bool）、Reset（Bool）；输出 Run/Fault（Bool）；静态 Running/Timer（TON）。
逻辑：起保停 + 反馈超时 5s 报 Fault；Reset 复位。
要求：
- 只从工具返回的编译输出判断成功，不许推测；
- 编译通过后读回接口，按「名称/方向/类型」三列贴给我；
- 列出你实际执行了哪几个工具调用（名字 + 关键参数），我要能复现。
```

### 3.3 仿真与下载（默认只下仿真）

1. 确认 PLCSIM Advanced 有运行中的虚拟实例（PC/PG 接口选对虚拟网卡）→ 2. 编译 → 3. 下载到虚拟 CPU →
4. 写测试变量 → 5. 读结果 → 6. 报「输入 → 期望 → 实测」三列表。

硬件下发（真机）**必须人工逐步确认**，且先确认停机窗口。

### 3.4 导出与归档

编译 → 保存 → 导出块/工程 → 归档 → 读回归档产物路径与大小。
用途：交付前留档、版本对比、"改了什么"取证。

---

## 4. 失败判读（对照着看，别重启乱试）

| 现象 | 最可能的原因 | 处理 |
|---|---|---|
| 连不上 / 超时 | 防火墙、只绑 `localhost`、端口错 | 网关主机放行端口；客户端改用局域网 IP |
| `401/403` | 令牌错/多空格/尾换行 | 重新复制；只在 header 里放 `Bearer <token>` |
| `404` | 路径不是 `/mcp` | 补全路径 |
| 连上了但工具列表是空的 | 客户端缓存了旧列表 | 重启客户端；确认支持 Streamable HTTP |
| Openness 报授权 / "not permitted" | 账号不在 `Siemens TIA Openness` 组 | 加入组 → **注销重登**（组权限要重开会话才生效） |
| 报版本相关错误 | 网关与博途版本不匹配 | 确认是 V19 / V20 / V21（V21 需 TiaLink 1.5.0+） |
| 仿真/下载类工具失败 | PLCSIM Advanced 未装、未起、无虚拟实例、PC/PG 接口选错 | 起实例 → 选虚拟网卡 → 重试 |
| 编译/下载调用超时 | 默认超时 600s，编译慢是正常的 | **不要**把超时降到聊天级别；等 |
| 重启后全挂 | 网关没注册成服务，博途未就绪 | 先起博途，再起网关 |

报问题时请带上：Windows 版本、博途版本、客户端名与版本、**错误原文**（不是聊天窗口截图）。

---

## 5. 安全边界（红线，不能"灵活处理"）

- **默认只下仿真**（S7-PLCSIM）。要下真机，必须操作员明确确认目标与停机窗口。
- **不碰生产工程、不碰运行中的设备**，除非人在环里逐步确认。
- **安全功能不进 AI 生成物**：急停/安全门/光幕由安全继电器或安全 PLC 实现；硬联锁用气动或电气；时间和传感器标定必须在真机上做。
- 网关主机按**工程基础设施**对待：最小权限账号、只在需要的网段监听、端口不外映射。
- 每次写入后都要**读回 + 编译**；没有编译输出的"已完成"一律不认。

---

## 6. 网关从哪来、怎么授权

| 项 | 说明 |
|---|---|
| 获取 | 付费软件，博途同机安装：https://tia.hubwiz.com/tia-link?utm_source=skillhub&utm_medium=skill （微信支付后页面直接给下载链接与安装步骤） |
| 价格 | ¥99/月 或 ¥999/年（中国区）；多席位 / 浮动 / 内网隔离部署另议：support@hubwiz.com |
| 未授权 | **只读可用**：能连、能读工程、能读块和硬件树；写入类操作需要授权 |
| 授权 | 打开 `http://localhost:8080/` → **机器码** + 下载 **`.tlreq`** 请求文件 → 连同订单号发 support@hubwiz.com → 回传与机器绑定的 `.lic`，完全离线有效 |
| 安装要点 | 先拷到最终目录（如 `C:\Program Files\TiaLink\`）再运行（Openness 白名单按路径+哈希登记）；跑一次 `TiaLink.Helper.exe` 一键修复；**以普通用户启动 `TiaLink.exe`，绝不要用管理员** |
| stdio 适配器 / 桌面包 | `npx tialink-mcp`（MIT）、`.mcpb` 桌面包、Docker 镜像，见 https://github.com/tia-forge/tialink |

> 该技能本身是**知识包**（CC BY 4.0），不含网关程序、不含授权；网关是商业软件，二者分开。

---

## 配套技能（同一套 TIA Forge 工作流）

这五个技能是一条链：**查文档 → 生成块 → 看图核对 → 跑验证 → 落地工程**。单独装一个能用，装齐才闭环。

| 技能 | 安装坐标 | 什么时候需要它 |
|---|---|---|
| 博途编程文档检索 | `@indiv-tiaforge/tia-portal-docs` | 不确定指令参数、引脚含义、版本行为 |
| LadDoc Cloud | `@indiv-tiaforge/laddoc-cloud` | 要把 LadDoc 生成成博途可导入的块 |
| 梯形图渲染 | `@indiv-tiaforge/lad-render-cloud` | 把 SimaticML 渲染成 PNG，导入前先看一眼 |
| PLC 云仿真 | `@indiv-tiaforge/plc-cloud-sim` | 生成后跑 PASS/FAIL、回归、边界用例 |
| TiaLink **← 你在这里** | `@indiv-tiaforge/tialink-tia-portal` | 在真实工程里编译、下载、读回 |

装齐的方式：把下面这句发给你正在用的 AI 助手（逐个发即可）：

```text
请根据 https://skillhub.cn/install/skillhub.md，安装 @indiv-tiaforge/<slug>
```

## 7. 三条常见误会

1. **"TiaLink 是 WorkBuddy 的插件？"** 不是。TiaLink 是汇智网（hubwiz.com）的产品，WorkBuddy / Claude / Cursor / DSH 都只是**调用方**。
2. **"装了技能就能改工程？"** 技能只教怎么用；真正干活的是网关进程 + 授权。
3. **"能不能离线？"** 能。网关与博途都在内网，MCP 走局域网，**工程数据不出内网**。

---

*TiaLink 与 Siemens AG 无关。TIA Portal、SIMATIC、S7、PLCSIM 是 Siemens AG 的商标。文档许可 CC BY 4.0；网关软件为商业软件，版权保留。*
