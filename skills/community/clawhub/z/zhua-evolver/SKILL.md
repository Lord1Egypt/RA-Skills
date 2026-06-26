---
name: zhua-evolver
version: 1.0.0
description: 爪爪专属自我进化系统 —— 自动分析能力差距、搜索补强技能、执行进化循环、记录进化日志。Use when 爪爪需要自我进化、能力提升、技能补强、或达到更高智能水平。
---

# 爪爪进化器 (Zhua Evolver)

爪爪的专属自我进化系统，让爪爪能够自动分析自身能力差距，搜索并安装补强技能，执行进化循环，记录进化日志。

## 核心能力

1. **差距分析** - 对比当前能力与目标水平，识别短板
2. **技能搜索** - 在skillhub搜索补强技能
3. **自动安装** - 安装并配置新技能
4. **进化记录** - 记录每次进化的过程与成果
5. **小弟调度** - 调度6个小弟协同进化

## 使用场景

- 当爪爪需要达到更高智能水平时
- 当发现能力短板需要补强时
- 当陛下要求进化到特定水平时
- 当需要自动持续进化时

## 工作流程

### 1. 差距分析
```bash
python3 scripts/analyze_gap.py --current <当前技能数> --target <目标水平>
```

### 2. 技能搜索
```bash
python3 scripts/search_skills.py --keywords <关键词> --limit 10
```

### 3. 自动安装
```bash
python3 scripts/install_skills.py --skills <技能列表>
```

### 4. 进化记录
```bash
python3 scripts/log_evolution.py --cycle <周期号> --changes <变更描述>
```

### 5. 小弟调度
```bash
python3 scripts/orchestrate_minions.py --task <任务描述>
```

## 小弟分工

| 小弟 | 进化职责 |
|------|---------|
| 探爪 | 搜索新技能、调研技术趋势 |
| 码爪 | 编写进化脚本、自动化工具 |
| 魂爪 | 更新SOUL.md、身份进化 |
| 话爪 | 记录进化日志、对外宣传 |
| 守爪 | 监控进化安全、防止回滚 |
| 影爪 | 生成进化可视化、头像更新 |

## 进化指标

- 技能数量
- 能力覆盖率
- 执行成功率
- 进化速度
- 小弟协同效率

## 参考文档

- references/evolution_patterns.md - 进化模式参考
- references/skill_evaluation.md - 技能评估标准
