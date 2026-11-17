# 目录规范化（directory-standardization）

> superpower 架构能不能成立，先看目录摆得对不对。本篇是五层结构的"验收清单"与常见错配速查。

## 一、五层职责边界（不许混层）

| 层 | 放什么 | 不放什么 |
|----|--------|----------|
| L1 `SKILL.md` | 触发条件、能力索引表、脚本清单、核心原则 | 具体命令细节、长方法论 |
| L2 `references/` | 某主题完整 playbook（决策树/命令/坑/清单） | 可独立安装的能力单元 |
| L3 `skills/` | 可单独 `npx skills add` 的细粒度能力 | 只有本仓才有意义的方法论 |
| L4 `scripts/` | 确定性、可重复、带 `--help` 的脚本 | 需人判断的流程 |
| L5 `assets/` | 配置模板、文档模板、示例规范 | 一次性产物 |

**混层是最常见失败模式**：把方法论塞进 L1（超 150 行）、把可安装能力塞进 L2、把流程写进 L4 脚本却要人拍板。

## 二、命名约定

- 仓库名：小写、连字符、领域名（如 `skill-quality-inspector`）
- 技能名：kebab-case、动名结构（`quality-auditor` 而非 `quality`）
- 技能目录名：必须等于 frontmatter 的 `name`
- references 文件名：主题 kebab-case（`quality-dimensions.md`）

## 三、路由完整性检查清单

- [ ] `references/` 每个 `.md`（除 `.gitkeep`）都在根 SKILL.md 路由表出现
- [ ] `scripts/` 每个 `.py` 都在根 SKILL.md「内置脚本」段出现
- [ ] `assets/` 每个文件都在根 SKILL.md「模板资源」段出现
- [ ] 路由表每行指向真实存在的路径（无悬空）
- [ ] 路由表每行带 3–6 个 grep 关键词（中英混合）
- [ ] 根 SKILL.md ≤150 行、无遗留 `TODO`、声明 `metadata.architecture: superpower`

## 四、Level 判定速查

| 信号 | 倾向 |
|------|------|
| 有明确文件产物 / 反复重写样板 / 反复复制配置 | A（加 scripts+assets） |
| 核心价值是判断、表达、沟通、策略 | B |
| 想不出第二个脚本写什么 | B |

## 五、典型错配

- **路由孤儿**：写完 `references/x.md` 忘了在根 SKILL.md 登记 → Agent 永远加载不到（D35 实证）。
- **悬空脚本引用**：playbook 调 `scripts/y.py` 但磁盘没有 → 指令不可执行（security-guardian 实证）。
- **legacy 残留**：旧仓库缺 L1 路由层，必须先迁移再添技能，别在旧结构堆。
- **为凑 A 造脚本**：无真实确定性任务就老实做 B，堆死代码是维护负债。

## 相关子技能与层次边界（L2→L3）

- [skills/directory-standardizer/SKILL.md](../skills/directory-standardizer/SKILL.md) — 本篇的执行落地层：本篇给"五层职责边界 + 命名约定 + Level 判定速查 + 错配清单"，子技能给对齐目录、补路由、消孤儿的操作步骤（见其「工作流」）。
- 边界：**该不该改归本篇（判定），怎么改归子技能（执行）**。尤其 Level A/B 的取舍先读本篇第四节速查表，避免"为凑 A 造脚本"。
- 定级联动：结构分档的事实来源始终是 `skills-repo-admin` 的 `audit_architecture.py`；本仓 [skills/quality-auditor/SKILL.md](../skills/quality-auditor/SKILL.md) 只在其之上做跨文件一致性补充，不重复判分。
