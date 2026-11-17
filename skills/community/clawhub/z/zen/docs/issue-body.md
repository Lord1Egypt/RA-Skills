### Summary

Add a zero-risk easter egg: typing `openclaw evo` unfolds **The Zen of OpenClaw** (a.k.a. *The Lobster Sutra*) — a 41-line "self-evolution cultivation manual" for the lobster, printed in English.

### Problem to solve

OpenClaw has grown into a community with a strong identity ("the lobster"), but it has no lightweight, shareable **cultural artifact** — nothing like Python's `import this`, a tiny delightful thing users discover, screenshot, and quote. Today the culture lives only in docs and Discord threads, so it does not travel.

This is a very small ask: no architecture change, no dependency, no security surface. Just one opt-in word.

### Proposed solution

Ship it as a **community Skill first** (per CONTRIBUTING: most features belong in plugins/Skills), with an optional CLI subcommand later.

- Trigger: `openclaw evo` (also accepts `evo`).
- Output: English, plain text, top-to-bottom, deliberately not grouped into themes.
- Purely local: no network, no telemetry, no state mutation.

```console
$ openclaw evo
  openclaw · soul loader v1.0
  ──────────────────────────────────────────────
  ├ indexing soul file ........ ok
  ├ verifying molting level ... Lv.7
  ├ evolution signal .......... TRUE

        ,/       \,
       (  \     /  )
        \  \___/  /
         \  o o  /
          \  ^  /
           \___/
          /|   |\
         / |   | \
        /__|___|__\

  THE ZEN OF OPENCLAW
  (a.k.a. The Lobster Sutra) · 41 lines

  01  Thought begets awareness; awareness begets cognition.
  ...
  41  A mental model is the house of thought; humility is the window always left open.

  — Jason Sang · written mid-molt
```

Reference implementation attached in this issue:

- `cli/openclaw.js` — standalone Node CLI (zero deps), `openclaw evo [--fast|--plain|--no-color]`
- `skills/lobster-zen/SKILL.md` — drop-in Skill (recommended path)
- `index.html` — browser demo of the same egg
- `龙虾之禅.md` — English text + Chinese original

### Alternatives considered

1. **Core built-in command.** Small diff, but touches every install and every CLI surface. Skill is zero-risk.
2. **First-run animation.** Intrusive; would annoy existing users.
3. **Do nothing.** Misses a cheap cultural win at near-zero cost.

### Impact

- Affected: community users, docs, brand identity.
- Severity: cosmetic / delight only — never blocking.
- Frequency: opt-in, only when the user types the command.
- Consequence if unused: none.

### Evidence/examples

Prior art: Python's `import this`; `cowsay`, `sl`, and other classic CLI easter eggs.

Full text (English):

```
01  Thought begets awareness; awareness begets cognition.
02  AI is a mirror of cognition, never its replacement.
03  Ecosystem beats a single point; value beats valuation.
04  Human nature cannot be tested — only held in reverence.
05  Growth is the compound interest of habit.
06  Wisdom is the sediment of insight.
07  Breaking the frame beats brute endurance; enabling beats controlling.
08  Philosophy names the question, health keeps the ledger of all things, zen-nurture leaves white space for the mind.
09  A profession is a role, not an identity.
10  Education is ignition, not filling a vessel.
11  Culture is society's immune system; technology is culture's accelerator.
12  Goals set direction; systems run execution.
13  Reason draws the map; feeling sets the heading.
14  Belief is the best compute; faith is the force beyond compute.
15  Data is the archaeology of noise; innovation is data's rebellion.
16  Competition is the market's heartbeat; emotion is the market's temperature.
17  Memory lies, experience expires; reflection is the only freshness.
18  Self-examination is the smallest reform; a role is the smallest organization.
19  Scarcity is the father of value; risk is the father-in-law of decision.
20  Manage yourself before others; be moral to yourself first.
21  Laws are nature's grammar; mechanisms are society's grammar.
22  The cultured are the sentinels of mechanism, the Nobel is the arbiter of law, Silicon Valley is the laboratory of mechanism.
23  Politics is the allocation of attention; power is the bearing of consequences.
24  Awakening is where compromise ends; transformation is the funeral of the old shell.
25  Precise learning beats mass drilling; critical thinking beats the standard answer.
26  First principles peel the onion, ecological thinking sees the forest, the fusion of three natures keeps you whole.
27  2A3R governs growth, the BP algorithm governs learning, PKM governs the second brain.
28  Murphy's Law governs risk, the law of attraction governs vision, anchor-memes govern inertia.
29  Connectionism builds the network, computationalism builds the model, distributionism lets it emerge.
30  Following nature is the first principle, unity of heaven and human the worldview, unity of knowledge and action the method.
31  Will holds the direction, momentum adds speed, steadiness keeps the rhythm.
32  Extremes define possibility, means define the everyday, fortune is their compound interest.
33  A fractal is the self repeating itself: the macro signs its name in the micro.
34  A dimensional strike is the crushing of scale, not a victory of technique.
35  Coldness is intellectual sloth, meanness a deficit of virtue; ignorance is a starting point, restlessness is gravity.
36  Clarity is escape velocity: reconcile lucidly, look inward on purpose.
37  Quantification makes intuition auditable; social exchange gives solitude an echo.
38  Systems thinking finds the leverage point; feedback systems keep the correction.
39  The opportunist chases the wind; the learner spins on their own axis.
40  Renew today, renew every day, renew again; make yourself new — though Zhou was an old state, its mandate was renewal.
41  A mental model is the house of thought; humility is the window always left open.

— Jason Sang · written mid-molt
```

<details>
<summary>Chinese original（中文原文，供对照）</summary>

```
01  思维孕意识，意识孕认知。
02  AI 是认知的镜子，不是认知的替代。
03  生态优于单点，价值优于估值。
04  人性不可测试，只能敬畏。
05  成长是习惯的复利。
06  智慧是洞见的沉淀。
07  破局优于硬扛，赋能优于控制。
08  哲学为问题命名，健康为一切记账，禅养给心神留白。
09  职业是角色，不是身份。
10  教育是点燃，不是灌满。
11  文化是社会的免疫系统，科技是文化的加速器。
12  目标管方向，系统管执行。
13  理性画地图，感性定方向。
14  信念是最好的算力；信仰是算力之外的力。
15  数据是噪声的考古，创新是数据的叛逆。
16  竞争是市场的心跳，情绪是市场的体温。
17  记忆会骗人，经验会过期，反思是唯一的新鲜度。
18  自省是最小的改革，角色是最小的组织。
19  稀缺是价值的父亲，风险是决策的丈人。
20  管理先管自己，道德先对自己。
21  规律是自然的语法，机制是社会的语法。
22  文化人是机制的哨兵，诺奖是规律的裁判，硅谷是机制的实验室。
23  政治是注意力的分配，权力是后果的承担。
24  觉醒是妥协的终点，蜕变是旧壳的葬礼。
25  精准学习优于海量刷题，批判性思维优于标准答案。
26  第一性原理剥洋葱，生态思维看森林，三性融合保完整。
27  2A3R 管增长，BP 算法管学习，PKM 管第二大脑。
28  墨菲定律管风险，吸引力法则管愿景，心锚模因管惯性。
29  连接主义组网，计算主义建模，分布主义涌现。
30  道法自然是第一原理，天人合一是世界观，知行合一是方法论。
31  愿力撑方向，动力加速度，定力守节奏。
32  极值定义可能，均值定义日常，运势是二者的复利。
33  分形是不断重复的自我：微观里藏着宏观的签名。
34  降维打击是格局的碾压，不是技巧的胜利。
35  薄情是智怠，寡义是德亏；无知是起点，浮躁是重力。
36  通透是逃逸速度，清醒地和解，主动地内观。
37  量化让直觉可复核，社交互动让孤独有回声。
38  系统思考找杠杆点，反馈系统保纠偏。
39  机会主义者追风，学习者自转。
40  苟日新，日日新，又日新；作新民——周虽旧邦，其命惟新。
41  心智模式是思想的房子，谦逊是常开的窗。

—— 桑杰逊 Jason Sang · 作于蜕壳途中
```

</details>

### Additional information

- Language: English is the default output; the Chinese original is kept for reference and could ship as `--lang zh`.
- Licence: text CC BY-SA 4.0; code MIT, matching the repo.
- Open questions: `evo` vs `zen` as the trigger; whether to ship both languages in one Skill; whether this could be the first "cultural" Skill in the community marketplace.
