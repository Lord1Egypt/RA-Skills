# 特殊元素处理手册

本文档详细说明歌词翻译中遇到的特殊元素类型及其处理方式。

## 目录

1. [段落标记 Section Markers](#1-段落标记-section-markers)
2. [拟声词 Adlibs & Onomatopoeia](#2-拟声词-adlibs--onomatopoeia)
3. [罗马音/注音](#3-罗马音注音)
4. [歌手名/角色名](#4-歌手名角色名)
5. [地点/历史典故](#5-地点历史典故)
6. [俚语/黑话](#6-俚语黑话)
7. [跨语言嵌套](#7-跨语言嵌套)
8. [重复段/回声](#8-重复段回声)
9. [语气词/感叹词](#9-语气词感叹词)
10. [数字/符号/特殊排版](#10-数字符号特殊排版)

---

## 1. 段落标记 Section Markers

### 识别

方括号包裹的结构标记：`[Intro]`, `[Verse 1]`, `[Verse 2]`, `[Pre-Chorus]`, `[Chorus]`, `[Bridge]`, `[Outro]`, `[Hook]`, `[Refrain]`, `[Drop]`, `[Solo]`, `[Instrumental]`, `[Beat drop]`

带演唱者：`[Intro: Justin Bieber]`, `[Verse 1: Luis Fonsi & Daddy Yankee]`, `[Chorus: Adele]`

### 处理规则

- **原样保留不译**
- 行单独占一行
- 不影响行号对齐（标记行不计入歌词行号）

### 案例

原文：
```
[Intro: Justin Bieber]
Come and move that in my direction
So thankful for that, it's such a blessing
```

译文：
```
[Intro: Justin Bieber]
毫无畏惧地朝我奔来
被你视中 势必我此生有幸
```

### 边界

- 中文歌曲的"前奏/间奏/尾奏"等中文标记，可保留中文
- 部分网站会用「1番」「2番」「サビ」等日文标记，翻译时统一转为英文 [Verse 1] [Verse 2] [Chorus]

---

## 2. 拟声词 Adlibs & Onomatopoeia

### 识别

歌词中的无实义声音：`Na na na`, `La la la`, `Yeah yeah`, `Oh oh`, `Da da da`, `Hey hey`, `Ooh`, `Aah`, `Woo`

日语：`ねえねえ`, `ハイハイ`, `どんどん`, `ドキドキ`
韩语：`오빠`, `아이고`, `웃겨`
中文：`啦啦啦`, `嗯嗯嗯`, `哎呀`

### 处理规则（重要：保持一致！）

整首歌中**同类型**拟声词采用**统一**处理方式，不要混用。三种可选策略：

#### 策略 A：保留原文（推荐用于英文歌）

```
Na na na nananana, nananana, hey Jude
Na na na nananana, nananana, hey Jude
```
保留原文不译。理由：保留原曲节奏感，且 "Na na na" 无实义。

#### 策略 B：音译（推荐用于日韩歌）

```
Na na na nananana → 那那那那那那那那
```
理由：让中文读者也能跟唱。

#### 策略 C：删除（不推荐）

只在拟声词是纯装饰、不影响信息时使用。

### 各语言推荐策略

| 语言 | 推荐策略 | 理由 |
|------|---------|------|
| 英文 | 保留原文 | 中文读者习惯英文 adlib |
| 日文 | 意译或保留 | 日文拟态词多有意境 |
| 韩文 | 意译 | 韩文 adlib 多有实义 |
| 西语 | 保留 | 拉丁节奏感重要 |
| 法语 | 意译 | 法语拟声词文学性强 |

### 案例：Hey Jude 副歌

原文：
```
Na na na nananana, nananana, hey Jude
Na na na nananana, nananana, hey Jude
```

推荐处理（保留原文 + 中文括注首次）：
```
Na na na nananana, nananana, hey Jude (那那那那那那那那)
Na na na nananana, nananana, hey Jude
```

### 案例反例

错例：每行不同处理
```
Na na na → 那那那
Na na na → 啦啦啦
Na na na → 嗯嗯嗯
```
读者会困惑，必须保持一致。

---

## 3. 罗马音/注音

### 识别

日韩文歌词中常附带的发音辅助：
- 日文：`残酷な天使` (ざんこくなてんし) 或 `残酷な天使` (Zankoku na Tenshi)
- 韩文：`사랑해` (saranghae)
- 中文：`我爱你` (wǒ ài nǐ)

### 处理规则

**全部删除**。译文只需保留汉字/谚文/原文字母，不需要发音辅助。

### 案例

原文：
```
残酷な天使のように (ざんこくなてんしのように)
少年よ 神話になれ (しょうねんよ しんわになれ)
```

处理后：
```
残酷な天使のように
少年よ 神話になれ
```

### 边界

- 如果用户专门要求"带罗马音版本"，则保留
- 学习用途（如外语学习者）可保留罗马音作为辅助

---

## 4. 歌手名/角色名

### 识别

歌手名：`Queen`, `Adele`, `Ed Sheeran`, `初音ミク`, `BLACKPINK`, `BTS`
角色名：动漫角色名如 `エヴァ` (EVA), `鬼滅` (鬼灭), `ナルト` (鸣人)

### 处理规则

按"首次出现 + 后续简化"原则：

1. **首次出现**：保留原文 + 中文括注
2. **后续出现**：仅用中文（或仅用原文，看哪个更自然）

### 案例

首次：
> 初音ミク（初音未来）演唱的《千本桜》...

后续：
> 初音未来在副歌部分...

### 各语言惯例

| 语言 | 处理 |
|------|------|
| 英文歌手名 | 保留英文（如 Adele, Ed Sheeran） |
| 日文歌手名 | 中文译名更常用（初音未来、米津玄师） |
| 韩文歌手名 | 中文译名常用（防弹少年团、粉墨） |
| 团体名 | 保留英文缩写（BTS, BLACKPINK） |

### 角色名特殊处理

动漫角色名根据中文社区惯例：

- 知名角色用中文译名：鸣人、路飞、悟空
- 不知名角色保留原文 + 译注
- 角色歌中演唱者人设需在元信息说明

---

## 5. 地点/历史典故

### 识别

地点：`New York`, `東京`, `Paris`, `Bollywood`, `Hollywood`, `Panamera` (车款)
历史：`ICBM`, `World War II`, ` Vietnam`, `Cold War`
神话：`黄泉`, `Valhalla`, `Mt. Olympus`, `Samsara`

### 处理规则

按典故"知名度 + 文化特异性"分级：

| 知名度 | 处理 |
|--------|------|
| 国际通用（New York, Paris） | 直译（纽约、巴黎） |
| 文化特异但知名（黄泉、武士道） | 直译 + 首次脚注 |
| 文化特异且冷门（神道教某概念） | 意译 + 详细脚注 |
| 现代俚语/缩写（ICBM） | 保留 + 脚注 |

### 案例：千本桜中的"ICBM"

```
悪霊退散 ICBM
環状線を走り抜けて
```

译文：
```
恶灵退散 ICBM
奔驰穿过环状线
```

脚注：ICBM = Intercontinental Ballistic Missile（洲际弹道导弹）。歌曲发表于 2011 年，借冷战意象表达对核威胁的反思。

### 案例：99 Luftballons 中"Luftballons"

德语"Luftballons" = "air balloons"，但中文译为"红色气球"（而非"空气球"），因为：

- 直译"空气球"无意义
- "红色气球"在中文语境中能引发对战争+童真的对比联想（与歌曲反战主题契合）
- 歌曲中后续提到"被误认为 UFO"、"将军派遣战机"，红色气球在天空中的视觉意象更强

### 案例：Con Altura 中"Panamera"

```
Pongo rosas sobre el Panamera
```

译文：
```
我摆了玫瑰在帕纳美拉上
```

脚注：Panamera = 保时捷帕纳美拉车型，是 Rosalía 在 MV 中驾驶的车款，象征奢华。

---

## 6. 俚语/黑话

### 识别

英文：`drop bombs`, `chokin'`, `snap back`, `OG`, `flex`, `low key`
日文：`うっせぇわ` (吵死了), `やばい` (糟了/超棒), `エモい` (emo)
韩文：`대박` (大发), `헐` (晕)
中文：`炸街`, `牛批`, `卧槽`

### 处理规则

- **意译为主**：用中文等效俚语传达情绪
- **必要时脚注**：解释文化背景
- **保留节奏感**：俚语多为短促词，译文也要短促

### 案例：Eminem "Lose Yourself"

```
His palms are sweaty, knees weak, arms are heavy
There's vomit on his sweater already, mom's spaghetti
He's nervous, but on the surface he looks calm and ready to
but he keeps on forgettin' what he wrote down
the whole crowd goes so loud
He opens his mouth, but the words won't come out
He's chokin', how, everybody's jokin' now
Snap back to reality, oh there goes gravity
```

译文（保留节奏感）：
```
他手心冒汗、腿软、手臂沉重
把妈妈煮的义大利面呕吐在毛衣上
他很紧张，但看起来冷静而就绪，要开始用歌词轰炸
但他却一直忘记他原本写的词
人群开始骚动
他张口却吐不出半个字
像窒息一般，怎么会这样，大家都在嘲笑他
跌落回现实，重力压着他
```

### 案例：Ado "うっせぇわ"

```
うっせぇわ うっせぇわ うっせぇわ
```

译文：
```
吵死了 吵死了 吵死了
```

或更口语：
```
烦死了 烦死了 烦死了
```

理由：用中文等效口语传达原词的烦躁感。

---

## 7. 跨语言嵌套

### 识别

一首歌中混合多种语言：
- Despacito Remix：西语 + 英语
- Waka Waka：西语 + 英语 + 斯瓦希里语
- Dynamite (BTS)：全英文 K-Pop
- 千本桜：日文 + "ICBM" 英文缩写
- DDU-DU DDU-DU：韩文 + 英文短句

### 处理规则

按"主语言 + 嵌入语言"区分：

| 嵌入类型 | 处理 |
|---------|------|
| 主语言 | 翻译为中文 |
| 嵌入英文短句（< 1 行） | 保留原文 + 中文括注 |
| 嵌入整段英文 | 翻译为中文（但标注"原文为英文段"） |
| 文化符号词（oppa, senpai） | 保留原文不译 |
| 国际通用缩写（ICBM, UFO） | 保留不译 |

### 案例：DDU-DU DDU-DU

原文：
```
BLACKPINK
Ah yeah, ah yeah
BLACKPINK
Ah yeah, ah yeah
착한 얼굴에 그렇지 못한 태도
가녀린 몸매 속 가려진 Volume은 두 배로
거침없이 직진 굳이 보진 않지 눈치
Black 하면 Pink 우린 예쁘장한 Savage
원할 땐 대놓고 뺏지
넌 뭘 해도 칼로 물 베기
두 손엔 가득한 Fat check
궁금하면 해봐 Fact check
```

译文：
```
BLACKPINK
啊 耶，啊 耶
BLACKPINK
啊 耶，啊 耶
善良的脸庞 却带着叛逆的态度
纤细身躯下 隐藏着翻倍的气场
毫无顾忌地直行 从不在意他人眼光
Black 配上 Pink 我们是甜美的 Savage
想要的时候就大方夺取
无论你做什么都只是徒劳无功
双手握满了厚实的 Fat check
好奇的话就尽管去 Fact check
```

注："Volume"、"Savage"、"Fat check"、"Fact check" 等英文词保留，因为这是 K-Pop 的标志性风格。

---

## 8. 重复段/回声

### 识别

歌词中常见的重复：
- 副歌重复 2-3 次
- 回声（括号内）：`(yeah)`, `(oh)`, `(uh)`
- 卡农式对位

### 处理规则

- **完整重复**：每次都重复译文（不要"同上"）
- **回声保留**：括号内的回声保留原文或音译
- **对位**：保持原文字位

### 案例：Hey Jude 副歌

原文：
```
Na na na nananana, nananana, hey Jude (repeat x4)
```

译文（每次都重复）：
```
Na na na nananana, nananana, hey Jude
Na na na nananana, nananana, hey Jude
Na na na nananana, nananana, hey Jude
Na na na nananana, nananana, hey Jude
```

不要简化为"（重复 4 次）"。

---

## 9. 语气词/感叹词

### 识别

英文：`oh`, `yeah`, `hey`, `ah`, `ooh`, `wow`
日文：`ね`, `よ`, `さ`, `わ`, `かしら`, `ぜ`, `ぞ`
韩文：`요`, `다`, `까`, `네`
中文：`啊`, `哦`, `哎`, `嘿`, `噢`

### 处理规则

- **保留语气**：原文有语气词，译文也要有对应
- **匹配人设**：女性语 vs 男性语 vs 中性
- **不滥用**：不要每行都加"啊"，会显得腻

### 日语语气词映射表

| 日文 | 中文对应 | 适用语境 |
|------|---------|---------|
| ね (ne) | 啊/哦/呢 | 寻求认同 |
| よ (yo) | 啊/哦 | 强调告知 |
| さ (sa) | 嘛 | 随意陈述 |
| わ (wa) | 呀/哦 | 女性语 |
| かしら (kashira) | 吧/呢 | 女性疑问 |
| ぜ (ze) | 嘛/啊 | 男性随意 |
| ぞ (zo) | 啊/哦 | 男性强调 |
| な (na) | 啊 | 感叹 |

### 案例：アイドル 中的人设

原文（甜腻偶像人设）：
> どうして？ どうして？ どうしてよ

译文（保留甜腻感）：
> 为什么？ 为什么？ 为什么呀

加"呀"字传达女性偶像的娇嗔感。

---

## 10. 数字/符号/特殊排版

### 数字处理

- **数字本身**：保留数字（如 "99 Luftballons" → "99 只红色气球"）
- **数字读法**：如果需要可读性，转为汉字（99 → 九十九）

### 符号处理

- **问号、感叹号**：保留
- **省略号**：保留
- **波浪号**：保留（如 "Yeah~" → "Yeah～"）
- **破折号**：保留
- **斜体/加粗**：HTML 输出时保留 `<em>` `<strong>` 标签

### 排版处理

- **段落分隔**：空行保留
- **缩进**：删除（歌词不需要缩进）
- **段内换行**：保留（用 `<br>` 或换行符）
- **特殊字符**：如 `♥` `★` 等装饰符号，保留

### 案例：Bohemian Rhapsody 多段落排版

原文：
```
Is this the real life?
Is this just fantasy?
Caught in a landslide
No escape from reality
Open your eyes
Look up to the skies and see
```

译文（保持原排版）：
```
这是现实世界吗?
还是只是我的幻想?
困在土石流中
无法摆脱现实
张开你的双眼
仰望天空，看看
```

不要重新排版或合并行。

---

## 总结

特殊元素处理的核心原则：

1. **一致性**：同类型元素整首歌统一处理
2. **保留原味**：能保留原文的尽量保留（特别是文化符号）
3. **可读性**：不能让译文变得难读
4. **目标读者**：考虑这首歌的目标读者（K-Pop 粉丝 vs 普通听众）会期望什么样的处理

遇到本手册未覆盖的特殊元素，参考已有案例类推，或咨询用户偏好。
