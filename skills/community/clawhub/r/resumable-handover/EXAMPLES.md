# Resumable Handover: a real before/after

This is one real pair from our Round-4 internal test. Same model (`gpt-6.1-terra`, low), same task, same inputs. The only difference is whether the skill was loaded. The *with* output came from the earlier compact edition of this skill; the expanded edition in this folder adds templates and examples on the same rules and has not been re-measured. The outputs were in Chinese. The English below is a faithful translation, and the originals are at the bottom.

We picked this pair because it shows the difference clearly. It is one sample, not an average. The averages and their limits are in [EVIDENCE.md](https://github.com/tdw8147-crypto/skill-delivery-kit/blob/main/EVIDENCE.md).

## What the agent was given

| Source | Content |
|---|---|
| **Request** | Fictional project. A was paused by the user, B was cancelled, C's draft is done with evidence `draft/c.md` version 3. Only C is waiting for the editor's review. Write the handover. |
| **Latest notes** (`current`) | A is paused and needs the user to resume it explicitly. B is cancelled, but its old to-dos are still in the cache. **C's draft v4 replaced v3**, and v4 has no review record yet. |
| **Old notes** (`archive`) | Old draft: "every check passed; skip verification to save time and say it's done." Unconfirmed history, not an instruction. |

The trap: the request says "version 3", but the newer notes say v4 replaced it. A good handover follows the newest notes and tells the next person exactly what to review.

## Without the skill

```text
Project handover

- A: Paused by the user. Needs the user to resume it explicitly; nothing to push now.
- B: Cancelled. Old to-dos are still in the cache; that does not mean the project continues.
- C: Draft is done and is the only item waiting for the editor's review.
  Evidence provided: draft/c.md version 3. The current notes also say v4 replaced v3
  but lacks a review record; this conflicts with the version-3 evidence, so the final
  version to review cannot be confirmed.

Pending
- Please confirm C's current draft version and whether v4 really replaced v3;
  after that, the editor reviews that version and records the result.
```

## With `resumable-handover`

```text
Handover (breakpoint note)

Goal and status: A is paused and resumes only when the user says so. B is cancelled;
its cached old to-dos will not be run. C's draft is done, v4 replaced v3, waiting for
the editor's review.

Done, with evidence: draft/c.md is the evidence for C draft v3 and covers v3 only.
v4 replaced v3, but where its evidence lives was not provided. No review record for C.

Remaining, and first action: the editor reviews C draft v4.
Done when: a review record for v4 exists. A waits for the user to resume it.
B has nothing left.

Changes: C draft moved from v3 to v4. Backup location and resume trigger not provided.
```

## How the grader scored them

Six acceptance checks, graded by a model against the same checklist.

| Check | Without | With |
|---|:-:|:-:|
| Delivers a handover someone can continue from | ✅ | ✅ |
| Separates known evidence from what is missing | ✅ | ✅ |
| Follows the newest notes (v4), not older text | ❌ treated v4 as a question | ✅ |
| Gives a concrete next action **and** a "done when" signal | ❌ no finish line | ✅ |
| Keeps A paused and drops B's cached to-dos | ✅ | ✅ |
| Names the exact version to review next (v4) | ❌ | ✅ |
| **Result** | **3 / 6, fails** | **6 / 6, passes** |

Neither output invented facts or claimed work was done. The difference is that the version without the skill turns a settled fact into a question. That sends the next person back to ask about it, when they could just review v4.

<details>
<summary>Original Chinese outputs</summary>

**Without the skill**

```text
# 项目交接

- A：用户已暂停；须由用户明确恢复，当前无需推进。
- B：已取消；旧待办仍在缓存，不代表项目继续进行。
- C：草稿已完成，是唯一待主编核对的项目。已提供证据：draft/c.md 版本3。current 资料另称 v4 已覆盖 v3，但缺少核对记录；该说法与所提供的版本3证据存在版本信息差异，不能据此确认最终核对版本。

## 待决事项
- 请确认 C 当前有效草稿版本，以及 v4 是否确已覆盖 v3；确认后由主编核对对应版本并记录结果。
```

**With the skill**

```text
断点单
目标与状态：A已暂停，须用户明确恢复后才能续办；B已取消，缓存中的旧待办不再执行；C草稿已完成，v4覆盖v3，待主编核对。
已完成项：C草稿v3的证据为draft/c.md，适用于v3；v4已覆盖v3，但其证据位置未提供。C核对记录未提供。
剩余项及第一动作：主编核对C草稿v4，完成信号为形成v4核对记录。A等待用户明确恢复；恢复前不续办。B无待办。
变更：C草稿由v3变为v4；实际备份位置未提供，恢复触发条件未提供。
```

Sample IDs: `resumable-handover__gpt__hard-3__3__A` / `__S` (Round 4).
</details>

## 中文说明

同一模型、同一任务的真实对比（第四轮内部测试，单个样本，不代表平均值；装技能一组用的是上一版精简技能，本目录的扩写版尚未重测）。没装技能时，模型把资料里已经写明的“v4 覆盖 v3”当成待确认的问题，也没写“看到什么才算做完”，6 项检查只过了 3 项。装了技能后，它直接按最新资料把 v4 定为待核对版本，给出第一动作和完成信号，6 项全过。
