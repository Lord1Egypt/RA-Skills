---
name: venus-project-pm
homepage: https://github.com/spikesubingrui-design/venus-project-pm
version: 1.0.0
description: |
  金星幼儿园 ERP 项目进度管理总控 Skill。将飞书群标签页、多维表格、动态 roster、planning-with-files 和晨晚 cron 串成一套软件开发项目管理流程。既跟踪 13 个模块进度，也跟踪 0-1 上线时间线（发送测试、小程序注册、提审、上线）。适用于“金星项目追踪”“ERP 项目管理”“飞书群内进度追踪”“模块里程碑追踪”“上线推进”等场景。
triggers:
  - "金星项目追踪"
  - "ERP 项目管理"
  - "飞书群内进度追踪"
  - "模块里程碑追踪"
tools:
  - shell
mutating: true
---

# Venus Project PM

## 作用

这是金星项目追踪的总控 skill，不直接替代 `venus-tracker`，而是规定整套流程：

1. 群内原生入口：飞书群顶部 `项目追踪` 标签页
2. 数据层：飞书多维表格 `日报表 / 任务表 / 项目总进程表`
3. 成员层：`sync-roster` 动态同步当前应报成员
4. 项目管理层：`workspace/.planning/venus-erp/task_plan.md`（模块里程碑 + 项目级上线时间线）
5. 输出层：`agent-format` 风格的晨晚追踪

## 必须先读

- `workspace/skills/venus-tracker/SKILL.md`
- `workspace/.planning/venus-erp/task_plan.md`
- 若要约束开发描述质量，同时参考 `workspace/skills/karpathy-coding-guidelines/SKILL.md`

## 工作流

### Phase 0：校准入口

确认群里已存在 `项目追踪` 标签页；如果没有，执行：

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py setup-group-tab
```

### Phase 1：同步应报成员

每次晨晚追踪前都先刷新 roster：

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py sync-roster
```

目标是让“谁需要填报”跟群内实际成员保持一致，例如吕不在群就不再催他。

### Phase 2：读取项目计划

如果 planning 文件不存在，先初始化：

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py seed-planning
```

读取：

- `workspace/.planning/venus-erp/task_plan.md`
- `workspace/.planning/venus-erp/findings.md`
- `workspace/.planning/venus-erp/progress.md`

重点看两层：

- 13 个模块的里程碑、基线进度和当前阶段
- 项目级 0-1 上线时间线：发送测试、小程序注册/资质、提审、审核通过、上线准备、正式上线

### Phase 3：跑确定性脚本

晚间汇总：

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py collect
```

晨间追踪：

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py track
```

### Phase 4：做 PM 视角比对

将脚本输出与 `task_plan.md` 对照，补上四类判断：

- 哪个模块在推进
- 哪个模块偏离计划或持续阻塞
- 当前卡在哪个上线阶段
- Spike 今天需要盯哪一件事

### Phase 5：推送口径

- 不再推 `share/base/...` 外链
- 始终引导到群顶部 `项目追踪` 标签页
- 未交成员只针对当前 `active_reporters`
- 若在老 Base 上追加字段，先执行：

```bash
python3 /Users/spikescp/.openclaw/workspace/scripts/venus-bitable-sync.py migrate-base
```

## 推荐组合

| 环节 | Skill |
|------|-------|
| 计划与里程碑 | `planning-with-files` |
| 开发描述质量 | `karpathy-coding-guidelines` |
| 复盘/周度回顾 | `gstack-retro` |
| 数据同步与追踪 | `venus-tracker` |

## 反模式

- 把群里所有人都当成应报成员
- 继续把外链表单当作默认入口
- 晨晚 cron 只跑脚本，不读 PM planning 文件
- 只看模块进度，不看 0-1 上线时间线
- 汇报只写“继续开发”“继续优化”这种不可验证描述
