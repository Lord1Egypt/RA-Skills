# 资鉴问道 · Zijian Wendao

> **借古喻今的人生抉择推演** ｜ History-grounded decision counseling
> 以《资治通鉴》《史记》为镜，照见你当下的抉择。
> *Hold up The Zizhi Tongjian and The Records of the Grand Historian as a mirror to your present decision.*

<p>
<img alt="license" src="https://img.shields.io/badge/license-CC%20BY--NC--SA%204.0-lightgrey">
<img alt="cases" src="https://img.shields.io/badge/cases-187-blue">
<img alt="source" src="https://img.shields.io/badge/source-史记%20·%20资治通鉴-orange">
</p>

**中文** ｜ [English（SKILL.en.md）](SKILL.en.md)

---

## 这是什么 ｜ What it is

**中文**：当一个人站在岔路口（要不要离开、信不信他、进还是退、守还是变），历史里往往已经有人做过"内核一模一样"的选择，并且付过代价。「资鉴问道」把这些选择——**连同代价**——端到面前：把当下的处境抽象成"抉择原型"，检索《史记》《资治通鉴》中场景内核相似的历史抉择案例，拆解古人当时的可选项、实际抉择、结果、显性代价与隐性代价，标注原文出处，最后给出启发与风险提醒。

它不是算命，不是鸡汤，也不是"历史总会重演"的宿命论。它只做一件朴素的事：**让你在别人的结局里，看见自己选择的代价。**

**English**: When you stand at a crossroads — leave or stay, trust or doubt, advance or retreat, hold or change — history has usually already shown someone making a structurally identical choice, and paying for it. **Zijian Wendao** lays those choices *and their costs* in front of you: it abstracts your situation into a "decision archetype", retrieves structurally similar decisions from *The Zizhi Tongjian* and *The Records of the Grand Historian*, and dissects each case into the options available, the choice actually made, the outcome, the visible costs and the hidden costs — with original-text citations — before drawing out transferable lessons and risk warnings. It is not fortune-telling, not motivational fluff, and not the fatalism of "history always repeats itself".

## 三条立身之本 ｜ Three principles

1. **案例必须真，原文必须实。** / *Real cases, faithful quotations.* Every classical citation is traceable to a specific chapter/volume, verbatim.
2. **代价必须讲全，尤其是隐性代价。** / *Count every cost — especially the hidden ones* (trust, loyalty, reputation, blowback).
3. **边界必须说清。** / *State the limits.* History is a frame of reference, not a verdict. It does not make the decision for you.

## 工作流 ｜ Workflow (7 steps)

接住问题 → 抽象"抉择原型" → 映射主题 → 检索案例 → 精选 2–4 例（含反面案例）→ 统一模板拆解 → 照见当下（对照 + 原则 + 风险 + 自问清单）。

*Intake → abstract a decision archetype → map themes → retrieve cases → select 2–4 cases (including counter-examples) → dissect each with a fixed template → reflect back on the present decision.*

## 仓库结构 ｜ Repository structure

```
├── SKILL.md                 # 技能主体（中文）：方法论 · 工作流 · 输出格式 · 示例
├── SKILL.en.md              # English version of the skill
├── LICENSE                  # CC BY-NC-SA 4.0（官方条款全文 / official legal code）
├── README.md                # 本文件（中英双语 / bilingual）
└── references/
    ├── 案例索引.md            # 187 案例 · 主题索引 + 按出处总目录
    ├── cases/                # 187 案例全文，14 册（史记 5 + 通鉴 9）
    ├── 篇卷索引.md            # 《史记》130 篇 + 《资治通鉴》294 卷 清单
    └── _design/提炼规范.md     # 案例模板与 25 个固定主题标签（供扩充）
```

## 案例库 ｜ Case library

- **共 187 个历史抉择案例**，覆盖《史记》（本纪 / 世家 / 列传）与《资治通鉴》（周纪—后周纪）。
- 每条含：情境 / 可选路径 / 实际抉择 / 结果 / **显性代价** / **隐性代价** / **原文出处** / 决策要点 / 风险提醒。
- 主题标签（25 个）：创业与守成 · 用人与识人 · 进退去留 · 结盟与背叛 · 危局突围 · 事上之道 · 谏诤与纳言 · 取舍与代价 · 知止与贪念 · 忍与争 · 信任与猜忌 · 复仇与宽恕 · 义利之辨 · 功成身退 · 改革与守旧 · 择主而事 · 言行与祸福 · 成事与避祸 · 家族与传承 · 危机决策 · 面子与里子 · 长期主义 · 识时务 · 忠与变通 · 势与时机

## 用法 ｜ Usage

- **作为 ima.copilot / OpenClaw 技能**：将本仓库作为技能目录导入（中文入口 `SKILL.md`，英文入口 `SKILL.en.md`）。
- **直接阅读**：从 `references/案例索引.md` 进入，按主题或出处查找。
- **作为 AI 提示词框架**：`SKILL.md` 中的七步工作流与输出模板可直接用于任何 LLM。

*Use it as a skill (Chinese entry `SKILL.md`, English entry `SKILL.en.md`), read `references/案例索引.md` directly, or reuse the 7-step workflow as a prompt framework for any LLM.*

## 数据来源 ｜ Sources

- 《史记》：《史记》简体全文（含白话译文），底本整理自公开的二十四史简化项目。
- 《资治通鉴》：《资治通鉴》简体文白对照全文，共 294 卷，整理自公开文本数据。
- 案例由 AI 辅助从两书原文中蒸馏提炼；**每条原文引用均逐字核对、可溯源**；底本中查无的桥段一律标注留白，不作杜撰。

*Texts of both classics are in the public domain. The distilled case library and this skill are the curator's original work.*

## 声明 ｜ Notes

- 本技能提供的是**历史参照**，不构成投资、法律、医疗或任何专业建议。
- 历史类比有其边界：它增加见识，不决定结局。**最后的决定权，始终在你手里。**

## 授权 ｜ License

本项目采用 **CC BY-NC-SA 4.0**（署名—非商业性使用—相同方式共享）；完整条款见 [`LICENSE`](LICENSE)。
《史记》《资治通鉴》原文属公有领域。

*Licensed under CC BY-NC-SA 4.0 — see [`LICENSE`](LICENSE). The classical texts are public domain.*
