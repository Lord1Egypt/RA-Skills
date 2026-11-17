# 搭子路书（Trek）微信旅行小程序 × Agent 自动化

让旅行计划不只停留在聊天记录里。Trek 把微信小程序作为用户可见、可编辑、
可协作的行程中心，用户只要复制一次并发给 WorkBuddy，它就能研究资料、
制定计划，并把结构化结果同步回小程序。Codex、Claude、OpenClaw、Hermes
等支持 MCP 或命令行的 Agent 也兼容同一套接入方式。

[![Verify and publish](https://github.com/super21-bat/trek-agent-control/actions/workflows/release.yml/badge.svg)](https://github.com/super21-bat/trek-agent-control/actions/workflows/release.yml)

<p align="center">
  <img src="assets/trek-miniapp-code.png" alt="微信扫码打开 Trek 旅行小程序" width="240" />
</p>

<p align="center">
  <strong>微信扫码打开 Trek 旅行小程序</strong><br />
  <sub>当前为测试阶段，是否可直接进入以微信侧体验权限为准。</sub>
</p>

## 小程序和 Agent 如何配合

```text
微信小程序创建行程与 Agent Key
            ↓
Agent 搜寻攻略、交通、餐饮和预订信息
            ↓
通过 Trek MCP 写入日程、地点、费用、票据与清单
            ↓
用户在小程序查看、修改、导航、分享和共同协作
```

小程序是行程的可视化工作区和最终数据来源；本仓库提供的是自动化接入层，
不是另一套旅行应用，也不会把用户数据保存到 GitHub。每个 Agent 使用独立、
可撤销的 Key，用户可以在微信端停止连接。

## 在小程序里可以做什么

- 查看首页下一站、当天时间线和地图导航。
- 编排国内或海外多日行程，维护地点、交通方式和当次安排。
- 保存酒店、机票、门票等预订信息、确认号、二维码、图片和 PDF。
- 管理费用、出发清单、待办事项和行程状态。
- 邀请同行者共同查看和修改行程。
- 为不同 Agent 创建独立连接，随时撤销不再使用的 Key。

## Agent 可以自动完成什么

- 结合用户时间、同行人、预算和已确认预订研究可执行的旅行方案。
- 读取、新建和更新行程、逐日日程、地点、交通与时间。
- 管理住宿、航班、门票、餐厅预订及关联附件。
- 写入费用、清单、待办、成员和协作提案。
- 写入后自动回读，核对计划是否真正出现在小程序对应位置。
- 使用 `doctor` 检查配置、网络、鉴权、工具发现与读取能力。

## 两步连接 WorkBuddy

1. 在 Trek 小程序“我的”页面点“创建并复制”。
2. 打开 WorkBuddy，把复制内容直接发给它。

安装、配置、Skill 同步和连接检查都由 WorkBuddy 完成，普通用户不需要理解
MCP、CLI 或 `doctor`。

## 其他兼容 Agent

- **原生支持 Streamable HTTP MCP**：直接配置 MCP URL 和 Bearer Key。
- **支持终端但不支持远程 MCP**：安装零依赖 Node.js CLI。
- **Codex / Claude / OpenClaw / Hermes**：使用同一个复制接入包；支持原生 MCP 时直接连接，否则使用 CLI。

Hermes 用户执行 `trek skill sync --global` 后，CLI 会在 Hermes 的可信目录
安装实体 Skill 副本；请重启 Hermes gateway 或开启新会话。Hermes 原生 MCP
扩展不是必需项，未安装时直接使用 `trek` CLI 即可，不要让 Trek 安装脚本
擅自修改 Hermes 的 Python 环境。

仓库中不包含任何用户 Key、行程数据、小程序源码或服务端凭据。

## 快速开始

先在 Trek 小程序的「我的 → Agent 连接」创建连接并复制配置。要求
Node.js 18 或更高版本：

```bash
npm install -g https://github.com/super21-bat/trek-agent-control/archive/refs/heads/main.tar.gz
trek config init --api-key '由用户单独提供' --url 'https://api.superd.fun/mcp'
trek skill sync --global
trek doctor
```

最小只读验证：

```bash
trek call list_trips '{"include_archived":false}'
```

原生 MCP 配置：

```text
URL: https://api.superd.fun/mcp
Authorization: Bearer <用户自己的 Trek Agent Key>
```

不要把真实 Key 写入 Git、聊天记录、截图、共享日志或公共配置示例。

## Agent 执行原则

1. 先读取现有行程，再研究和生成计划。
2. 写入前展示变更预览，避免覆盖真实数据。
3. 一条可见日程必须是 Place + Assignment，不能只写在备注里。
4. 地点介绍、电话、官网属于 Place；当次时间和说明属于 Assignment。
5. 订单号和票据属于 Reservation/File；金额属于 Budget/Expense。
6. 每次写入后使用 list/get 工具回读，并核对小程序可见位置。
7. 不猜工具名或字段；服务端变化后先调用 `tools/list`。

## 常用命令

```bash
trek doctor
trek tools place
trek summary 3
trek audit-plan 3 /absolute/path/expected-assignments.json
trek upload-file 3 /absolute/path/ticket.pdf --assignment 42
trek set-cover 3 /absolute/path/cover.jpg
trek add-pending 3 '西湖游船' --place-id 88 --reason '同行者表态后再排日程'
trek batch /absolute/path/actions.json
trek batch /absolute/path/actions.json --apply
```

`batch` 默认只预览；高风险操作需要额外确认。新增日程时可直接在 `create_and_assign_place`（已有地点用 `assign_place_to_day`）中传 `place_time` 和 `end_time`，单条动作即可保存当天时间，无需先取 assignmentId 再拆第二批。生产诊断默认只读。
`doctor` 会在线完成 MCP 初始化、工具发现和 `list_trips` 回读，因此也能识别
已撤销或无效的 Key；输出只显示 `configured`，不会暴露 Key 的任何片段。

## 文档

| 文档 | 用途 |
| --- | --- |
| [SKILL.md](SKILL.md) | Agent 必须遵守的执行流程与安全边界 |
| [字段指南](references/field-guide.md) | MCP 字段归属、写入工具和小程序可见位置 |
| [工作流](references/workflows.md) | 研究、规划、同步、回读与审计 |
| [配置指南](references/configuration.md) | 各 Agent 的 MCP/CLI 接入与排障 |
| [维护说明](MAINTAINING.md) | Git、测试、版本、ClawHub 发布与回滚 |

## 发布状态

- GitHub 是 CLI 和 Skill 的发行源。
- ClawHub 是 OpenClaw Skill 目录，审核完成后提供独立安装入口。
- npm 正式包为 `@trek-cn/cli`；GitHub 安装方式仍可使用。
- GitHub、ClawHub、npm 三者的“已发布”状态必须分别验证。

## 开源与致谢

Trek 中国版复用并扩展开源项目
[liketrek/TREK](https://github.com/liketrek/TREK) 的旅行管理与 MCP 能力，
面向微信小程序、中国大陆服务和国内外行程场景进行了适配。

GitHub 仓库内容按 [AGPL-3.0](LICENSE) 发布。发布到 ClawHub 的 Skill 副本
遵循 ClawHub 平台规定的 MIT-0。

## 每日提醒与备注（CLI 0.3.3 / 小程序 0.3.24+）

```bash
trek set-day-brief TRIP_ID DAY_ID @brief.txt
trek day-view TRIP_ID DAY_ID
trek audit-notes TRIP_ID expected-notes.json
```

今日提醒可写穿搭和出门物品，建议精简并用真实换行分开事项；0.3.24 起按行显示，字段是纯文本，不解析 Markdown。提醒为空即隐藏。天气按当天日期和已定位的安排自动查询：前9天使用MET Norway真实预报，延长预报到第15天，之后显示明确标注的历史气温预估，按天缓存。当天信息折叠区只包含提醒和备注；两者可在小程序原位增删改。实际地点仍使用assignment。`day-view`返回展示契约，不证明手机已安装最新版；`audit-plan`只核对assignment，备注请用`audit-notes`。

## 跨零点升级（CLI0.3.5 / 小程序0.3.36 / schema184）

凌晨接机仍归属出发当天，显示“次日01:00”，按实际日期排序；首页下一站与ICS同步识别真实时间。出发/抵达时区独立处理，连接地址和Key不变，旧数据不自动改写。详见[跨零点字段与示例](references/cross-midnight.md)。

## 到达方式升级（CLI0.3.4 / 小程序0.3.35 / schema183）

每次安排独立保存到达方式；Agent根据实际动线合理推断，用户手动修改优先，不再创建后全部变步行。读[完整字段与示例](references/arrival-mode.md)。先升级服务器，再更新小程序和Agent技能；旧真实行程不自动批量改写。旧客户端可读取，不代表能编辑新字段。
