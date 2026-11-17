# skill-quality-inspector — 技能质量检查官

面向 **skills-repo 组织内部**的技能仓库治理工具：检查技能质量、修复技能矛盾点、评估技能风险、减少技能冗余、规范技能目录。本质是把组织既有的 `quality-gates` / `superpower-architecture` 规范变成一套可重复执行的质检 + 风控 + 整理流程。

## 定位

- **目标用户**：组织维护者、仓库负责人、定期巡检机器人
- **不解决的**：单领域技能开发（请用对应领域仓库）、第三方社区技能的供应链安全（建议结合 skills.sh 三方审计）

## 架构说明（superpower 五层）

```
skill-quality-inspector/
├── SKILL.md              # L1 路由层
├── references/           # L2 深层 playbook（5 篇）
├── skills/               # L3 细粒度子技能（5 个，可单独安装）
├── scripts/              # L4 确定性脚本（3 个，stdlib-only）
├── assets/               # L5 模板资源（2 个）
├── AGENTS.md
├── README.md
├── LICENSE               # MIT
└── .gitignore
```

加载策略：先读根 `SKILL.md` 路由表，按任务按需加载 `references/` 或调用 `skills/`，确定性检查交给 `scripts/`。

## 核心理念

- **规范即尺子**：以组织 `rules/` 下的门禁与架构规范为唯一事实来源。
- **只读默认不改**：审计脚本只产出报告，修复需显式授权。
- **只增不减**：去重 / 下线走 `deprecated`，不删已发布路径。
- **账实一致**：registry 计数以实时扫描为准。

## 技能清单

| 环节 | 子技能 | 描述 |
|------|--------|------|
| 质量检查 | `quality-auditor` | 对照 Q1–Q10/W1–W7 与架构规范逐条核验并出报告 |
| 矛盾修复 | `contradiction-fixer` | 修复数字不一致、规则冲突、断链、术语漂移 |
| 风险评估 | `risk-evaluator` | 安全/维护/合规三维定级（P1/P2/P3） |
| 冗余治理 | `redundancy-reducer` | 检测重名/近重/关键词打架，提出合并去重建议 |
| 目录规范 | `directory-standardizer` | 校验五层结构、命名、路由完整性 |

## 快速开始

```bash
# 整库安装（推荐）—— 拿到路由层 + 全部 references/scripts/assets
npx skills add skills-repo/skill-quality-inspector -g -y

# 单技能安装 —— 只要某一个细粒度能力
npx skills add skills-repo/skill-quality-inspector@quality-auditor -g -y
```

## 推荐工作流

1. **新建自检**：写完仓库跑 `python3 scripts/quality_audit.py --repo <path> --strict`。
2. **矛盾扫描**：`python3 scripts/contradiction_scan.py --repo <path>` 查断链/数字矛盾。
3. **组织巡检**：`python3 scripts/redundancy_scan.py --org <root>` 查跨仓库重叠。
4. **出报告**：用 [assets/quality-report-template.md](assets/quality-report-template.md) 套模板，按阻断/警告/建议三档交付。
5. **门禁兜底**：再跑 `audit_architecture.py` 与 `audit_readme_gates.py`（`skills-repo-admin`）。

## 许可

MIT © skills-repo
