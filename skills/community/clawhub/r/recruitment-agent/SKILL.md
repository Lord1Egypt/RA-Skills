---
name: recruitment-agent
description: "招聘Agent：通过 opencli(Boss直聘) + lark-cli(飞书多维表格) 管理招聘流程。支持：(1) 查看Boss直聘最近/未读消息; (2) 将候选人存入人才库（先搜索比对，再新建/更新）; (3) 添加人才决策记录（加入库/约面试/跟进/发Offer/归档）; (4) 更新人才库中某候选人的指定信息; (5) 约面试（发邀约消息、心跳检测、确认时间、创建飞书日程）。当用户说「查boss消息」「把XXX存入人才库」「我对XXX感兴趣」「对XXX做个决策记录」「更新XXX的信息/字段」「帮我给XXX约个面试」「约一下XXX」时触发。"
---

# Recruitment Agent

## 重要规则

- **opencli boss 命令必须串行执行**，绝不能并行——同时运行多个会 cookie 冲突导致失败
- 候选人定位统一用 **uid** 作为唯一标识

## 常量

> ⚠️ 安装后请将以下占位符替换为实际值。

| 名称 | 值 |
|---|---|
| Base Token | `<YOUR_BASE_TOKEN>` |
| 人才库V3 table_id | `<YOUR_TALENT_TABLE_ID>` |
| 决策记录 table_id | `<YOUR_DECISION_TABLE_ID>` |
| 使用者姓名 | `<YOUR_NAME>` |
| 使用者 open_id | `<YOUR_OPEN_ID>` |

## 工作流索引

### 主工作流

| 工作流 | 触发词 | 参考 |
|---|---|---|
| 1. 查看Boss消息 | 查boss消息、未读消息、最近对话 | 见下方内联说明 |
| 2. 存入人才库 | 把XXX存入人才库、我对XXX感兴趣 | [workflow-2-save-candidate.md](references/workflow-2-save-candidate.md) |
| 3. 人才决策记录 | 对XXX做决策、约面试、发Offer、归档XXX | [workflow-3-decision-record.md](references/workflow-3-decision-record.md) |
| 4. 更新人才信息 | 更新XXX的信息、给XXX加备注、修改XXX字段 | [workflow-4-update-candidate.md](references/workflow-4-update-candidate.md) |
| 约面试（综合） | 帮我给XXX约个面试、约一下XXX | [workflow-schedule-interview.md](references/workflow-schedule-interview.md) |

### 辅助工具

| 工具 | 用途 | 参考 |
|---|---|---|
| 查看日程 | 查可用时间段，约面试流程中调用 | [util-check-calendar.md](references/util-check-calendar.md) |
| 发飞书消息 | 向使用者确认信息，约面试流程中调用 | [util-send-feishu-message.md](references/util-send-feishu-message.md) |
| 心跳任务 | 后台定时检查候选人回复 | [heartbeat_task.md](references/heartbeat_task.md) |

---

## 工作流 1：查看 Boss 消息（内联）

```bash
# 查看聊天列表（最近联系人）
opencli boss chatlist

# 查看与某人的聊天记录（先从 chatlist 获取 uid）
opencli boss chatmsg <uid>
```

输出字段：name / job / last_msg / last_time / uid / security_id
