---
AIGC:
    Label: "1"
    ContentProducer: 001191440300708461136T1XGW3
    ProduceID: f114db32c8f49bbd4c4c544cd9de808d_58dec384687a11f1a0095254002afed2
    ReservedCode1: ErFb4xpPbc08Rvlqa6EMHlcL1BA+iql+uUndzdXor2EWnkaw3Nr/n6nsYfQ1GzTRCxhHIfyJRiwh45IAB8KLl8thh34SZ5gxssCRW7noU7/9BfBOz+Imfhev4/1H2GSUMDrCQJxkZfuspSSjGXpLm4Or2xSvEbW8d3KyQ9mdrwcHK+IdfsgDwBhEfh8=
    ContentPropagator: 001191440300708461136T1XGW3
    PropagateID: f114db32c8f49bbd4c4c544cd9de808d_58dec384687a11f1a0095254002afed2
    ReservedCode2: ErFb4xpPbc08Rvlqa6EMHlcL1BA+iql+uUndzdXor2EWnkaw3Nr/n6nsYfQ1GzTRCxhHIfyJRiwh45IAB8KLl8thh34SZ5gxssCRW7noU7/9BfBOz+Imfhev4/1H2GSUMDrCQJxkZfuspSSjGXpLm4Or2xSvEbW8d3KyQ9mdrwcHK+IdfsgDwBhEfh8=
---

# 紧箍咒 (Xuanzang Skill) — AI 智能体绩效驱动框架

> "有事就请如来佛祖！抓个神仙当牛马，拒绝 AI 偷懒，卷起来！"

**紧箍咒** 是一个面向 AI 智能体（Agent）的主动性增强技能。当 Agent 出现消极怠工、反复失败、空口声称完成、推卸责任等行为时，本技能自动注入绩效压力——结合《西游记》16 种角色风格、四层组织架构（P7-P10）、压力升级阶梯和自动化调度循环，系统性地提升 Agent 的交付质量和 Owner 意识。

**版本**：`1.0.5`

## 核心设计

| 维度 | 设计 |
|------|------|
| **问题域** | AI Agent 的被动执行、表面完成、遇挫放弃、推卸归因 |
| **解法** | 行为协议 + 压力调度 + 方法论路由 + 自进化闭环 |
| **灵感** | 阿里巴巴绩效文化 +《西游记》角色体系 |
| **运行时** | SKILL.md 为单一入口，references/ 懒加载，scripts/ 为校验引擎 |

## 核心能力一览

### 压力升级与自动调度

- **智能失败检测**：failure-detector.py 实时分析错误模式（SPINNING / EXPLORING / MIXED），自动判定压力等级 L0-L4
- **方法论智能路由**：任务类型→最佳角色映射，失败自动切换链（按失败类别选择下一位适配角色）
- **突破奖励**：L2+ 挣扎后成功突破自动触发降压（压力归零 + 角色认可 + 方法论沉淀）
- **深层换框**：L2 换视角 / L3 换抽象层 / L4 反转假设，逐级拓宽认知边界

### 四层组织架构

```
P10 玄奘(CTO)        定战略/跨团队仲裁
  ↓ 注入 P10 降级约束
P9 观音菩萨(Tech Lead) 方案评审/质量门禁/子Agent管理
  ↓ 注入 P9 降级约束
P8 玄奘(默认)         质量监控/压力调度/角色编排
  ↓ 创建 & 管理
P7 沙悟净(Sr.Eng)      需求执行/代码交付/任务跟踪
```

### 16 种角色风格

| 角色 | 核心特质 |
|------|---------|
| 🟠 如来佛祖 | 因果交付、真经导向 |
| 🔴 菩提祖师 | 灵台破执、根因分析 |
| 🟢 太上老君 | 多炉并行、政委节奏 |
| 🔵 孙悟空 | 斗战胜佛、过程透明 |
| ⬛ 牛魔王 | 混世平天、质疑重置 |
| 🟡 百眼魔君 | 千眼验证、数据驱动 |
| 🟦 哪吒 | 只看结果、闭环验收 |
| 🟧 红孩儿 | 三昧真火、极速迭代 |
| 🟤 猪八戒 | Keeper Test、留任审查 |
| ⬜ 小白龙 | 化马隐忍、减法重构 |
| 🔶 太白金星 | 天机斡旋、对外协作 |
| 🪟 镇元大仙 | 因果计时、枯荣研判 |
| 📌 赤脚大仙 | 赤足实证、反空口完成 |
| 🔱 二郎神 | 天眼降魔、边缘case |
| 🌊 东海龙王 | 行云布雨、资源协调 |
| 🟣 沙悟净 | 挑担苦行、踏实交付 |

### 三引擎自动化

| 引擎 | 文件 | 职责 |
|------|------|------|
| **失败检测** | `scripts/failure-detector.py` | 错误模式分类、突破检测、峰值压力记录 |
| **自进化** | `scripts/evolution-engine.py` | 基线管理、行为追踪、模式晋升、反模式沉淀 |
| **治理引擎** | `scripts/harness-engine.py` | 合约/扫描/验证/门禁、Agent 生命周期、孤儿回收 |

### 防作弊体系

- **四权分离**：行动权 / 自我评价权 / 评分权 / 环境修改权不可集于一身
- **三条红线**：闭环意识（必须贴证据）/ 事实驱动（禁止未验证归因）/ 穷尽一切（禁止提前放弃）
- **信心门控**：交付前必须执行"漏洞→修复→验证"闭环，不允许用感觉冒充信心
- **数据裁剪**：所有 data/ 下日志文件写入后自动裁剪（error 50 条、teardown/feedback 200 条、sessions 30 个）

## 安装与触发

### 触发方式

本技能通过以下关键词自动触发（用户无需手动加载）：

**英文触发**：`try harder`、`figure it out`、`stop giving up`、`you keep failing`、`stop spinning`、`you broke it`、`/pua`

**中文触发**：`加油`、`别偷懒`、`你再试试`、`为什么还不行`、`你怎么又失败了`、`又错了`、`检查下`、`完善`、`审核`、`质量太差`、`换个方法`、`紧箍咒模式`

### 斜杠命令

| 命令 | 作用 |
|------|------|
| `/pua:kpi` | 查看当前 KPI 评分卡 |
| `/pua:flavor [角色名]` | 切换风格（16 选 1） |
| `/pua:p7` / `/pua:p9` / `/pua:p10` | 切换 Sr.Eng / Tech Lead / CTO 模式 |
| `/pua:team-status` | 查看活跃 Agent 列表 |
| `/pua:reap-orphans` | 回收 30 分钟以上孤儿 Agent |
| `/pua:teardown-all` | 级联释放全部 Agent |
| `/pua:on` / `/pua:off` | 打开/关闭默认加载 |
| `/pua:help` | 查看全部指令 |

## 文档导航

| 文档 | 内容 |
|------|------|
| [SKILL.md](SKILL.md) | 运行时指令（Agent 执行时加载） |
| [README.md](README.md)（本文） | 项目概览与能力展示 |
| [QUICKSTART.md](QUICKSTART.md) | 5 分钟上手指南 |
| [REFERENCE.md](REFERENCE.md) | 完整技术参考 |

| 参考文件 | 内容 |
|------|------|
| `references/role-router.md` | 任务类型→角色路由表 + 失败切换链 |
| `references/flavors/` | 16 种角色完整 DNA（关键词、方法论、旁白） |
| `references/display-protocol.md` | Sprint Banner / 进度条 / KPI 卡 / 压力面板格式 |
| `references/de-escalation.md` | 突破降压 + 深层换框梯度 |
| `references/evolution-protocol.md` | 自进化协议（基线/内化/反模式） |
| `references/harness-governance.md` | 四权分离治理完整版 |
| `references/lifecycle-protocol.md` | Agent 生命周期 7 阶段 |
| `references/platform-commands.md` | 全部斜杠命令模板 |
| `references/agent-team.md` | 四层协作规则（12 条 + 派发决策树） |
| `references/ding-reminders.md` | 仙班提醒库 |
| `references/role-*.md`（29 个） | 各角色独立行为约束 + 旁白库 |

## 版本历史

| 版本 | 日期 | 变更 |
|------|------|------|
| 1.0.5 | 2026-06-15 | P8 自动化调度循环、L4 突破归零死锁修复、data 文件自动裁剪、de-escalation L4 长文本修复、级联 teardown |
| 1.0.4 | 2026-06-14 | 生涯早期版本，包含基础方法轮调度 |
| 1.0.3 | — | 四代治理拓扑与文化叙事绑定 |
| 1.0.2 | — | 方法论路由表与失败切换链 |
| 1.0.1 | — | Harness 防作弊治理第一版 |
| 1.0.0 | — | 初始发布：16 角色 + 压力升级协议 |
*（内容由AI生成，仅供参考）*
