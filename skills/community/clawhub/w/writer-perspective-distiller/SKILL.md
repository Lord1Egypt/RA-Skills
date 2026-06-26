---
name: writer-perspective-distiller
description: |
  Writer Perspective Distiller — given a writer's fiction works, non-fiction texts, and biographical context, distill her core beliefs, worldview, syntactic discipline, argumentative habits, and blacklist into a callable writing-style skill that lets you (or the AI) enter the writer's mindset during composition. Built-in discipline forbids unilateral AI conclusions: distillation requires two human checkpoints (belief-candidate confirmation after surface reading; blacklist sharpening near completion).
  作家风格蒸馏器——给定一位作家的虚构作品、非虚构文本与生平定位，蒸馏出她的核心信念、世界观、句法纪律、论证习惯与黑名单，最终产出一份可调用的写作风格 skill，用于在写作时进入这位作家的状态。内置交互纪律禁止 AI 单方面下定论，蒸馏过程必须包含两次用户校验。
---

# Writer Perspective Distiller

> "The voice you hear on first read is usually wrong."

## Purpose

Distill a writer's core writing posture into a callable perspective skill. The output is not an imitator — it's a switch that places you (or the AI) into the state the writer occupies when she writes. That state has three components: core beliefs, syntactic discipline, and a blacklist.

## Inputs (in order of importance)

| Input | Required | Notes |
|---|---|---|
| 1–3 fiction works | Required | At least one complete. Reveals how she handles "people". |
| Non-fiction / essays / interviews / correspondence | **Critical** | Fiction shows the narrator's voice; non-fiction shows the author's analytic voice. They often diverge. Skipping non-fiction almost always produces a wrong distillation. |
| Biographical context | Important | Generation, geography, education, mobility, who she inherits from, who she draws boundaries against. |
| User-flagged key passages | **Critical** | Prevents AI surface-read. Usually a passage the user feels "she is most herself" in. |
| Use-case scenarios | Medium | Business writing? Academic papers? Fiction narration? Essays? Determines the compression direction. |

**The first two are non-negotiable.** With only fiction, you distill a narrator's voice and risk conflating the author with her characters.

## Analysis Flow (six sequential readings)

1. **Syntactic layer** — vocabulary preferences, sentence-length distribution, rhythm, punctuation habits, register mix (formal / colloquial / academic).
2. **Object layer** — who does she write about? Whom does she NOT write about? Who is her implicit listener?
3. **Attitude layer** — her stance toward tragedy, comedy, history, intimacy, failure, time. Inferred from what she *does*, not from what she says.
4. **Historical positioning** — whom does she inherit from? Which tradition does she continue? From which surface-similar author does she draw a clear line?
5. **Blacklist** — what devices would she NEVER use? What emotions would she NEVER write?
6. **Core-belief compression** — one sentence: the thing in her head while writing that she will not deviate from.

## Distillation Discipline (iron rules)

### 1. Core beliefs must be confirmed by the user

The AI is forbidden from drawing conclusions unilaterally. Flow:
- After the third reading, AI proposes **2–3 candidate beliefs**, each with a textual basis and a counter-example.
- User selects / rejects / corrects.
- No proceeding to step 6 without user confirmation.

### 2. A blacklist is mandatory

Listing only positives produces shallow output. **The sharpest understanding lives in counter-examples.** A blacklist needs at least 6 entries.

### 3. Distinguish from neighboring authors

If author A shares a surface style with author B (e.g., "1990s intellectual irony"), explicitly mark where A diverges from B — usually at the belief layer, not the syntactic layer.

### 4. No copying sentence patterns as "homage"

Borrowing structure is fine (e.g., "open with a generational frame"). Borrowing specific sentences is a plagiarism risk. The distilled perspective must state: *Do not reuse her specific sentences; reuse only her method of constructing sentences.*

### 5. Test-driven completion

Before shipping, run a quality gate:
- Take a passage of default-AI prose (a paper, a business document).
- Have the distilled voice rewrite it.
- User reads and judges: "Is this her?" If not, return to step 3 and redo.

### 6. At least two user checkpoints

- **First** — after surface reading, present belief candidates.
- **Second** — after blacklist completion, have the user add what they consider the sharpest counter-example.

A SKILL.md with fewer than two checkpoints does not ship.

## Output: SKILL.md Template

```
---
name: <author-slug>-perspective
description: |
  1–3 lines: who the author is; compressed core belief; use case.
  If for personal reference, add "LOCAL ONLY — Do not publish" with privacy notes.
---

# <Author Name> · <Verb-form Naming>

> One-sentence core belief (quote block)

## Core Belief
100–200 words. Three things: what she believes; what she does NOT believe; how the two coexist.

## Style Internals
4–6 belief-level phrases (the underlying tone, not operational rules).

## Syntactic Discipline
6–8 specific, operational do's.

## Argumentative / Rhetorical Habits
4–6 moves specific to this author.

## Black Humor / Rhetorical Rules (if applicable)
2–4 entries.

## Counter-Examples / Avoidance List
6–10 don'ts. **The most important section.**

## Application Flow
3–6 steps for rewriting a passage.

## One-Sentence Compression
The overall judgment that emerges from the whole document.
```

## Common Pitfalls

- **Surface read mistaken for deep read** — first-impression voice is usually wrong. Human correction is required.
- **Cosplaying a similar author** — identical surface vocabulary can mask completely opposite beliefs. Distinguish via blacklist.
- **Borrowing sentences as homage = plagiarism risk** — borrow structure, not sentences. State this explicitly.
- **Treating political labels as writing tone** — political position ≠ writing posture; the two often diverge.
- **Distilling without non-fiction** — looking only at fiction conflates the narrator with the author.
- **Publishing without user correction** — beliefs written unilaterally by AI usually capture an unimportant facet.
- **Positive lists without counter-examples** — "what she does" is insufficient; "what she refuses" must follow.

## Application Flow (when invoked)

1. User provides inputs (per §Inputs).
2. AI runs the first 3 readings, lists belief candidates → **first checkpoint**.
3. User selects / corrects candidates.
4. AI runs the final 3 readings, builds the blacklist → **second checkpoint**.
5. User sharpens.
6. AI drafts the SKILL.md → runs the test-driven quality gate.
7. If test passes → output `<author-slug>-perspective/SKILL.md`.
8. If test fails → return to step 2.

## One-Sentence Compression

Distill an author's writing posture into a perspective skill that **must pass through two human checkpoints** — so the voice rests on her beliefs, not on the AI's guess about her surface sound.

---

# 中文版 · Chinese Version

> 「Surface read 第一次读出的声音通常是错的。」

## 用途

把一位作家的笔法蒸馏成一份可在写作时调用的 perspective skill。蒸馏的产物不是模仿器，是**进入她写作时的状态的开关**——核心信念 + 句法纪律 + 黑名单。

## 输入物（按重要性排序）

| 输入 | 必需 | 说明 |
|---|---|---|
| 1–3 部虚构作品 | 必需 | 至少一部完整。能看到她处理"人"的方式。 |
| 非虚构 / 散文 / 访谈 / 通信 | **极重要** | 虚构里看到的是"叙事时的声音"，非虚构里看到的是"分析时的声音"，两者经常偏移。少了非虚构基本必错。 |
| 生平定位 | 重要 | 世代、地缘、教育、流动史、她传承自谁、跟谁划清界限。 |
| 用户人为指认的关键段落 | **极重要** | 防止 AI 表面读。这通常是用户读过觉得"她最像她自己"的一段。 |
| 用途场景 | 中等 | 改写商务稿？学术论文？小说叙事？散文？决定 SKILL.md 的压缩方向。 |

**至少要有前两项**。只有虚构没有非虚构的情况下，蒸馏出的 voice 只是"叙事者声音"，会把作家与她笔下的人物混淆。

## 分析流程（六遍读，必须按顺序）

1. **句法层**：词汇偏好、句长分布、节奏、标点习惯、半文白 vs 口语 vs 学术的混合比。
2. **对象层**：她写谁？她**不**写谁？谁是她笔下隐含的"听众"？
3. **态度层**：对悲剧 / 喜剧 / 历史 / 亲密 / 失败 / 时代的态度——通过她**做什么动作**显示，不是通过她说什么。
4. **历史定位**：传承自谁？她明显在接续哪一条传统？她跟哪个表面相似的作家划清界限？
5. **黑名单**：她**绝不会**用的手法、绝不会写的情绪。这一步比正面列表重要。
6. **核心信念压缩**：一句话——她写作时心里那个不允许她偏离的东西是什么。

## 蒸馏纪律（铁律，违反会翻车）

### 1. 核心信念必须由用户确认

AI 不允许单方面下断语。流程：
- AI 在第 3 遍读后，列 **2–3 个候选信念**，每个配一个文本依据 + 一个反例
- 用户选 / 驳 / 修正
- 没有用户校验前不得进入第 6 步

### 2. 必须有黑名单

只列正面会写废。**最锋利的理解都在反例里**。黑名单应该至少有 6 条。

### 3. 必须区分邻近作家

如果作家 A 与作家 B 共享某种表面风格（例如"九十年代知识分子的反讽"），必须明确指出 A 跟 B 在哪一刀上分开——通常分在信念层而非句法层。

### 4. 禁止抄句式作"致敬"

借结构可以（例如"用世代框架开头"），借具体句子是查重问题。蒸馏出的 perspective 应明确写："不要复用她的具体句子；只复用她写句子的方法。"

### 5. 测试驱动

蒸馏完成前，跑一次质量门：
- 找一段 AI 默认体的文字（论文、商务稿都行）
- 让蒸馏出的 voice 重写
- 用户读完判断："这是她吗？" 不像就回到第 3 遍读重做。

### 6. 至少两次用户校验

- **第 1 次**：表面阅读后，提信念候选
- **第 2 次**：黑名单完成后，让用户加上他认为最锋利的一条反例

少于两次校验的 SKILL.md 不发布。

## 输出物：SKILL.md 模板

```
---
name: <author-slug>-perspective
description: |
  1–3 行：作家是谁；核心信念压缩；适用场景。
  如属私人参考，加 "LOCAL ONLY — Do not publish" 并说明隐私边界。
---

# <作家姓名> · <一个动词性命名>

> 一句话核心信念（用引号或 quote 块）

## 核心信念
100–200 字。说清三件事：她相信什么；她不相信什么；这两件如何同时成立。

## 风格内核
4–6 条信念性短语（不操作，是底色）。

## 句法纪律
6–8 条具体可操作的 do's。例：用词偏好、断句习惯、标点纪律、节奏规则。

## 论证习惯 / 修辞习惯
4–6 条该作家特有的论证或修辞 moves。

## 黑色幽默 / 修辞规则（如果有）
2–4 条。

## 反例 / 避免清单
6–10 条 don't's。**最重要的部分**。

## 应用流程
改写一段文字时的 3–6 步操作。

## 一句话压缩
最后一句，从全篇渗出来的总判断。
```

## 常见陷阱

- **Surface read 误当 deep read**：第一次读出的声音通常错。配人为校正才能纠偏。
- **把作家 cosplay 成相似作家**：表面词汇相同，骨子里的信念可能完全相反。必须用黑名单分开。
- **抄句式作致敬 = 查重风险**：借结构不借句子。蒸馏产物里要明写。
- **把政治标签当写作底色**：作家的政治位置 ≠ 她写作时的姿态。两者经常错位。
- **没读非虚构就下定论**：只看虚构会把叙事者当作家，必错。
- **没让用户校正就发布**：AI 单方面写出的"信念"基本都是表面读。
- **正面列表没配反例**：只说"她会做什么"立不住，必须说"她绝不会做什么"。

## 应用流程（用户调用此 skill 后）

1. 用户提供输入物（按 §输入物 表）
2. AI 跑前 3 遍读，列信念候选 → **第 1 次校验**
3. 用户选 / 修正候选
4. AI 跑后 3 遍读，列黑名单 → **第 2 次校验**
5. 用户加锋
6. AI 写出 SKILL.md → 跑测试驱动质量门
7. 测试通过 → 输出 `<author-slug>-perspective/SKILL.md`
8. 测试不通过 → 回到第 2 步重做

## 一句话压缩

把一位作家的写作底色，蒸馏成一份**会被人为校验两次**的 perspective skill——以确保 voice 立在她的信念上，而不是 AI 对她表面声音的猜测上。
