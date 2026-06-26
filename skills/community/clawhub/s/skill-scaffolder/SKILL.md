---
name: skill-scaffolder
description: 生成结构精简的 Claude Code skill 骨架，强制 routing-signal 三要素 + 五类 body taxonomy + Faithfulness gate。用户说起草/设计/新建/scaffold skill 时触发。
---

# SkillScaffolder

## Trigger
- `/skill-scaffolder`
- 用户要求起草 / 设计 / scaffold / 新建一个 skill
- 用户有 idea 要落成 skill

## 7 步流程（一次性产出，非引导式）

0. **Retirement check**（Gate 0）：给 3 个"典型触发场景"。若裸模型 / 现有 skill / CLAUDE.md 都能搞定 → 建议退休，停止
1. **Routing signal 三要素**：primary capability（10–20 tok）+ trigger condition（10–20 tok）+ unique identifier（10–20 tok）
2. **Description draft**：三要素合成 ≤120 tok；DDMIN 自检（能否再删一词仍唯一触发）
3. **Body taxonomy 预标**：逐条规则打五类标签（`core_rule` / `background` / `example` / `template` / `redundant`）；拿不准读 `background.md`
4. **File split 布局**：SKILL.md 只放 `core_rule`；非空拆出文件必有 `when:` + `topics:` frontmatter；< 50 tok 的拆出文件合回 SKILL.md
5. **四反模式检查**：
   - ❌ examples-as-specification（规则藏在示例里）
   - ❌ background 藏数字 / 阈值 / 路径 / API / env
   - ❌ description 堆触发词枚举
   - ❌ redundant（body 重复 refs）
6. **Faithfulness 自检**（Gate 1）：列 operational concept（动词 / 阈值 / 路径 / API / env）→ 核对都在 `core_rule` ∪ 拆出文件；丢失则回滚到 `core_rule`
7. **产出**：写到 `<path>/<skill-name>/`：
   - `SKILL.md`（core_rule only）
   - 非空的 `background.md` / `examples.md` / `templates.md`（各带 frontmatter）
   - `ARCHITECT_REPORT.md`（格式读 `templates.md`）

辅助：
- 分类拿不准 → `background.md`
- 对照走查 → `examples.md`
- 骨架 / 报告模板 → `templates.md`

## 约束
- **不创建** < 300 tok 的 skill（Gate 0 退休）
- **description ≤ 120 tok**
- **body `core_rule` 占比 ≥ 80%**；不到重新归类或退休
- **不堆触发词**枚举到 description
- **不把 operational 信息藏**在 background / example
- **每个拆出文件**必有 `when:` + `topics:` frontmatter
- **不覆盖**已存在的目录（若 `<path>/<skill-name>/` 存在，改写到 `<skill-name>.new/`）

## 不该用 skill-scaffolder 的情况
- 改造**老 skill** → 用 [`skill-compressor`](https://github.com/David0Ming/skill-compressor)
- 想要**引导式创作 + eval 迭代** → 用官方 `skill-creator`
- 只有 1–2 条规则 → 直接写进 `CLAUDE.md`，不建 skill
