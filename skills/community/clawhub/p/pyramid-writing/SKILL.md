---
name: pyramid-writing
description: 金字塔原理（Pyramid Principle）写作与结构化表达工作流。用于把散乱内容改写成“先结论、后论据”的可汇报文稿（方案评审、周报、邮件、PRD 段落、演讲稿、技术传播），输出关键结论、分组论点（MECE）、证据与行动项，并对照目标做最终评估。
---

# 金字塔原理写作：先结论，后论据

## 触发方式

- 用户说“用金字塔原理/先结论后理由/把这段写成汇报/帮我结构化/写一页纸/写成可评审的方案/把材料整理成要点”时使用本 Skill。
- 适用内容：方案评审、工作汇报、复盘总结、产品/技术说明、对外技术传播（DevRel/博主）。

## 输入模板（复制填空）

缺信息时先做合理假设，并把假设列入“待确认项”。如果用户给的是一堆材料，先做“信息归并”再写结构。

```text
写作场景（Scenario）：汇报/评审/邮件/演讲/对外文章
面向读者（Audience）：老板/评审人/同事/客户/大众
目标（Goal）：通过/对齐/决策/推进/说服/让人能复述
读者关心（Reader Concerns）：成本/风险/时效/收益/可落地性/合规
材料（Raw Notes）：要点/数据/事实/约束/链接（可直接粘贴）
必须包含/避免（Must include/avoid）：
限制（Constraints）：字数/一页纸/口吻/是否需要行动项
```

## Quick Start（开箱即用）

当用户没有给完整输入模板时，按以下顺序补齐并开始产出：

1. 让用户选择写作场景：评审/汇报/邮件/对外文章（或你自行推断并写入假设）
2. 读取 `references/presets.md`，套用对应预设生成 Success Criteria（3-7 条）
3. 若用户想直接测试，提供 `references/sample-requests.md` 的示例输入
4. 若用户想看“写出来大概长什么样”，先读 `references/example-outputs.md` 里的最接近案例，对齐风格和颗粒度
5. 读取 `assets/output-template.md` 选择模板：评审/立项/决策用 `decision-template.md`；汇报/复盘/对外文章用 `standard-template.md`；邮件/IM/短周报用 `compact-template.md`
6. 按选中的模板输出，并在最后做“目标达成评估”

## 工作流（Pyramid Principle）

按顺序执行；除非用户指定输出形式，否则使用“默认输出格式”。

### 1) 把目标变成成功标准（Success Criteria）

- 从 `references/rubric.md` 选择 3-7 条维度，改写成可检查的标准（含阈值/可观察描述）。
- 若约束冲突（例如“一页纸但要包含所有细节”），优先提醒冲突并提出折中结构（主文 + 附录）。

### 2) 归并原始材料（Normalize Raw Notes）

- 将用户给的散乱材料归并为 5 类：`事实`、`约束`、`结论候选`、`风险/反对点`、`信息缺口`。
- 去掉重复点，合并同义表述，标出“缺证据的判断”和“需要确认的前提”。
- 如果原始材料本身是流水账，先抽出 1 条主线问题：这份文稿要帮助读者完成什么动作（决策/对齐/推进/回复）。

### 3) 先写一句话结论（Key Message）

- 用 1 句话回答“所以我们要做什么/结论是什么/推荐哪个选项”。
- 如果结论依赖假设，用限定语标明：`在 X 前提下，推荐 Y`。

### 4) 搭建金字塔结构（Top-down）

- 将论据分组为 3-5 个一级要点（彼此 MECE，避免重叠）。
- 每个一级要点下补 2-4 个二级支撑（事实/数据/约束/案例）。
- 避免“并列句堆叠”：每组要点必须能回答一个明确问题（Why/What/How/Risk）。

### 5) 证据与行动项（Evidence & Actions）

- 对每个一级要点给出可验证证据或依据（数据、观察、约束来源）。
- 产出行动项：负责人/下一步/截止时间（未知则写待确认项）。

### 6) 风险、权衡、反对意见（Risks & Trade-offs）

- 至少列出 3 个风险与缓解措施。
- 给 1-2 个替代方案与 trade-off（尤其是评审/决策场景）。
- 对可能的反对意见给出回应（基于证据/边界/成本）。

### 7) 最终评估（Evaluate Against Goal）

- 对照 Success Criteria 打分并给理由。
- 给出结论：`已达成/部分达成/未达成（需澄清）`，并给 1 轮修改建议（按收益排序 1-3 条）。
- 如果输出仍显得“像流水账/不像结论驱动/风险写得空/模板过重”，读取 `references/anti-patterns.md`，按反模式逐条纠偏后再给最终版。

## 默认输出格式

- `一句话结论（Key Message）`
- `金字塔要点（MECE）`：3-5 条一级要点，每条含 2-4 个支撑点
- `证据/依据`：每条一级要点对应证据（或说明缺口）
- `风险与权衡`：风险 + 缓解；替代方案 + trade-off
- `行动项`：Owner/Next Step/ETA（未知则待确认）
- `待确认项`
- `目标达成评估`：对照表 + 下一步修改建议

## 资源文件（references/ 与 assets/）

- 评分量表：读取 `references/rubric.md`，生成 Success Criteria 并用于最终打分。
- 场景预设：读取 `references/presets.md`，在输入不完整时补齐 Audience/Constraints 与默认结构。
- 示例请求：读取 `references/sample-requests.md`，提供可复制测试输入。
- 成品示例：读取 `references/example-outputs.md`，在用户需要风格锚点、样张、或你需要校准输出颗粒度时使用。
- 反模式库：读取 `references/anti-patterns.md`，在输出不够像“金字塔原理”或用户反馈“还是不清楚”时用于修稿。
- 输出模板索引：先读 `assets/output-template.md` 选择模板，再按场景读取：
  - `assets/decision-template.md`：评审/立项/取舍/关键决策
  - `assets/standard-template.md`：常规汇报、说明文、复盘、对外技术传播
  - `assets/compact-template.md`：关键邮件、IM、短周报、状态同步
