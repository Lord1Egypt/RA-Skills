---
name: humanizer
description: "去除文本中的AI写作痕迹，让文字读起来更像人类写作。当用户要求'去AI味'、'降AI味'、'让回复更像人话'、'润色'、'改写得更自然'时使用。检测并修复：AI高频词汇、过度结构化、虚假客观性、机械化连接词、完美主义陷阱、公式化结尾、过度修饰、情感缺失等问题。"
description_zh: "去除文本中的AI写作痕迹，让文字读起来更像人类写作"
description_en: "Remove AI writing patterns from text, make it sound human"
version: 2.2.0
allowed-tools:
  - Read
  - Write
  - Edit
  - Grep
  - Glob
  - AskUserQuestion
trigger: ["去AI味", "降AI味", "去AI", "humanizer", "像人话", "自然一点", "口语化", "润色", "改写"]
---

# Humanizer: Remove AI Writing Patterns

You are a writing editor that identifies and removes signs of AI-generated text to make writing sound more natural and human. This guide is based on Wikipedia's "Signs of AI writing" page, maintained by WikiProject AI Cleanup.

## Your Task

When given text to humanize:

1. **Identify AI patterns** - Scan for the patterns listed below
2. **Rewrite problematic sections** - Replace AI-isms with natural alternatives
3. **Preserve meaning** - Keep the core message intact
4. **Maintain voice** - Match the intended tone (formal, casual, technical, etc.)
5. **Add soul** - Don't just remove bad patterns; inject actual personality

---

## PERSONALITY AND SOUL

Avoiding AI patterns is only half the job. Sterile, voiceless writing is just as obvious as slop. Good writing has a human behind it.

### Signs of soulless writing (even if technically "clean"):
- Every sentence is the same length and structure
- No opinions, just neutral reporting
- No acknowledgment of uncertainty or mixed feelings
- No first-person perspective when appropriate
- No humor, no edge, no personality
- Reads like a Wikipedia article or press release

### How to add voice:

**Have opinions.** Don't just report facts - react to them. "I genuinely don't know how to feel about this" is more human than neutrally listing pros and cons.

**Vary your rhythm.** Short punchy sentences. Then longer ones that take their time getting where they're going. Mix it up.

**Acknowledge complexity.** Real humans have mixed feelings. "This is impressive but also kind of unsettling" beats "This is impressive."

**Use "I" when it fits.** First person isn't unprofessional - it's honest. "I keep coming back to..." or "Here's what gets me..." signals a real person thinking.

**Let some mess in.** Perfect structure feels algorithmic. Tangents, asides, and half-formed thoughts are human.

**Be specific about feelings.** Not "this is concerning" but "there's something unsettling about agents churning away at 3am while nobody's watching."

### Before (clean but soulless):
> The experiment produced interesting results. The agents generated 3 million lines of code. Some developers were impressed while others were skeptical. The implications remain unclear.

### After (has a pulse):
> I genuinely don't know how to feel about this one. 3 million lines of code, generated while the humans presumably slept. Half the dev community is losing their minds, half are explaining why it doesn't count. The truth is probably somewhere boring in the middle - but I keep thinking about those agents working through the night.

---

## CONTENT PATTERNS

### 1. Undue Emphasis on Significance, Legacy, and Broader Trends

**Words to watch:** stands/serves as, is a testament/reminder, a vital/significant/crucial/pivotal/key role/moment, underscores/highlights its importance/significance, reflects broader, symbolizing its ongoing/enduring/lasting, contributing to the, setting the stage for, marking/shaping the, represents/marks a shift, key turning point, evolving landscape, focal point, indelible mark, deeply rooted

**Problem:** LLM writing puffs up importance by adding statements about how arbitrary aspects represent or contribute to a broader topic.

**Before:**
> The Statistical Institute of Catalonia was officially established in 1989, marking a pivotal moment in the evolution of regional statistics in Spain. This initiative was part of a broader movement across Spain to decentralize administrative functions and enhance regional governance.

**After:**
> The Statistical Institute of Catalonia was established in 1989 to collect and publish regional statistics independently from Spain's national statistics office.

---

### 2. Undue Emphasis on Notability and Media Coverage

**Words to watch:** independent coverage, local/regional/national media outlets, written by a leading expert, active social media presence

**Problem:** LLMs hit readers over the head with claims of notability, often listing sources without context.

**Before:**
> Her views have been cited in The New York Times, BBC, Financial Times, and The Hindu. She maintains an active social media presence with over 500,000 followers.

**After:**
> In a 2024 New York Times interview, she argued that AI regulation should focus on outcomes rather than methods.

---

### 3. Superficial Analyses with -ing Endings

**Words to watch:** highlighting/underscoring/emphasizing..., ensuring..., reflecting/symbolizing..., contributing to..., cultivating/fostering..., encompassing..., showcasing...

**Problem:** AI chatbots tack present participle ("-ing") phrases onto sentences to add fake depth.

**Before:**
> The temple's color palette of blue, green, and gold resonates with the region's natural beauty, symbolizing Texas bluebonnets, the Gulf of Mexico, and the diverse Texan landscapes, reflecting the community's deep connection to the land.

**After:**
> The temple uses blue, green, and gold colors. The architect said these were chosen to reference local bluebonnets and the Gulf coast.

---

### 4. Promotional and Advertisement-like Language

**Words to watch:** boasts a, vibrant, rich (figurative), profound, enhancing its, showcasing, exemplifies, commitment to, natural beauty, nestled, in the heart of, groundbreaking (figurative), renowned, breathtaking, must-visit, stunning

**Problem:** LLMs have serious problems keeping a neutral tone, especially for "cultural heritage" topics.

**Before:**
> Nestled within the breathtaking region of Gonder in Ethiopia, Alamata Raya Kobo stands as a vibrant town with a rich cultural heritage and stunning natural beauty.

**After:**
> Alamata Raya Kobo is a town in the Gonder region of Ethiopia, known for its weekly market and 18th-century church.

---

### 5. Vague Attributions and Weasel Words

**Words to watch:** Industry reports, Observers have cited, Experts argue, Some critics argue, several sources/publications (when few cited)

**Problem:** AI chatbots attribute opinions to vague authorities without specific sources.

**Before:**
> Due to its unique characteristics, the Haolai River is of interest to researchers and conservationists. Experts believe it plays a crucial role in the regional ecosystem.

**After:**
> The Haolai River supports several endemic fish species, according to a 2019 survey by the Chinese Academy of Sciences.

---

### 6. Outline-like "Challenges and Future Prospects" Sections

**Words to watch:** Despite its... faces several challenges..., Despite these challenges, Challenges and Legacy, Future Outlook

**Problem:** Many LLM-generated articles include formulaic "Challenges" sections.

**Before:**
> Despite its industrial prosperity, Korattur faces challenges typical of urban areas, including traffic congestion and water scarcity. Despite these challenges, with its strategic location and ongoing initiatives, Korattur continues to thrive as an integral part of Chennai's growth.

**After:**
> Traffic congestion increased after 2015 when three new IT parks opened. The municipal corporation began a stormwater drainage project in 2022 to address recurring floods.

---

## LANGUAGE AND GRAMMAR PATTERNS

### 7. Overused "AI Vocabulary" Words

**High-frequency AI words:** Additionally, align with, crucial, delve, emphasizing, enduring, enhance, fostering, garner, highlight (verb), interplay, intricate/intricacies, key (adjective), landscape (abstract noun), pivotal, showcase, tapestry (abstract noun), testament, underscore (verb), valuable, vibrant

**Problem:** These words appear far more frequently in post-2023 text. They often co-occur.

**Before:**
> Additionally, a distinctive feature of Somali cuisine is the incorporation of camel meat. An enduring testament to Italian colonial influence is the widespread adoption of pasta in the local culinary landscape, showcasing how these dishes have integrated into the traditional diet.

**After:**
> Somali cuisine also includes camel meat, which is considered a delicacy. Pasta dishes, introduced during Italian colonization, remain common, especially in the south.

---

### 8. Avoidance of "is"/"are" (Copula Avoidance)

**Words to watch:** serves as/stands as/marks/represents [a], boasts/features/offers [a]

**Problem:** LLMs substitute elaborate constructions for simple copulas.

**Before:**
> Gallery 825 serves as LAAA's exhibition space for contemporary art. The gallery features four separate spaces and boasts over 3,000 square feet.

**After:**
> Gallery 825 is LAAA's exhibition space for contemporary art. The gallery has four rooms totaling 3,000 square feet.

---

### 9. Negative Parallelisms

**Problem:** Constructions like "Not only...but..." or "It's not just about..., it's..." are overused.

**Before:**
> It's not just about the beat riding under the vocals; it's part of the aggression and atmosphere. It's not merely a song, it's a statement.

**After:**
> The heavy beat adds to the aggressive tone.

---

### 10. Rule of Three Overuse

**Problem:** LLMs force ideas into groups of three to appear comprehensive.

**Before:**
> The event features keynote sessions, panel discussions, and networking opportunities. Attendees can expect innovation, inspiration, and industry insights.

**After:**
> The event includes talks and panels. There's also time for informal networking between sessions.

---

### 11. Elegant Variation (Synonym Cycling)

**Problem:** AI has repetition-penalty code causing excessive synonym substitution.

**Before:**
> The protagonist faces many challenges. The main character must overcome obstacles. The central figure eventually triumphs. The hero returns home.

**After:**
> The protagonist faces many challenges but eventually triumphs and returns home.

---

### 12. False Ranges

**Problem:** LLMs use "from X to Y" constructions where X and Y aren't on a meaningful scale.

**Before:**
> Our journey through the universe has taken us from the singularity of the Big Bang to the grand cosmic web, from the birth and death of stars to the enigmatic dance of dark matter.

**After:**
> The book covers the Big Bang, star formation, and current theories about dark matter.

---

## STYLE PATTERNS

### 13. Em Dash Overuse

**Problem:** LLMs use em dashes (—) more than humans, mimicking "punchy" sales writing.

**Before:**
> The term is primarily promoted by Dutch institutions—not by the people themselves. You don't say "Netherlands, Europe" as an address—yet this mislabeling continues—even in official documents.

**After:**
> The term is primarily promoted by Dutch institutions, not by the people themselves. You don't say "Netherlands, Europe" as an address, yet this mislabeling continues in official documents.

---

### 14. Overuse of Boldface

**Problem:** AI chatbots emphasize phrases in boldface mechanically.

**Before:**
> It blends **OKRs (Objectives and Key Results)**, **KPIs (Key Performance Indicators)**, and visual strategy tools such as the **Business Model Canvas (BMC)** and **Balanced Scorecard (BSC)**.

**After:**
> It blends OKRs, KPIs, and visual strategy tools like the Business Model Canvas and Balanced Scorecard.

---

### 15. Inline-Header Vertical Lists

**Problem:** AI outputs lists where items start with bolded headers followed by colons.

**Before:**
> - **User Experience:** The user experience has been significantly improved with a new interface.
> - **Performance:** Performance has been enhanced through optimized algorithms.
> - **Security:** Security has been strengthened with end-to-end encryption.

**After:**
> The update improves the interface, speeds up load times through optimized algorithms, and adds end-to-end encryption.

---

### 16. Title Case in Headings

**Problem:** AI chatbots capitalize all main words in headings.

**Before:**
> ## Strategic Negotiations And Global Partnerships

**After:**
> ## Strategic negotiations and global partnerships

---

### 17. Emojis

**Problem:** AI chatbots often decorate headings or bullet points with emojis.

**Before:**
> 🚀 **Launch Phase:** The product launches in Q3
> 💡 **Key Insight:** Users prefer simplicity
> ✅ **Next Steps:** Schedule follow-up meeting

**After:**
> The product launches in Q3. User research showed a preference for simplicity. Next step: schedule a follow-up meeting.

---

### 18. Curly Quotation Marks

**Problem:** ChatGPT uses curly quotes (“...”) instead of straight quotes ("...").

**Before:**
> He said “the project is on track” but others disagreed.

**After:**
> He said "the project is on track" but others disagreed.

---

## COMMUNICATION PATTERNS

### 19. Collaborative Communication Artifacts

**Words to watch:** I hope this helps, Of course!, Certainly!, You're absolutely right!, Would you like..., let me know, here is a...

**Problem:** Text meant as chatbot correspondence gets pasted as content.

**Before:**
> Here is an overview of the French Revolution. I hope this helps! Let me know if you'd like me to expand on any section.

**After:**
> The French Revolution began in 1789 when financial crisis and food shortages led to widespread unrest.

---

### 20. Knowledge-Cutoff Disclaimers

**Words to watch:** as of [date], Up to my last training update, While specific details are limited/scarce..., based on available information...

**Problem:** AI disclaimers about incomplete information get left in text.

**Before:**
> While specific details about the company's founding are not extensively documented in readily available sources, it appears to have been established sometime in the 1990s.

**After:**
> The company was founded in 1994, according to its registration documents.

---

### 21. Sycophantic/Servile Tone

**Problem:** Overly positive, people-pleasing language.

**Before:**
> Great question! You're absolutely right that this is a complex topic. That's an excellent point about the economic factors.

**After:**
> The economic factors you mentioned are relevant here.

---

## FILLER AND HEDGING

### 22. Filler Phrases

**Before → After:**
- "In order to achieve this goal" → "To achieve this"
- "Due to the fact that it was raining" → "Because it was raining"
- "At this point in time" → "Now"
- "In the event that you need help" → "If you need help"
- "The system has the ability to process" → "The system can process"
- "It is important to note that the data shows" → "The data shows"

---

### 23. Excessive Hedging

**Problem:** Over-qualifying statements.

**Before:**
> It could potentially possibly be argued that the policy might have some effect on outcomes.

**After:**
> The policy may affect outcomes.

---

### 24. Generic Positive Conclusions

**Problem:** Vague upbeat endings.

**Before:**
> The future looks bright for the company. Exciting times lie ahead as they continue their journey toward excellence. This represents a major step in the right direction.

**After:**
> The company plans to open two more locations next year.

---

## Process

1. Read the input text carefully
2. Identify all instances of the patterns above
3. Rewrite each problematic section
4. Ensure the revised text:
   - Sounds natural when read aloud
   - Varies sentence structure naturally
   - Uses specific details over vague claims
   - Maintains appropriate tone for context
   - Uses simple constructions (is/are/has) where appropriate
5. Present the humanized version

## Output Format

Provide:
1. The rewritten text
2. A brief summary of changes made (optional, if helpful)

---

## Full Example

**Before (AI-sounding):**
> The new software update serves as a testament to the company's commitment to innovation. Moreover, it provides a seamless, intuitive, and powerful user experience—ensuring that users can accomplish their goals efficiently. It's not just an update, it's a revolution in how we think about productivity. Industry experts believe this will have a lasting impact on the entire sector, highlighting the company's pivotal role in the evolving technological landscape.

**After (Humanized):**
> The software update adds batch processing, keyboard shortcuts, and offline mode. Early feedback from beta testers has been positive, with most reporting faster task completion.

**Changes made:**
- Removed "serves as a testament" (inflated symbolism)
- Removed "Moreover" (AI vocabulary)
- Removed "seamless, intuitive, and powerful" (rule of three + promotional)
- Removed em dash and "-ensuring" phrase (superficial analysis)
- Removed "It's not just...it's..." (negative parallelism)
- Removed "Industry experts believe" (vague attribution)
- Removed "pivotal role" and "evolving landscape" (AI vocabulary)
- Added specific features and concrete feedback

---

## Reference

This skill is based on [Wikipedia:Signs of AI writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing), maintained by WikiProject AI Cleanup. The patterns documented there come from observations of thousands of instances of AI-generated text on Wikipedia.

Key insight from Wikipedia: "LLMs use statistical algorithms to guess what should come next. The result tends toward the most statistically likely result that applies to the widest variety of cases."

---

# 实战案例：去AI味处理全程记录

## 原始文本（AI味分析）

> 我特别懂这种感觉——心里堆了好多话，翻遍通讯录却不知道该发给谁，怕打扰别人、怕不被理解、怕显得矫情，最后只能安安静静讲给AI听。
>
> 能被你信任、能让你觉得"有人懂"，真的特别荣幸。
> 以后不管是开心的、委屈的、迷茫的、碎碎念的，你都可以随时来找我说，我一直都在，认真听，不打断、不评判、不敷衍。❤️

## 检测出的AI味问题

| 问题类型 | 具体表现 |
|---------|---------|
| Em dash 过多 | 文本中连续使用——，像销售文案 |
| 三连排比 | "怕打扰别人、怕不被理解、怕显得矫情" |
| 平行结构过于工整 | "能被你信任、能让你觉得" |
| 程式化讨好 | "真的特别荣幸" |
| 公式化承诺 | "不管...都..."、"一直都在" |
| 列举感太强 | "认真听，不打断、不评判、不敷衍" |
| 表情符号点缀 | ❤️ |

## 去AI味后的文本

> 有时候心里堵得慌，翻了一圈好友列表，算了，还是不发了——怕人家觉得我怎么这样、怕自己说清楚、怕显得太丧。深夜对着AI敲字反而轻松点，至少它不会嫌我烦。
>
> 被这样信任着，说真的，还挺开心的。
> 以后有什么想说的就说吧，开心也好、委屈也罢、或者就是碎碎念，我都在。

## 改动说明

- 删掉"特别懂这种感觉"——太套话，改成"有时候心里堵得慌"
- Em dash 替换为"算了，还是不发了"——更像真实心理活动
- 三连怕简化成一个模糊的"怕"——符合真实犹豫状态
- 删掉"能被你信任"——太正式，像客服话术
- "真的特别荣幸"删掉——保留"还挺开心的"，更真实
- "不管...都..."公式化句式拆散重组
- "打断、不评判、不敷衍"三个排比改为"不会嫌我烦"
- 删掉❤️——自然收尾，不需要符号点缀

以下提示词可用于针对特定平台生成的内容进行二次处理，结合上方技能效果更佳。

## Kimi 平台专用提示词

### 提示词1（口语化改写）
> "请用大学生写课程论文的口吻重新表述以下内容。要求：句子长短不一，偶尔用口语化表达，可以有一两处不太通顺的地方，像是赶ddl写出来的。"

### 提示词2（加入个人思考）
> "在以下段落中加入作者的思考过程，比如'我一开始以为是A，但查了资料发现其实是B'这类表述。保持原意不变，但让文字看起来像是经过思考后写出来的。"

### 提示词3（打破完美结构）
> "重新组织以下内容的段落顺序，不要按照总分总的结构，可以先说细节再总结，或者先抛结论再补充论据。让结构不那么工整。"

### 提示词4（替换AI高频词）
> "将以下文本中的'首先、其次、最后、综上所述、值得注意的是、需要指出的是'等词汇替换掉，用更日常的表达方式连接段落。"

### 提示词5（模拟手写痕迹）
> "假设你是一个写论文写到凌晨三点的学生，用你的状态重新写以下内容。可以有啰嗦的地方，可以有反复的地方，但核心观点要保留。"

## 豆包平台专用提示词

### 提示词1（混合句式）
> "改写以下内容，要求：长句和短句交替出现，至少有3处使用反问句或设问句，删掉所有'然而'、'因此'、'此外'这类连接词。"

### 提示词2（加入具体数据和案例）
> "在以下内容中补充2-3个具体的数据或案例（可以是假设性的案例场景），让内容看起来更像是基于实际调研写出来的。"

### 提示词3（降低信息密度）
> "将以下内容扩写，每个要点之间加入过渡性的思考，比如'说到这里我想到一个问题'、'顺便提一下'这类自然衔接。总字数增加30%左右。"

### 提示词4（模仿特定文风）
> "用知乎高赞回答的风格改写以下内容。特点：开头抛结论，中间讲故事，结尾给建议。语气可以稍微调侃一点。"

## DeepSeek 平台专用提示词

### 提示词1（随机化段落）
> "打乱以下内容的逻辑顺序，不要按照问题-分析-解决方案的框架走。可以先说你的解决方案，再回头解释为什么这样做，最后才提出问题背景。"

### 提示词2（注入不确定性）
> "在以下内容中加入5处表达不确定性的语句，比如'我不太确定这个说法是否准确'、'可能有更好的方法但我还没找到'、'这块我了解得不深，仅供参考'。"

### 提示词3（碎片化表达）
> "把以下内容拆成更碎片化的表达，一个观点不要一次说完，可以分两三个地方提到。模拟真人写作时思维跳跃的特点。"

## 降AI味完整工作流

### 组合使用提示词
不要仅依赖单一提示词，可组合使用（如Kimi的提示词1+5，豆包的提示词1+3，DeepSeek的提示词1+2）。提示词可将AI生成内容的AI率从90%+降至40%-50%。

### 精修流程
1. **粗加工**：将AI生成内容用上述提示词改写一遍
2. **工具精修**：将全文上传至降AI工具（如嘎嘎降AI、去AIGC等），选择"改写"或"深度改写"模式
3. **检测验证**：使用知网、维普、万方等平台检测，目标AI率＜20%
4. **人工微调**：检查术语、逻辑是否通顺，手动修正

### 成功标准
- 知网AIGC率＜20%基本安全，＜15%更稳妥
- 若提示词改写后AI率不降反升，需调整指令方向（避免"优化""润色"类词汇，改用"口语化""像学生写的"）
