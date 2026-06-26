---
name: solo
description: |
  SOLO — Solo Operating Legion ⚡ 三权制衡架构。内核(立法) + SOLO审计(司法) + 技能(执行)。meta-agent，零脚本，纯OpenClaw原生。
homepage: https://github.com/meta-evo-creator/solo
version: 2.0.0
metadata:
  openclaw:
    emoji: ⚡
    requires: {}
---

# SOLO v2.0 ⚡ — 三权制衡架构

> **One person, an entire agent army.**
> 内核定铁律，SOLO管审计，技能干实事。零脚本，纯 OpenClaw 原生。

---

## 架构总览

```
┌──────────────────────────────────────────────────────────────┐
│ ① 内核（立法权）                                            │
│   SOUL.md · AGENTS.md · TOOLS.md                            │
│   六条铁律 · Suit门禁 · 工具护栏                             │
├──────────────────────────────────────────────────────────────┤
│ ② SOLO（司法/审计权） · Pro 模型                            │
│   agent-audit.md · AUDIT_LEARNINGS.md                       │
│   事前拦截 · 事后审计 · 跨任务模式检测 · 审计层自我进化       │
│   Flash⊥Pro 异构校验 · memory/audit/{archive,knowledge,meta} │
├──────────────────────────────────────────────────────────────┤
│ ③ 技能（执行权）                                            │
│   cron / MSF / DI / babata-browser / ...                    │
│   执行 → 写 G4.5 signature → 审计层消费                       │
└──────────────────────────────────────────────────────────────┘
```

**三权边界：** 立法不可改（内核只追加不修改），司法只读不写（只提提案不改SOP），执行不许越权（受铁律+审计双重约束）。

---

## 一、内核（立法权）

| 文件 | 职责 | 访问方式 |
|:-----|:-----|:---------|
| `SOUL.md` | 六条铁律：隐私/溯源/注入/权责/惜文件/谦逊 | Suit Step 0 门禁自检 |
| `AGENTS.md` | 工作区规则：三层记忆·会话协议·工具调用纪律 | 每次会话自动加载 |
| `TOOLS.md` | 工具护栏：搜索降级链·反爬检测·web_fetch→babata硬规则 | 每次任务工具选择 |

内核原则：**只追加不修改**——铁律不能降级，只能补充。

---

## 二、SOLO审计（司法权）

**独立技能：** `skills/solo-audit/SKILL.md` — 由OpenClaw自动发现

对标六条铁律（是非）+MEV五层（质量）+四原则（设计），从cron runs日志追踪。零异常一句输出。只提提案不执行。

### 审计规则

**文件：** `AUDIT_LEARNINGS.md`
- 每次审计提案经石冰审批通过后自动追加
- 所有技能启动时自动加载（每个 cron payload 顶部 `read AUDIT_LEARNINGS.md`）

### 审计仓库

```
memory/audit/
├─ archive/         哈希链档案，审计结论永久不可改
├─ knowledge/
│  ├─ 失败模式清单.json    已知失败模式字典
│  ├─ 已批准的SOP改动记录.json  已生效改动
│  └─ 已拒绝的审计提案.json     被拒提案及理由
└─ meta/
   ├─ auditor-health.json   采纳率·健康度·自检建议
   └─ audit-standard-changes.json  审计标准变更日志
```

### 审计日程

| cron | 时间 | 职责 |
|:-----|:----:|:------|
| **SOLO 每日审计** | **22:00** | 读当日全部技能产出→跨任务模式检测→提案→推送 |

---

## 三、技能（执行权）

| 技能 | 文件 | 职责 |
|:-----|:-----|:------|
| AI圈热点 | cron payload | 每日04:00 增量热点监测 |
| 医院智慧监督 | cron payload | 每日06:00 情报内参 |
| AI医疗案例 | cron payload | 每日09:00 企业案例 |
| 法规月度检查 | cron payload | 每月1日法规版本校验 |
| MSF | `skills/msf/` | 医学社会组织尽职调研 |
| DI | `skills/discipline-inspect/` | 纪检法规搜索 |
| babata-browser | `skills/babata-browser/` | 反爬页面抓取（取内容） |
| babata-search | `skills/babata-search/` | 中文搜索引擎 v2.0（搜链接） |
| ... | ... | ... |

### 🔗 技能关联：search → browser 标准工作流

```
babata-search（搜）  ──→  babata-browser（取）
     ↓                        ↓
  找有什么                打开看内容
  返回URL列表              返回全文/证据
```

**规则：** search 搜到的非静态页面链接，必须用 babata-browser 打开获取内容，不能用 web_fetch。
**例外：** 学术搜索（知网/万方）直接走 babata-browser，不经过 search。

每个技能执行完成后必须：
1. 写 G4.5 `execution_signature` 到 checkpoint
2. 输出含 `rawLength` / 反爬关键词 / 签名三段式
3. **在每阶段切换时更新 `.solo/pipeline-status.json`**（为 `solo status` 提供实时进度数据）

---

## 调度规则

| 层级 | 触发规则 |
|:-----|:---------|
| **循坏调度** | cron 表达式固定（4/7/9/22点，法规每月1日） |
| **按需调度** | 石冰直接触发 MSF/DI/babata-browser |
| **审计调度** | SOLO 每日22:00 自动扫描所有任务输出 |

---

## 清单

| 文件 | 来源 |
|:-----|:------|
| `skills/solo/SKILL.md` | 本文档 |
| `skills/solo/agent-audit.md` | 审计Agent |
| `AUDIT_LEARNINGS.md` | 审计规则 |
| `memory/audit/` | 审计仓库 |
| 内核三件套 | `SOUL.md` · `AGENTS.md` · `TOOLS.md` |
| 各技能文件 | `skills/{msf,discipline-inspect,...}/` |

---

## Changelog

| 版本 | 日期 | 变化 |
|:-----|:----:|:------|
| **2.0.1** | **05-24** | **新增管线状态协议：`.solo/pipeline-status.json`（DR/DI/MSF统一状态文件），`solo status` 命令可视化进度面板** |
| **2.0.0** | **05-23** | **三权制衡架构重写：内核(立法)+SOLO审计(司法·Pro·反镜像·🚨紧急·哈希链)+技能(执行)。MSF降级+宪法规则+元进化闭环。** |
| 1.0.0 | 05-18 | 初版。SOLO 从 v8 架构进化而来。Meta-agent monitors the fleet. |
