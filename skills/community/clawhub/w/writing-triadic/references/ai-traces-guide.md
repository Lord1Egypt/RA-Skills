# 🚨 AI 痕迹高频特征避坑指南 (v2.7)

本指南旨在从词汇、结构、逻辑和**双语混淆**四个维度，精准打击大语言模型的"出厂设置味"。
执行者（Executor）需严格规避，读者（Reader）需以此为依据严厉扣分。

**v2.3 新增**：第 4 节 — 中英双语混淆检测
**v2.7 新增**：模板专属疲劳词表联动 — 以下为**全局通用**词表，各模板另有专属词表（见 template-library.md），
Executor 执行时自动注入"全局词表 + 当前模板专属词表"两层过滤。

---

## 1. 词汇与短语警戒线（高危词表）

只要出现以下词汇，立刻打破人类读者的沉浸感，需严格清洗。

### 英文灾区
`delve into`, `tapestry`, `testament`, `realm`, `landscape`, `Maps`, `unlock`, `symphony`, `crucial`, `foster`, `beacon`, `moreover`, `furthermore`, `additionally`, `underscores`, `highlights`, `stands as`, `serves as`, `acts as`, `it is worth noting that`, `it is important to`, `not only... but also...`

### 中文灾区

**陈词滥调**
"宛如一幅画卷"、"交织在一起"、"扬帆起航"、"毋庸置疑"、"不可或缺"、"织就"、"谱写"、"铸就"

**过度书面语**
"旨在"、"综上所述"、"在...的大背景下"、"不仅...更是一场..."、"其重要性不言而喻"

**机械发问**
"试想一下"、"你是否曾想过"、"那么，问题来了"、"让我们深入探讨"

**程度副词滥用**
频繁使用"极大地"、"深刻地"、"完美地"等缺乏具体数据支撑的空洞修饰词

---

## 2. 结构性 AI 模式（行文规律特征）

人类写作有呼吸感和参差感，AI 写作往往过于匀称。

### 对仗强迫症
每一段的字数惊人地相似，且都喜欢用一个短句开头。人类写作段落长短不一，长段后往往跟短句缓冲。

### 机械三段论
"首先...其次...最后..."或"一方面...另一方面..."，缺乏更自然的过渡。人类写作会用"更糟的是"、"话虽如此"、"但有意思的是"等非结构化过渡。

### "结尾升华"综合征 ⚠️ 最致命的 AI 特征
无论段落讲的是多小的事情，最后一句都要强行总结拔高，给出人生建议或行业展望。人类写作允许一个段落没有"意义"——信息传达到了就结束。

### 破折号与分号滥用
为了显得句子复杂，毫无必要地频繁使用"——"来解释说明。正常写作中 em dash 每 500 字不应超过 1 次。

### 所有段落等距等长
AI 倾向于每段 3-5 句，长度几乎相同。人类写作通常混合使用单句段、中段和长段。

---

## 3. 内容空洞信号（正确但无用的废话）

### 端水大师
"虽然 A 有很多优点，但我们也不能忽视 B 的重要性，关键在于找到平衡。"（说了等于没说）

### 时间遁词
"只有时间能给出答案"、"未来还有很长的路要走"

### 无意义的免责声明
"重要的是要记住..."、"值得注意的是..."

### 模糊归因
"专家表示"、"研究表明"、"数据指出"——如果没有具体引用，就是虚的

### 抽象名词撑场面
"the interplay of..."、"the tapestry of..."、"the evolving landscape of..."——用具体描述替代抽象概括

---

## 🆕 4. 中英双语混淆检测 (Bilingual Cross-Contamination — v2.3)

AI 在处理中英混排文本时容易出现两类反人类错误：**英文思维套中文句式**和**中文思维硬译英文**。以下为双向量表。

### 4.1 英文思维写中文 (English Brain in Chinese Body) ⚠️ 最隐蔽

这类错误不是单个错词，而是**整句的思维结构是英文的**，只是词的表面翻译成了中文。

#### 检测特征

| 模式 | 示例 (❌ 英文思维) | ✅ 中文自然表达 |
|---|---|---|
| **被动语态泛滥** | "这个问题可以被理解为..." | "这个问题可以这么理解..." |
| **无生命主语 + 有生命动词** | "数据告诉我们..." / "经验让我意识到..." | "我从数据里看到..." / "做了这么久，我发现..." |
| **It is + adj + that 结构的直译** | "值得注意的是..." / "令人惊讶的是..." / "需要指出的是..." | 直接陈述，省略铺垫 |
| **过度使用连接词作为句子开头** | "因此，..." / "然而，..." / "此外，..." / "尽管如此，..." — 几乎每段都来一个 | 用"所以"、"不过"、"还有"等口语连接词，或在逻辑够强时省略。人类写作的连接词密度远低于 AI |
| **定语从句堆叠** | "这是一个拥有着众多用户且在过去十年中不断创新的平台" | "这平台用户多，也一直在变。十年了。" |
| **抽象名词 + of + 抽象名词 直译** | "技术的演进" / "创新的浪潮" / "变革的力量" | "技术在变" / "很多人开始创新" / "一切都在变" |
| **"对……进行……" 万能句式** | "对问题进行深入分析" / "对数据进行清洗处理" | "把问题拆开看" / "把数据洗干净" |
| **"在……方面/层面/维度上" 滥用** | "在用户体验层面，我们做了优化" | "用户体验上，我们改了几处" |

#### 快速检测法

将一段中文**逐字译回英文**，如果得到的英文句子通顺自然，那这段话八成是英文思维。

```
❌ 中文原文: "这个概念可以被认为是对传统方法的重大变革"
→ 回译英文: "This concept can be considered a significant revolution to traditional methods"
→ 自然英文 ✅ → 中文 ❌（AI味浓）
→ 自然中文: "说白了，这和以前的做法不一样"
```

### 4.2 中文思维硬译英文 (Chinese Brain in English Body)

当中文用户要求英文输出时，AI 容易写出「语法正确但母语者永远不会这么写」的内容。

#### 检测特征

| 模式 | 示例 (❌ Chinglish) | ✅ Native English |
|---|---|---|
| **主语重复（中文习惯）** | "The system, it allows users to..." | "The system allows users to..." |
| **"There is/are" 开场过多** | 每段开头都用 "There are many reasons why..." | 用具体主语开场："Three factors drove this change." |
| **"We all know that" / "As we all know"** | AI 最爱的小演讲开场 | 直接陈述，不假设读者知道什么 |
| **"In daily life" / "In modern society"** | "在日常生活中" 的逐字翻译 | 直接描述场景，不加抽象前置 |
| **过度使用 "very" / "really" / "quite"** | "This is very important" / "a really good example" | 用更精确的词："critical"、"useful" 或减少修饰 |
| **"not only... but also" 泛滥** | 中文 "不仅……而且……" 的机械翻译 | 偶尔用；平常直接分两句说 |
| **"With the development of..."** | "随着……的发展" 的逐字翻译 — 英文中最臭名昭著的 AI 开场白 | 直接切入，不问来路 |
| **"plays an important role in"** | "扮演重要角色" 逐字翻 | 说具体做了什么，不说"角色" |

#### 快速检测法

问自己：**一个母语为英语的人在 Reddit / Twitter / Hacker News 上会这样发帖吗？**

```
❌ "With the development of AI technology, it plays an increasingly important role in our daily life."
→ Reddit 没人这么说话。
✅ "AI is everywhere now. My dad used it to write a birthday card last week."
```

### 4.3 双语混淆评分表 (Reader 评分用)

Reader 在评审混排/双语内容时，额外检查以下维度（每处违规 -3 分）：

| 检查项 | 扣分 |
|---|---|
| 英文思维写中文（被动语态/It is 结构直译/连接词首句） | -3/处 |
| 中文思维硬译英文（"With the development of"/"plays an important role"/"not only but also"） | -3/处 |
| 中英掺杂时风格割裂（中文部分口语化，英文部分突然学术腔） | -5/处 |
| 回译检测失败（回译后英文自然 = 中文大概率是 AI 味） | -5/处 |

---

## 快速自查清单

每次输出前快速扫描：

**词汇检查**
- [ ] 有无全局疲劳词（见上文第1节）？
- [ ] 有无模板专属疲劳词（见 template-library.md 对应模板的「AI 疲劳词表」小节）？
- [ ] 有无 "织就" / "谱写" / "扬帆起航" / "毋庸置疑"？
- [ ] 有无 "旨在" / "综上所述" / "在...的大背景下"？

**结构检查**
- [ ] 有无段落结尾强行升华？
- [ ] 有无 "不仅...更..." 等套话句式？
- [ ] 破折号是否超过 1 个/500 字？
- [ ] 段落长度是否有自然的参差感？

**内容检查**
- [ ] 每句话是否可被真实人类在聊天中说出来？
- [ ] 有无"端水大师"式的无立场陈述？
- [ ] 有无没有具体引用的"专家表示/研究表明"？

**🆕 双语检查 (v2.3)**
- [ ] 中文部分有无被动语态泛滥？（"可以被认为..."）
- [ ] 中文部分有无"It is + adj + that"直译？（"值得注意的是..."）
- [ ] 英文部分有无"With the development of..." 开场？
- [ ] 英文部分有无"not only... but also" 套话？
- [ ] 回译测试是否通过？（中文译回英文后是否自然？）

---

## 对比示例

### ❌ AI 味重（中文区）
> 在当今这个数字化快速发展的时代，人工智能技术无疑正在深刻地改变着我们的生活方式。它不仅为各行各业带来了前所未有的机遇，同时也引发了一系列深刻的思考。毋庸置疑，如何平衡技术创新与人文关怀，将成为未来科技发展的重要命题，只有时间能给出最终答案。

**问题清单**：
- "在当今这个数字化快速发展的时代" — 陈词滥调大背景
- "无疑"、"深刻"、"前所未有"、"深刻" — 空洞程度副词
- "不仅...同时也..." — 机械句式
- "毋庸置疑" — 中文高危词
- "如何平衡...成为...重要命题" — 端水大师
- "只有时间能给出最终答案" — 时间遁词
- "可以被认为" — 被动语态泛滥

### ✅ 人味版（中文）
> 去年我用 AI 写了第一篇公众号。朋友看完说："这是机器人写的吧？"
>
> 我问他怎么看出来的。
>
> 他说："因为你平时说话不这样。你说话会抖机灵，这篇没有。"
>
> 从那以后我开始琢磨一个问题：AI 到底是在帮我写，还是在替我写？

**为什么更好**：具体场景、对话感、段落长短不一、没有强行总结、最后一句留问号不回答。

### ❌ AI 味重（英文区 — Chinglish）
> With the rapid development of artificial intelligence technology, it has profoundly changed our daily lives. It is worth noting that AI plays an increasingly important role in various fields. Not only does it improve efficiency, but also it brings unprecedented opportunities. We all know that the future of AI is bright. However, we cannot ignore the challenges it poses.

**问题清单**：
- "With the rapid development of..." — 最著名的 AI 开场白
- "it has profoundly changed" — 空泛动词 + 乏味副词
- "It is worth noting that" — 英文高危词
- "plays an increasingly important role in" — 典型的逐字中译英
- "Not only... but also" — 机械句式
- "We all know that" — 假共识开场
- "unprecedented opportunities" — 英文常见过度修饰
- "However, we cannot ignore" — 端水大师英文版

### ✅ Native English
> I asked ChatGPT to write a blog post last month. Took three seconds.
>
> Took me two hours to rewrite it so it didn't sound like a robot.
>
> The weird part? The "robotic" version was grammatically flawless. The human version had sentence fragments. Started paragraphs with "And." Used the word "weird" four times.
>
> Maybe that's the difference. Humans are messy. AI is clean. Readers trust messy.

**为什么更好**：具体故事而非抽象陈述、短句碎句、有自嘲、用具体数字（three seconds / two hours）、没有人会读到一半觉得"这段是生成的"。
