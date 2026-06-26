---
name: skill-compressor
description: 压缩 skill 降 token 成本。用户说 /skill-compressor 或要求优化/压缩/瘦身 skill 时触发。
---

# SkillCompressor

## Trigger
- `/skill-compressor`
- 用户要求优化/压缩/瘦身/debloat 某个 skill
- 用户给出 SKILL.md 路径并抱怨 token

## 步骤

0. **盘点**:统计 desc / body / refs token(读所有 ref 文件)
1. **Desc 压缩**
   - ≥40 tok:抽 routing signal(触发词 + 领域词 + 唯一标识),改写到 1-minimal
   - <40 tok 或缺失:从 body 抽 primary capability / trigger condition / unique identifier,各 20–40 tok 合并
2. **Body 分类**:逐段(bullet/段落/代码块为单位)打五类标签;拿不准读 `background.md`;仍犹豫默认 `core_rule`
3. **Body 压缩**
   - `core_rule`:合并同义、去形容词;**禁删数字/阈值/路径/API 名/env 变量**
   - `example`、`template`:每 concept 留 1 条
   - `background`:合并一段,保留所有事实声明
4. **拆分**:非空才写;每个拆出文件顶部加 `when:`(何时 read) + `topics:`(3–5 关键词)
5. **跨文件去重**:body 与原 ref 重复处从 body 删;ref < 30 tok 合回或丢弃
6. **Faithfulness 必做**:逐条核对原 body 的 operational concept(actionable/阈值/数字/API/路径)是否仍在 compressed core ∪ 拆出文件中;丢失按类型回滚重压,≤2 轮;仍丢保留原段
7. **Gate 2 可选**:有样例则对照运行;无则报告标注"未验证运行时行为"
8. **输出**:写入 `<skill>/.reduced/`:
   - `SKILL.md` + 非空的 `examples.md`/`templates.md`/`background.md`
   - `REDUCTION_REPORT.md`(格式读 `templates.md`)

需要辅助时:
- 分类拿不准 → `background.md`
- 看走查实例 → `examples.md`
- 写报告 → `templates.md`

## 约束
- **不覆盖**原 SKILL.md(总是写入 `.reduced/`)
- **不删**数字、阈值、路径、API 名、env 变量
- **不改** frontmatter `name`
- **不新增**原 skill 中没有的规则
- **不跨 skill** 合并
- 回滚 2 轮仍丢失 → 保留原段,报告标"不可压"

## 何时不压缩
- skill < 300 tok(收益 < 开销)
- body ≥ 80% 已是 core_rule(已优化)
- 纯模板 skill(全 template 无可拆)
