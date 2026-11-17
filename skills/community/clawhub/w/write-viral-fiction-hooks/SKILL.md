---
name: write-viral-fiction-hooks
description: Generate viral Chinese short-fiction opening hooks and concise micro-fiction copy from a scene idea. Use when the user says "帮我生成开篇导语" or asks for five selectable opening leads, short-novel hook options, opening-guide variants, or a final Chinese fiction copy under 200 characters based on a scene inspiration.
---

# Write Viral Fiction Hooks

## Workflow

1. Read the user's scene inspiration and infer the core genre, protagonist, relationship, danger, secret, and emotional wound.
2. If the scene inspiration is missing, ask the user for one concrete scene in one sentence.
3. Provide exactly five opening-hook options first. Do not write the final copy yet unless the user explicitly asks to skip selection.
4. Give each option a clear type name, a 60-120 Chinese-character opening, and a one-line note naming the main hook.
5. Ask the user to choose one option or ask for a blend.
6. After the user chooses, generate one final Chinese fiction copy within 200 Chinese characters.

## Five Opening Types

Use these five types by default, adapting them to the user's scene:

1. **Death Warning / Impossible Event**: Start with a precise, impossible danger, such as a death call, prophecy, body double, missing memory, or message from someone who should not be able to speak.
2. **Betrayal Plus Inner Reversal**: Start with a cold breakup, humiliation, abandonment, or forced plot beat, then reveal a contradictory inner voice, system rule, secret affection, or unwilling performance.
3. **Folk Suspense / Taboo Object**: Start with a grounded village, family, funeral, ritual, craft, object, or rule, then insert one detail that makes the ordinary scene unsafe.
4. **Old Love Reunion / Hidden Sacrifice**: Start with regret, public reunion, class reversal, or an ex-lover's success, then reveal a scar, debt, illness, promise, or sacrifice that redefines the breakup.
5. **Identity Misread / Power Reversal**: Start with the protagonist being underestimated, replaced, mocked, or discarded, then reveal an identity, contract, inheritance, memory, or witness that flips the power balance.

## Style Rules

- Write in Chinese unless the user asks otherwise.
- Prefer first-person narration with immediate action.
- Make the first sentence short and sharp.
- Put the contradiction within the first three sentences.
- End each option on a question, revelation, or emotional cliffhanger.
- Use concrete roles and objects instead of abstract setup.
- Keep names sparse. Use relationships like "老公", "男友", "前任", "我爷", "继妹", or "老板" when they create faster tension.
- Let the scene imply genre. Avoid explaining the genre label inside the prose.
- Avoid hashtags, marketing slogans, moral summaries, and long backstory.
- Avoid generic lines like "她不知道的是" unless the user specifically wants a platform-style teaser.

## Output Format

For the first response after the trigger phrase:

```markdown
下面是五种开篇导语方向：

1. 类型名
导语：...
钩子：...

...

你想选哪一种？也可以说"混合 2 和 4"。
```

For the final selected copy:

```markdown
最终文案：
...
```

Do not exceed 200 Chinese characters in the final copy. If character count is uncertain, revise shorter before answering.

## Reference

Read `references/opening-patterns.md` when the user asks to match the provided example file closely, when the scene is vague, or when a stronger set of type distinctions is needed.
