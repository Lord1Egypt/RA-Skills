# 审计手册 · 报告模板与执行细则

## 单 skill 评分 · Markdown 模板

```markdown
# Skill Review · {skill_name}

**路径**：`{skill_path}`  
**Rubric**：TRACE+ v2.0（T-R-F-S-I-E · 30 子项）  
**综合分**：{composite_score}/100 · **评级** {rating} · **结论** {verdict}  
**E 维模式**：{effectiveness_mode}

## 六维得分（TRACE+）

| 维度 | 得分 | TRACE 映射 | 说明 |
|------|------|------------|------|
| T Trust 安全可信 | {T}/10 | TRACE T | {one_line} |
| R Reliability 运行可靠 | {R}/10 | TRACE R | {one_line} |
| F Findability 可发现性 | {F}/10 | TRACE A | description/CSO/触发 |
| S Structure 结构 | {S}/10 | TRACE C | L1/L2/L3、渐进披露 |
| I Instruction 指令 | {I}/10 | 写作反向+reviewer | 祈使、示例、可执行性 |
| E Effectiveness 效果 | {E}/10 | TRACE E | {one_line} |

## 来源覆盖

本评分参考：TRACE · Extra08 · skill-reviewer · skill-quality-audit · skill-creator ·（可选 skill-eval）

## 红线 / Critical

{若无：✅ 未发现 critical 安全问题}

## Top 5 修复项

1. **[{维度}{子项}]** {action} — 来源：{Extra08|skill-reviewer|TRACE|…}

## 触发测试（F 维）

从 description 提取 when / 触发词 / 关键词，填写 **应触发 / 不应触发各 ≥3 条**：

- **应触发**：用户原话或近义说法，应路由到本 skill（非泛化助手）
- **不应触发**：相邻任务、泛化请求、或应路由到其他 skill 的说法

**应触发**：…  
**不应触发**：…

## 弱项明细（score ≤ 1）

| 子项 | 分 | 证据 |
|------|-----|------|

---
*rubric v2 · 公式见 scoring-engine-deterministic.md*
```

---

## A vs B 对比 · Markdown 模板

```markdown
# Skill 对比 · {skill_a} vs {skill_b}

**Rubric**：TRACE+ v2.0（同一公式，不得换 rubric）

## 综合对比

| Skill | T | R | F | S | I | E | 综合 | 评级 | Verdict |
|-------|---|---|---|---|---|---|------|------|---------|
| {skill_a} | | | | | | | | | |
| {skill_b} | | | | | | | | | |
| **Δ (A−B)** | | | | | | | | | |

## 六维分差解读

| 维度 | Δ | 谁更强 | 关键差异 |
|------|---|--------|----------|
| T | | | |
| R | | | |
| F | | | |
| S | | | |
| I | | | |
| E | | | |

## 推荐

- **保留/主推**：{skill_name} — 理由：{composite + 关键维优势}
- **合并项**：从较弱方吸收 {具体 references/脚本/触发词}
- **弃用/归档**：{若适用}

## 触发路由对比（F 维）

同一组用户说法下的期望路由：

| 用户说法 | 期望 | {skill_a} | {skill_b} |
|----------|------|-----------|-----------|
| … | 应选 A/B/均不选 | | |

---
*rubric v2 · 各 skill 完整 JSON 附于文末或分文件*
```

---

## 批量评分 · Markdown 模板

```markdown
# Skills 批量评分 · {parent_dir}

**Rubric**：TRACE+ v2.0 · 共 {n} 个 skill

## 汇总表

| Skill | T | R | F | S | I | E | 综合 | 评级 | Verdict |
|-------|---|---|---|---|---|---|------|------|---------|
| … | | | | | | | | | |

## 简评（按综合分降序）

### {skill_name} — {composite}/100 · {rating}

- **亮点**：{1 句}
- **首要修复**：**[{子项}]** {action}
- **Verdict**：{Pass|Conditional Pass|Fail}

---
*rubric v2 · 公式 round((T+R+F+S+I+E)×100/60, 1)*
```

---

## LLM 执行纪律

1. 跑 `static_audit.py` v2 → Read `scoring-engine-deterministic.md` → 读目标 SKILL.md → 填 30 子项 → 验算
2. **不得**仅报 TRACE 五维而跳过 F/S/I
3. **不得**用旧公式 `(T+R+A+C+E)×2`
4. 0 分必须可定位 evidence；`auto_scores` 项只补 evidence 不改分
5. **对比**：两份完整 JSON + 上表「A vs B 对比模板」
6. **批量**：汇总表 + 各 skill 一段简评（可省略弱项明细表）
7. F 维须含触发测试（应触发 / 不应触发各 ≥3 条）；对比模式加路由对比表
