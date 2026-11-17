---
name: "TencentDB PostgreSQL Skill"
description: "Bundle entry for TencentDB PostgreSQL skills. It organizes five scenarios: one natural-language management-plane router, two extension-service scenarios for mem0 and REST, and two operations-plane scenarios for PG inspection and slow SQL lookup. The mem0 scenario focuses on one-sentence service deployment, while the REST scenario covers open or close requests, safe read-only invocation, and 502-style troubleshooting when runtime prerequisites are satisfied. Ambiguous targets and high-risk changes still remain guarded by repository safety rules."
description_zh: "TencentDB PostgreSQL Skill"
description_en: "TencentDB PostgreSQL Skill"
version: 1.0.3
---

# TencentDB PostgreSQL Skill

## 简介

TencentDB PostgreSQL Skill 是面向腾讯云数据库 PostgreSQL 的统一入口，用于把管理、扩展服务和运维观察类请求路由到对应子场景，并在统一的安全边界内返回结构化结果。具体覆盖范围、典型请求和输出结果，请直接查看下一节。

## 覆盖的 5 个场景

| 场景目录 | 能力名称 | 适合处理的问题 | 典型请求 | 输出结果 | 入口 |
|---|---|---|---|---|---|
| `tencent-pg-management` | 管控面统一入口 | 实例状态查看、实例变更准备、备份恢复管理、访问安全治理 | `查看实例状态并评估是否适合升级规格`、`帮我看恢复时间窗`、`检查账号权限和 SSL 配置` | `目标范围`、`识别意图`、`当前事实`、`动作状态`、`安全下一步` | `references/tencent-pg-management/SKILL.md` |
| `tencent-pg-mem0-deploy` | mem0 一句话部署 | 目标实例识别、mem0 只读预检查、一键开通、状态轮询直到可用 | `帮我给广州 postgres-abc12345 开通 mem0`、`给当前实例一键部署 mem0，AgenticBaseId 用 ab-xxxxx` | `实例信息`、`进行的操作`、`TaskId`、`耗时`、`执行结果` | `references/tencent-pg-mem0-deploy/SKILL.md` |
| `tencent-pg-rest-deploy` | REST 一句话开通 / 调用 / 排障 | 目标实例识别、REST 只读预检查、只读路径调用、502 排障取证、地域不支持时返回候选地域、一键开通或关闭、状态轮询直到可用 | `帮我给广州 postgres-abc12345 开通 REST 服务`、`帮我调用这个实例的 REST 路径 /`、`帮我排查 ap-qingyuan postgres-abc12345 的 REST 502` | `地域`、`识别 lane / 请求动作`、`预检事实`、`TaskId / HTTP 状态`、`最终状态 / 返回摘要` | `references/tencent-pg-rest-deploy/SKILL.md` |
| `tencent-pg-inspection` | 运维面 PG 巡检 | 日常健康检查、基础资源巡检、固定指标核对 | `PG巡检`、`健康检查`、`资源巡检`、`监控巡检` | `执行摘要`、`检查目标`、`健康快照`、`指标明细`、`风险复核`、`数据说明` | `references/tencent-pg-inspection/SKILL.md` |
| `tencent-pg-slowquery-diagnosis` | 运维面慢 SQL 查询 | 慢 SQL 列表查看、时间窗口查询、Top SQL 核对 | `慢SQL查询`、`慢SQL分析`、`查看慢查询` | `查询范围`、`筛选条件`、`排序依据`、`基础列表`、`缺失字段说明` | `references/tencent-pg-slowquery-diagnosis/SKILL.md` |

## 使用前准备

### 1. 获取腾讯云 API 凭证

- 打开 API 密钥控制台：[腾讯云 API 密钥管理](https://console.cloud.tencent.com/cam/capi)
- 如无可用密钥，点击 `新建密钥` / `创建密钥`
- 推荐使用 **最小权限 CAM 子账号**，不要长期复用高权限主账号密钥
- 创建后立即保存 `SecretId` 与 `SecretKey`
  - `SecretId` 可后续查看
  - `SecretKey` 一般只在创建时完整展示一次，丢失后需要重新创建并轮换旧密钥
- 再打开 [PostgreSQL 控制台](https://console.cloud.tencent.com/postgres) 确认目标地域，例如 `ap-guangzhou`

### 2. 运行时环境

必须使用这些标准变量名：

- `TENCENTCLOUD_SECRET_ID`
- `TENCENTCLOUD_SECRET_KEY`
- `TENCENTCLOUD_REGION`
- 可选：临时凭证场景补充 `TENCENTCLOUD_SESSION_TOKEN`

无论你用哪种客户端，都要保证**真正触发 skill 的宿主进程**能读到这组变量；如果宿主已有自定义变量名，请先映射到这些标准名称。地域既可以直接写 `ap-guangzhou`，也可以先写 `广州`、`上海`、`成都`、`北京`。密钥只应存在于运行时环境，不应写入代码、仓库文件、URL、查询参数或聊天记录。

#### 先判断你的使用方式

| 你当前怎么用 | 常见客户端 / 场景 | 推荐方式 |
|---|---|---|
| 在终端直接启动宿主进程、CLI、本地调试命令 | `node`、`npm run ...`、本地脚本 | 方式 A |
| macOS 图形客户端，从图标或 Finder / Dock 启动 | `WorkBuddy`、`CodeBuddy`、`Claude Desktop`、`Cherry Studio`、`Chatbox` 等 | 方式 B |
| IDE / 编辑器类客户端 | `Cursor`、`VS Code`、`Windsurf`、`Trae` 等 | 集成终端启动用方式 A；IDE 主进程读取变量时按启动方式选择方式 B 或方式 D |
| Windows 桌面客户端 | Windows 上的桌面 AI 客户端、IDE、Electron App | 方式 D |

#### 方式 A：CLI / 命令行启动

适合你准备**从命令行直接启动宿主进程、CLI 或本地调试命令**的场景。

1. 在你接下来要执行启动命令的终端里，先运行：

```bash
export TENCENTCLOUD_SECRET_ID="你的 SecretId"
export TENCENTCLOUD_SECRET_KEY="你的 SecretKey"
export TENCENTCLOUD_REGION="ap-guangzhou"
# 临时凭证场景再补：
export TENCENTCLOUD_SESSION_TOKEN="你的 SessionToken"
```

2. 紧接着验证：

```bash
echo $TENCENTCLOUD_SECRET_ID
echo $TENCENTCLOUD_REGION
```

3. 验证通过后，在**同一个终端窗口**里继续执行你的启动命令。
4. 如果你希望以后新开的终端也自动带上这些变量，可以把同样的 `export` 追加到 `~/.zshrc` 或 `~/.bashrc`，保存后执行 `source ~/.zshrc` 或重新打开终端。

#### 方式 B：macOS 图形客户端（WorkBuddy / CodeBuddy / Claude Desktop / Cherry Studio / Chatbox 等）

适合你通过 macOS 桌面客户端使用这些 skill，而不是从 CLI 直接启动。

1. 打开终端，执行：

```bash
launchctl setenv TENCENTCLOUD_SECRET_ID "你的 SecretId"
launchctl setenv TENCENTCLOUD_SECRET_KEY "你的 SecretKey"
launchctl setenv TENCENTCLOUD_REGION "ap-guangzhou"
# 临时凭证场景再补：
launchctl setenv TENCENTCLOUD_SESSION_TOKEN "你的 SessionToken"
```

2. 执行下面命令验证是否已经写入当前登录会话环境：

```bash
launchctl getenv TENCENTCLOUD_SECRET_ID
launchctl getenv TENCENTCLOUD_REGION
```

3. **完全退出** 客户端后再重新打开。
4. 重新进入 skill，再继续你的操作。

> 如果客户端是从图标启动，单独在某个终端里执行一次 `export`，通常不会自动传给这个桌面客户端进程；`launchctl setenv` 更适合作为 macOS 图形客户端的配置方式。

#### 方式 C：IDE / 编辑器客户端（Cursor / VS Code / Windsurf / Trae 等）

先分清楚：**到底是 IDE 自己触发 skill，还是你在 IDE 集成终端里启动宿主进程**。

- 如果你是在 IDE 集成终端里自己启动命令，本质上仍然是 **方式 A**。
- 如果你希望 IDE 主进程及其插件也能读到变量，就要把变量配置给 **启动 IDE 的那个进程**。

例如，从终端启动 IDE 时可以这样做：

```bash
export TENCENTCLOUD_SECRET_ID="你的 SecretId"
export TENCENTCLOUD_SECRET_KEY="你的 SecretKey"
export TENCENTCLOUD_REGION="ap-guangzhou"

# 按你实际使用的客户端选择其一
cursor .
# code .
# windsurf .
# trae .
```

如果客户端平时是从 Dock / Finder / 桌面图标启动的，那么 macOS 回到 **方式 B**，Windows 回到 **方式 D**。

#### 方式 D：Windows 客户端

适合你在 Windows 上使用桌面客户端、IDE 或自定义宿主。

##### 方案 1：写入用户级环境变量

在 PowerShell 中执行：

```powershell
setx TENCENTCLOUD_SECRET_ID "你的 SecretId"
setx TENCENTCLOUD_SECRET_KEY "你的 SecretKey"
setx TENCENTCLOUD_REGION "ap-guangzhou"
```

执行后关闭并重新打开你的终端 / 客户端，再验证：

```powershell
echo $env:TENCENTCLOUD_SECRET_ID
echo $env:TENCENTCLOUD_REGION
```

##### 方案 2：只给当前会话临时注入

```powershell
$env:TENCENTCLOUD_SECRET_ID = "你的 SecretId"
$env:TENCENTCLOUD_SECRET_KEY = "你的 SecretKey"
$env:TENCENTCLOUD_REGION = "ap-guangzhou"
$env:TENCENTCLOUD_SESSION_TOKEN = "你的 SessionToken"
```

这种方式更适合临时调试或短期会话。

#### 其他宿主说明

对于 Docker、CI、自建宿主或宿主已有自定义变量名的场景，当前不再单列独立方式。

统一只遵循一个原则：**在真正启动宿主进程前，把标准 `TENCENTCLOUD_*` 变量注入到实际触发 skill 的进程环境中**。如果你内部已经有其他变量名，也请先在启动链路里映射到标准变量，再继续启动客户端或宿主。

#### 常见误区

- **误区 1**：在一个终端里 `export` 过，桌面客户端就一定能读到。很多从图标启动的 GUI 客户端并不会继承那个终端里的环境。
- **误区 2**：把 `SecretKey` 直接写进客户端配置文件或仓库。更安全的做法是通过系统环境变量、平台 Secret 或运行时注入来提供。
- **误区 3**：`setx` 或 `launchctl setenv` 配完后不重启客户端。很多客户端只有在重新启动后才会重新读取环境。
- **误区 4**：把临时 `SessionToken` 当成长期凭证。临时凭证会过期，过期后需要重新注入。

## 使用方法

1. **确认目标范围**：至少准备好地域和实例 ID；如果是 mem0 开通，最好额外准备 `AgenticBaseId` 或对应运行时默认值。
2. **选择匹配的场景入口**：管控面任务进入 `tencent-pg-management`，mem0 开通或关闭进入 `tencent-pg-mem0-deploy`，REST 开通、关闭、只读调用或 502 排障进入 `tencent-pg-rest-deploy`，运维面巡检进入 `tencent-pg-inspection`，运维面慢 SQL 查询进入 `tencent-pg-slowquery-diagnosis`。
3. **发起请求**：建议在请求里明确地域、实例 ID、任务目标，以及可选的时间范围、部署参数、REST 路径、查询字符串或受影响对象。
4. **查看结果**：先阅读当前状态、HTTP 返回或排障结论，再决定是否需要进一步操作。

推荐输入格式示例：

```text
ap-guangzhou postgres-abc12345

请检查这个实例当前状态，并评估是否适合升级规格
请帮我确认最近 24 小时的备份和恢复时间窗
请帮我给这个实例开通 mem0，AgenticBaseId 用 ab-xxxxx
请帮我给这个实例开通 REST 服务
请帮我调用这个实例的 REST 路径 /
请帮我排查 ap-qingyuan postgres-abc12345 的 REST 502
请做一次 PG 巡检
请查询最近 1 小时慢 SQL
```

## 安全与边界

- 默认应以 **只读结果返回** 为先，不直接执行会影响实例状态的动作。
- 任何 **写类、费用类或高风险动作** 都必须先说明影响面并获得明确确认。
- REST 场景下，默认通过 **EnableWanNet=false** 开通 REST 服务，也就是服务可开但**公网 / 外网访问默认保持关闭**；如需代用户打开公网访问，必须先明确告知安全风险并等待用户二次确认。
- 两个运维面场景当前以报告式基础事实返回结果，不做复杂扩查、排障或根因分析。

## 目录与扩展说明

- 根目录入口：`SKILL.md`
- 根目录元数据：`_meta.json`
- 公共规则目录：`references/common/`
- 子技能目录：`references/<skill-name>/`
- 子技能入口：`references/<skill-name>/SKILL.md`
