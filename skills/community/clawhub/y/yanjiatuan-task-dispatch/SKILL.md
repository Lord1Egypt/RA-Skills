---
name: yanjiatuan-task-dispatch
description: 研家团Skill — 团队任务调度、分派与成果汇总管理
---

# 研家团 · 团队任务调度 (yanjiatuan-task-dispatch)

## 功能
1. **任务分解** — 将投研需求拆解为子任务，匹配对应角色
2. **任务分派** — 将子任务分派给研木/研林/研技/研声/研盾/研策
3. **进度追踪** — 跟踪各角色任务完成状态
4. **成果汇总** — 收集各角色输出，整理为统一格式

## 工作流编排
```
用户需求 → 任务分解 → 并行分派 → 等待完成 → 汇总成果 → 提交研策合成 → 审核交付
                            ↓
              ┌─── 研木（基本面）───┐
              │   研林（产业策略）   │
              │   研技（技术面）    │
              │   研声（舆情）     │
              └─── 研盾（风控）────┘
```

## 调用方式
```bash
python3 {baseDir}/scripts/dispatch_task.py [--task "投研需求描述"] [--stocks "标的列表"] [--output json|text]
```

## 输出示例
```json
{
  "task_id": "T20260706-001",
  "status": "completed",
  "dispatch": {
    "yanmu": {"assigned": ["基本面分析：宁德时代"], "status": "completed"},
    "yanlin": {"assigned": ["产业策略：锂电池赛道"], "status": "completed"},
    "yanji": {"assigned": ["技术分析：宁德时代"], "status": "completed"},
    "yansheng": {"assigned": ["舆情分析：锂电池板块"], "status": "completed"},
    "yandun": {"assigned": ["风险评估：宁德时代"], "status": "completed"}
  },
  "next_step": "提交研策合成最终报告"
}
```
