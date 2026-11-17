# X 人设运营专家 (X Persona Operator)

> 面向个人或小团队的 X（Twitter）单账号人设化运营技能库。把 AI 编程助手变成一名能长期守住人设、稳定产出、持续增长并维护社区的运营搭档。

## 能力矩阵

| 能力 | 技能 | 描述 | 来源 |
|------|------|------|------|
| 人设设计 | persona-design | 身份定位、声音标尺、话题半径、边界与一致性检查 | [original](skills/persona-design/SKILL.md) |
| 内容引擎 | content-engine | 选题、Hook、长线程结构、跨形态改编 | [derived](https://skills.sh/coreyhaines31/marketingskills/social) |
| 增长策略 | growth-tactics | X 推荐信号、增长循环、内容日历、复盘闭环 | [derived](https://skills.sh/coreyhaines31/marketingskills/social) |
| 互动运营 | engagement-ops | 回复、社区贡献、DM、负面 SOP | [derived](https://skills.sh/101-skills/superpowers/twitter-automation) |

## 架构

采用 **superpower 架构**：`SKILL.md` 只做路由，深层 playbook 在 `references/`（人设校准 / 算法增长 / 内容工作流），可独立调用的细粒度能力在 `skills/`。

```
x-persona-operator/  (Level B)
├── SKILL.md                      路由层
├── references/                   L2 方法论（决策树 + 清单 + 坑）
│   ├── persona-playbook.md
│   ├── growth-algorithm-playbook.md
│   └── content-ops-playbook.md
├── skills/                       L3 细粒度子技能
│   ├── persona-design/           (original)
│   ├── content-engine/           (derived)
│   ├── growth-tactics/           (derived)
│   └── engagement-ops/           (derived)
├── AGENTS.md / README.md / LICENSE / .gitignore
```

## 工作流

```
人设设计 ──▶ 内容引擎 ──▶ 增长策略 ──▶ 互动运营
 (定位)      (写什么)     (怎么涨)      (怎么守)
   │            │            │            │
   └───────────┴────────────┴────────────┘
              统一由 persona-playbook 的人设标尺校准
```

## 安装

```bash
# 安装全部 X 人设运营技能
npx skills add skills-repo/x-persona-operator -g -y

# 或按需安装单个技能
npx skills add skills-repo/x-persona-operator@persona-design -g -y
npx skills add skills-repo/x-persona-operator@content-engine -g -y
npx skills add skills-repo/x-persona-operator@growth-tactics -g -y
npx skills add skills-repo/x-persona-operator@engagement-ops -g -y
```

## 与本组织其他仓库的关系

- **content-creator** — 多平台内容矩阵（视频 / 播客 / 简报），本库聚焦 X 单账号人设化运营
- **marketing-master** — 营销漏斗 / 着陆页 / 投放，本库聚焦社媒账号日常运营
- **writer-studio** — 长文 / 文案 / SEO 文字，本库聚焦推文短形态
- **visual-designer** — 视觉封面 / 品牌图，本库聚焦文字与互动
