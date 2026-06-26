# writer-perspective-distiller

Distill a writer's writing posture into a callable perspective skill.

把一位作家的写作底色，蒸馏成一份可在写作时调用的 perspective skill。

---

## English

### What problem this solves

Getting an AI to "learn a writer's style" tends to drift: the voice you hear on first read is usually some surface facet of the author rather than her real underlying posture. Hand the distillation off to the AI and you get something that *looks* like her on the surface but is AI default underneath.

This skill imposes a distillation flow with **mandatory human checkpoints**:

- Non-fiction is required, not optional (so the narrator's voice isn't mistaken for the author's)
- Belief candidates must be confirmed by the user — the AI cannot conclude unilaterally
- A blacklist (what she would never write) is mandatory, not just a positive list
- Neighboring authors with surface similarity must be explicitly distinguished
- Before completion, a "test-driven" pass: have the distilled voice rewrite a piece of default-AI prose, and let the user judge whether it really sounds like her

### Output

A standalone SKILL.md (with optional README) containing:

- Core belief
- Style internals
- Syntactic discipline
- Argumentative / rhetorical habits
- Counter-examples / blacklist (the most important section)
- Application flow
- One-sentence compression

Drop it back into `~/.claude/skills/<author-slug>-perspective/SKILL.md` and call it during writing.

### Use cases

- Personal writing-style reference (an author you already know, whose state you want to enter for a particular piece)
- Building a citable, source-grounded voice for an organization or brand
- Shaping a narrator's voice for fiction
- Finding a non-default-AI tone for a paper, essay, or letter

### How to use

After invoking the skill, you'll be prompted to provide:

1. 1–3 fiction works by the author (at least one complete)
2. Non-fiction / essays / interviews / correspondence (**required** — without this, the distillation will not be accurate)
3. Biographical context (generation, geography, education, mobility)
4. One or two passages you flag as critical (to prevent AI surface-read)
5. Use-case scenarios (determines compression direction)

The skill then runs a 6-pass reading and analysis. It will pause **twice** for your confirmation, and finally output a SKILL.md ready to load.

### Design principles

- **First-read voice is usually wrong** — every quality gate is built around this
- **A blacklist matters more than a positive list** — saying only "what she does" doesn't hold up
- **Borrow structure, not sentences** — the distilled perspective must explicitly forbid copying her specific sentences
- **An author is not her characters** — non-fiction is the bridge to seeing this clearly

---

## 中文

### 它解决什么问题

让 AI 学一位作家的"风格"很容易跑偏：第一遍读出的声音通常是作家的某个表面侧面，不是她真正的写作底色；直接把蒸馏交给 AI，得到的多半是"看起来像她、骨子里是 AI 默认体"的产物。

这个 skill 用一套**强制带人为校验**的流程蒸馏：

- 必须有非虚构文本，不只看小说（防止把叙事者声音误当作家声音）
- 信念候选必须由用户确认，AI 不允许单方面下断语
- 必须列黑名单（她绝不会写的东西），不只列正面
- 必须区分邻近作家（表面相似但骨子里不同的那一类）
- 蒸馏完成前跑一次"测试驱动"——找一段 AI 默认体的文字让蒸馏出的 voice 重写，用户判断像不像她

### 输出物

一份独立的 SKILL.md（连同可选的 README），结构：

- 核心信念
- 风格内核
- 句法纪律
- 论证 / 修辞习惯
- 反例 / 黑名单（最重要）
- 应用流程
- 一句话压缩

可以装回 `~/.claude/skills/<author-slug>-perspective/SKILL.md`，在写作时调用。

### 用途场景

- 私人写作风格借鉴（已经熟悉的作家，想在某次写作里进入她的状态）
- 为某个组织或品牌建立有出处可考的 voice
- 为虚构作品塑造一位叙事者的声音
- 为论文 / 散文 / 书信寻找一个非 AI 默认体的语调

### 怎么用

调用此 skill 后，按提示提供：

1. 1–3 部该作家的虚构作品（至少一部完整）
2. 该作家的非虚构 / 散文 / 访谈 / 通信（**必需**——否则蒸馏不准）
3. 生平定位（世代、地缘、教育、流动史）
4. 你认为关键的一两个段落（防止 AI 表面读）
5. 用途场景（决定 SKILL.md 的压缩方向）

之后 skill 会带你跑一遍 6-pass 的阅读分析，**两次**停下来等你校验，最后输出可直接装载的 SKILL.md。

### 设计原则

- **Surface read 第一次读出的声音通常是错的**——所有质量门都为这一点准备
- **黑名单比正面列表重要**——只说"她会做什么"立不住
- **借结构不借句子**——蒸馏出的 perspective 应禁止抄她的具体句式
- **作家不等于她笔下的人物**——非虚构是看清这件事的桥梁

---

## License

MIT-0. No restrictions.
