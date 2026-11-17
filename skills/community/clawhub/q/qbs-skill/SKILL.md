---
name: "qbs-skill"
slug: "qbs-skill"
displayName: "QBS Skill 拷问书籍方法论"
description: "拷问书籍方法论：把卡住的问题经「拷问收敛→找书→完整读章→三重验证蒸馏→合成Skill→真实试跑」六阶段，产出有书籍出处、可验收的Skill。说「拷问书籍方法论」时触发。Do NOT use for 改进已有skill、无需读书依据的问答、古籍建库。"
version: "1.0.0"
license: "MIT-0"
summary: "Question→Book→Skill 升级版六阶段流水线：grilling设计树拷问收敛问题规格书，自依赖完成找书漏斗、完整读章、三重验证蒸馏、子Skill合成与验收试跑。"
allowed-tools: "Read, Write, Edit, Glob, Grep, LS, WebFetch, WebSearch, AskUserQuestion"
metadata:
  openclaw:
    skillKey: "qbs-skill"
    emoji: "📚"
    homepage: ""
    os: ["windows", "macos", "linux"]
    requires:
      bins: []
      env: []
    primaryEnv: ""
    envVars: []
    always: false
---

# 拷问书籍方法论 · QBS Skill

> 先把问题拷问到收敛，再让书来回答，最后把答案锻造成技能。
> 方法论血统：QBS 流程（Question→Book→Skill）的阅读纪律与反幻觉合约 × grilling 设计树拷问机制，全部内化自依赖。

## 何时触发

**触发词**：「拷问书籍方法论」

**适用场景**：
- 用户有一个**卡住的问题**（通常在陌生领域），想要一个有书籍依据、可独立调用、真实试跑过的 Skill
- 用户想"带着问题找书做 skill"、"把某本书的方法变成 skill"

**Do NOT（不触发）**：
- 改进/评估已有 skill → 走对应改进流程
- 无需读书依据的普通问答
- 古籍/方志建库（有专用流程）
- 论文写作执行、润色、投稿

## 任务

六阶段流水线，**阶段不可跳越，每阶段产物是下一阶段的输入**：

```
用户卡住的问题
 ①拷问 Grill —— 设计树×前沿轮次拷问，产出「问题规格书」
   ↓ question-spec.md（找书契约+验收契约 二合一）
 ②找书 Book —— 四层漏斗收敛，产出选书决策
   ↓ book-decision.md（首选书+选读章节+理由）
 ③取文读章 Read —— 取正文+核验五项+完整读章
   ↓ source-notes.md（阅读记录+方法-原文映射）
 ④蒸馏 Distill —— L1/L4/L5 三层提取+三重验证
   ↓ methods.md（七字段方法单元表）
 ⑤合成 Synthesize —— 4+1 模块组装子 Skill
   ↓ 子 SKILL.md + references/
 ⑥试跑回书 Test —— 用①的验收契约跑新任务，交付+回书入口
```

各阶段执行协议：
- ① 见 [references/grill-protocol.md](references/grill-protocol.md)（五分支设计树 / 前沿轮次 / 事实与决策分界 / question-spec 模板）
- ②③ 见 [references/book-and-reading.md](references/book-and-reading.md)（四层找书漏斗 / 可读性核验五项 / 完整读章纪律 / 阅读记录模板）
- ④⑤ 见 [references/distill-and-synthesize.md](references/distill-and-synthesize.md)（三层提取 / V1-V3 三重验证 / 七字段 / 归属三分 / 4+1 组装模板 / status 分级）

## 输出格式

| 交付 | 用户可检查什么 |
|---|---|
| 可独立调用的子 Skill | 何时用/需要什么输入/按什么步骤/交什么结果/何时不用 |
| question-spec.md | 拷问收敛出的问题规格与验收契约 |
| source-notes.md | 实际读了哪本书哪些章节，规则与原文位置的映射 |
| 试跑证据 | 输入是什么、方法怎么用、哪些验收项通过/未通过 |
| 回书入口 | 用到的方法在书里哪里、值得继续读什么 |

运行产物落盘到 `qbs-runs/<run-slug>/`；产出 Skill 登记到 [references/library.json](references/library.json)。

## 规则

1. **阶段不可跳越**：找到书名不能直接生成 Skill；读到序言不算读完正文。
2. **缺口诚实**：拿不到正文就报告缺口（缺哪本书哪几章），禁止"读序言也足够"式搪塞；不得悄悄换书。
3. **归属三分**：每条规则标注 `[书]`来源概括 / `[书→推]`根据来源的推断 / `[设计]`场景设计；`[设计]` 不得冒充书籍方法。
4. **三重验证**：方法单元必须过 V1 跨域（≥2处独立佐证）/ V2 预测力 / V3 独特性，未通过不得进入合成。
5. **验收闭环**：⑥试跑必须用①规格书锁定的验收标准，不得现场现编；证据不足以支撑任何贡献类型时输出停机报告，禁止强行包装。
6. **不虚构执行**：搜索/阅读/下载必须实际调用工具，失败如实说；阅读记录不得预填。

## 示例

**输入**："拷问书籍方法论。我想把 AI 协作项目的发现写成能发表的论文，但不知道怎么立论。"

**执行轨迹（摘要）**：
1. ①拷问 2 轮：收敛出根因=论证构造卡点、现象域=empirical SE、试跑素材=定时任务运维记录、验收=paper skeleton 级 → question-spec.md
2. ②找书：本地书库 0 命中 → 网络核验 → 首选《The Craft of Research》4th ed.（选书三问逐本回答）
3. ③读章：下载 340 页扫描 PDF → OCR → 完整读 Ch4/7/8/9/10 五章 → source-notes.md 含方法-原文位置映射
4. ④蒸馏：12 个方法单元过三重验证（三步公式/So what 递归/claim 六分类/证据四准则/12 问审问…），4 个候选淘汰并记录原因
5. ⑤合成：章节级轻量路线组装出「论文骨架锻造」子 Skill（4+1 模块+诚实边界）
6. ⑥试跑：用验收契约跑真实运维记录 → paper skeleton 交付，5 条验收 4 过 1 部分通过（证据缺口如实标注）

## 故障排除

| 症状 | 处置 |
|---|---|
| 本地书库检索工具不可用 | 跳过本地层，直接网络核验层（见 book-and-reading.md 漏斗设计，各层可独立降级） |
| PDF 无文字层（扫描版） | 用环境中可用的 OCR 能力转文本；OCR 质量不足时如实报告，不硬读 |
| 正文拿不到 | 触发规则 2：报告缺口清单（需要的文件/访问/购买决定由用户拍板） |
| 用户说"别问了直接做" | 按 grill-protocol.md §六捷径条款处理：按推荐答案落定并标注未经确认，但验收契约必须显式让用户过目 |
