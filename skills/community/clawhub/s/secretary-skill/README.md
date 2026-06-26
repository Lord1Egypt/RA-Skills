# Secretary Skill（秘书技能）

帮助用户制定计划并执行计划，确保计划能够顺利完成的自动化工具。

## 核心工作流

```
[模糊/深远的愿景]
       │
       ▼
 1. De-ambiguation  ——► 定向追问 ——► 锁定 "原始目标"
       │
       ▼
 2. Vertical Splitting ——► 拆解为 Milestones ——► 生成 Atomic Tasks
       │
       ▼
 3. Cron Automation   ——► 设定执行频率 ——► 输出定时配置
```

## CLI 命令

| 命令 | 功能 |
|------|------|
| `/init_goal` | 启动去模糊引擎，锁定具体可衡量的目标 |
| `/split` | 将目标拆解为里程碑和原子任务 |
| `/schedule` | 映射时间线，生成定时任务配置 |
| `/align` | 计划偏离时重新校准 |
| `/status` | 评估当前进展 |

## 项目结构

```
src/          核心逻辑
commands/     CLI 命令实现
docs/         文档
tests/        测试
```
