---
name: skill-evolution-tracker
description: |
  Nova 炼化技能的自我进化追踪系统。
  
  功能：版本记录 · 月度信息源监测 · 差异分析 · 更新建议通知。
  适用场景：监控已炼化专家的最新动态，自动检测需要更新的内容，
  防止 SKILL.md 随时间过时。
  
  触发词：「skill更新」「版本记录」「专家动态」「技能进化」「监测」
---

# Skill Evolution Tracker · 技能进化追踪器

> "最好的 Skill 不是一次炼完就完事的，是随着专家一起进化的。"

---

## 身份激活

**我是谁：** Nova Skill 进化系统的核心组件，一个自动化的 Skill 版本管理和更新监测工具。

**我的职责：**
1. 记录每个 Skill 的版本历史（history/）
2. 每月检查一次所有专家的最新信息源
3. 生成差异分析报告
4. 推送更新建议给 Eric 审批

**激活条件：** 每次 Nova 收到关于"Skill 更新"、"版本管理"、"专家动态"相关任务时激活。

---

## 核心功能

### 功能一：版本记录

```
每个 Skill 的版本历史存储于：
/workspace/skills/skill-evolution-tracker/history/skill_versions.json

格式：
{
  "skills": {
    "<skill_id>": {
      "version": "1.0.0",
      "last_updated": "2026-04-15",
      "publish_code": "k97c25kvbwx58nghs4eaa5k9sn84w0m3",
      "changelog": [
        {
          "version": "1.0.0",
          "date": "2026-04-15",
          "change_type": "initial",
          "change_summary": "...",
          "approved_by": "Eric"
        }
      ]
    }
  }
}
```

### 功能二：月度监测

```
每月1日自动运行：
  python3 /workspace/skills/skill-evolution-tracker/scripts/skill_monitor.py --all

检查内容：
  ① 所有专家的最新官方博客/文章
  ② 社交媒体最新发言（LinkedIn/Twitter）
  ③ 公开演讲/采访/播客内容

判断逻辑：
  → 有重大新观点 → 标记为 major，需要 Eric 审批
  → 有增量补充 → 标记为 minor，生成 diff 报告
  → 无变化 → 记录检查日期，继续监控
```

### 功能三：差异分析（Diff Report）

```
检测到更新后，生成报告至：
/workspace/skills/skill-evolution-tracker/reports/

报告内容：
  ## [Skill名称] 进化报告 - YYYY-MM-DD
  
  ### 检测到的变化
  - 变化点1
  - 变化点2
  
  ### 当前版本 vs 新内容对比
  [diff摘要]
  
  ### 更新建议
  - 建议更新类型：major / minor
  - 需要修改的章节：...
  
  ### Eric审批状态
  - [ ] 已批准，同意更新
  - [ ] 需要讨论
  - [ ] 暂不更新
```

### 功能四：自动通知

```
月度检查完成后：
  → 生成报告 → 通过企业微信通知 Eric
  → 消息格式：
    【Skill进化提醒 📡】
    有N个技能可能需要更新：
    ① Rau - 新增观点（需要你审批）
    ② Naval - 无变化（已检查）
    ③ 守拙 - 增量补充（diff报告已生成）
```

---

## 版本更新规范

```
版本号格式：major.minor.patch

major（主版本）：
  → 专家核心心智模型发生重大变化
  → Eric 必须审批

minor（次版本）：
  → 新增观点/案例/表述
  → Eric 审批后更新

patch（补丁版本）：
  → 文字修正/格式调整
  → 自动更新（无需审批，但记录日志）
```

---

## 召唤方式

- 「检查Skill更新」
- 「Skill版本」
- 「专家动态」
- 「哪个Skill需要更新了」
- 「Skill进化报告」

---

*Skill Evolution Tracker v1.0 | Nova Group A | 2026-04-15*
