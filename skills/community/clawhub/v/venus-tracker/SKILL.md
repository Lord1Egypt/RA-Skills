---
name: venus-tracker
homepage: https://github.com/spikesubingrui-design/venus-tracker
version: 1.0.0
description: |
  金星幼儿园 / 幼儿园 ERP 项目追踪执行 Skill。负责飞书多维表格的数据同步与晨晚追踪，必须在 `venus-project-pm` 总控流程下使用。适用于“项目追踪”“日报汇总”“晨间追踪”“飞书项目看板”“ERP 进度表”“金星项目日报”等场景。
triggers:
  - "项目追踪"
  - "日报汇总"
  - "晨间追踪"
  - "飞书项目看板"
  - "ERP 进度表"
  - "金星项目日报"
tools:
  - shell
mutating: true
---

# Venus Tracker

## 作用

维护金星幼儿园小程序项目的飞书多维表格追踪体系：

- `日报表`：组员通过群顶部 `项目追踪` 标签页进入飞书 Base 提交日报
- `任务表`：根据日报自动沉淀待办 / 完成 / 阻塞，并保留 `任务类型 / 所属上线阶段 / 时间节点 / 输出物`
- `项目总进程表`：按模块追踪总进度
- `project timeline`：通过 planning + 任务字段追踪 0-1 上线节点（发送测试、注册、提审、上线）

## 前置要求

执行本 skill 前，必须先读：

- `workspace/skills/venus-project-pm/SKILL.md`
- `workspace/.planning/venus-erp/task_plan.md`

## 关键文件

- 配置：`workspace/config/venus-bitable.json`
- 脚本：`workspace/scripts/venus-bitable-sync.py`
- 使用说明：`workspace/docs/venus-tracker-onboarding.md`

## 常用命令

### 初始化 Base

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py init-base
```

### 初始化项目总进程表基线

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py seed-progress
```

### 初始化项目 planning 文件

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py seed-planning
```

### 创建/更新群顶部标签页

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py setup-group-tab
```

### 为已有 Base 补齐新增字段

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py migrate-base
```

### 同步当前应报成员

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py sync-roster
```

### 晚间汇总（19:00）

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py collect
```

### 晨间追踪（08:00）

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py track
```

## 输出约定

- 聊天层输出遵循 `agent-format`
- 有阻塞时优先给出：
  - 谁卡住了
  - 卡在哪个模块
  - 是否需要 Spike 介入
- 晨晚输出除了模块进度，还要明确：
  - 当前处于哪个上线阶段
  - 下一个上线节点是什么
  - 是否存在延期或提审/上线风险

## 组员填写口径

日报统一包含：

- 日期
- 成员
- 角色
- 工作类型
- 关联模块
- 关联上线阶段
- 今日完成
- 明日计划
- 卡点求助
- 计划完成时间
- 实际完成时间
- 输出物/链接

任务表统一包含：

- 模块
- 任务类型
- 所属上线阶段
- 负责人
- 优先级
- 状态
- 计划开始日 / 计划完成日 / 实际完成日
- 来源日期 / 来源成员
- 阻塞原因
- 验收标准
- 输出物/链接
- 备注

## 反模式

- 继续读飞书群自由聊天历史做项目追踪
- 同时维护本地 JSON 和飞书表两套主数据
- 在提醒消息里继续发 `share/base/...` 外链
- 不同步 roster，仍然硬编码谁必须填报
- 任务表不记录上线阶段，导致发送测试/提审/上线无法跟踪
- 汇报里只写“继续开发”“继续优化”这类不可追踪描述
