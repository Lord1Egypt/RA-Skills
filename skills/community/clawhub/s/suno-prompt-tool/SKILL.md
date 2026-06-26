---
name: suno-prompt-tool
description: "Use when user wants to generate music with Suno AI, needs help writing Suno prompts, or asks about Suno music creation. (用于用户想要使用 Suno AI 生成音乐、需要帮助编写 Suno 提示词，或询问 Suno 音乐创作相关问题的场景。) 触发词：提示词，Suno提示词，suno提示词，SunoAI提示词，sunoai提示词，Suno提示词工具，suno提示词工具，提示词生成器，Suno提示词生成器，suno提示词生成器，音乐提示词，AI音乐提示词，ai音乐提示词，Prompt，prompt，Suno Prompt，suno prompt，Suno Prompts，suno prompts，Suno AI Prompt，suno ai prompt，Suno Prompt Tool，suno prompt tool，Prompt Generater，prompt generater，Suno Prompt Generater，suno prompt generater，Music Prompt，music prompt，AI Music Prompt，ai music prompt"
author: 猫头鹰AI音乐训练营（公众号：SunoAIStudio，微信号：SunoMusic）
website: https://skill.sunoai.wiki
version: 1.1.0
---

# Suno 提示词工具

帮助你生成高质量的 Suno AI 音乐提示词，创作专业级 AI 音乐。

## 什么是 Suno

Suno 是一款 AI 音乐生成工具，可以根据文本提示词生成完整的歌曲，包括：
- 人声演唱
- 乐器伴奏
- 歌词内容
- 多种音乐风格

## 提示词结构

Suno 提示词通常包含以下要素：

```
[风格/流派] + [情绪/氛围] + [乐器/配器] + [节奏/BPM] + [人声/演唱风格] + [场景/用途]
```

## 核心参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| **Style** | 音乐风格/流派 | Pop, Rock, Jazz, Classical, EDM, Hip-hop |
| **Mood** | 情绪氛围 | Happy, Sad, Energetic, Calm, Epic, Romantic |
| **Instrument** | 主要乐器 | Piano, Guitar, Strings, Synth, Drums |
| **Tempo** | 节奏快慢 | Slow, Mid-tempo, Fast, 120 BPM |
| **Vocal** | 人声类型 | Female vocal, Male vocal, Choir, Rap |
| **Theme** | 主题/场景 | Love song, Battle music, Lullaby, Workout |
| **Mastering** | 母带处理 | Professional, Radio-ready, Dynamic, Warm, Bright |
| **Era** | 时代感 | 80s, 90s, Modern, Retro, Vintage, Futuristic |

## 提示词模板

### 模板 1：简洁风格模式

```
[风格], [情绪], with [乐器], [节奏], [人声类型], for [场景]
```

**示例：**
- `Pop, upbeat, with synth and electronic drums, mid-tempo, female vocal, for workout`
- `Classical piano, emotional and romantic, slow tempo, instrumental, for wedding`

### 模板 2：详细描述模式

```
A [风格] song featuring [乐器]. The mood is [情绪] with [节奏描述]. [人声描述]. [额外细节].
```

**示例：**
- `A cinematic orchestral piece featuring strings and brass. The mood is epic and inspiring with a gradual build-up. No vocals. Perfect for movie trailers.`
- `A lo-fi hip-hop track featuring vinyl crackle and smooth piano. The mood is chill and relaxing with a slow groove. No vocals. Great for studying.`

### 模板 3：故事/场景模式

```
[场景描述]. [音乐风格] with [情绪], [乐器配置]. [人声/歌词主题].
```

**示例：**
- `Walking through a rainy city at night. Jazz with a melancholic mood, featuring saxophone and double bass. Soft male vocal singing about lost love.`
- `Sunrise over mountains. Ambient electronic with hopeful and peaceful vibes, featuring pads and gentle arpeggios. Ethereal female vocal humming.`

## 风格关键词速查

### 流派 (Genres)
| 中文 | 英文 |
|------|------|
| 流行 | Pop |
| 摇滚 | Rock |
| 爵士 | Jazz |
| 古典 | Classical |
| 电子 | Electronic / EDM |
| 嘻哈 | Hip-hop / Rap |
| 乡村 | Country |
| 民谣 | Folk |
| 蓝调 | Blues |
| 金属 | Metal |
| 放克 | Funk |
| 灵魂乐 | Soul |
| R&B | R&B |
| 拉丁 | Latin |
| 雷鬼 | Reggae |
| 世界音乐 | World Music |
| 电影配乐 | Cinematic / Film Score |
| 氛围音乐 | Ambient |
| 低保真 | Lo-fi |
| 赛博朋克 | Cyberpunk |

### 情绪 (Moods)
| 中文 | 英文 |
|------|------|
| 快乐 | Happy / Joyful |
| 悲伤 | Sad / Melancholic |
| 激励 | Inspiring / Motivational |
| 平静 | Calm / Peaceful |
| 史诗 | Epic / Grand |
| 浪漫 | Romantic |
| 神秘 | Mysterious |
| 紧张 | Tense / Suspenseful |
| 怀旧 | Nostalgic |
| 愤怒 | Angry / Aggressive |
| 梦幻 | Dreamy / Ethereal |
| 黑暗 | Dark |
| 明亮 | Bright / Uplifting |
| 复古 | Retro / Vintage |
| 未来感 | Futuristic |

### 乐器 (Instruments)
| 中文 | 英文 |
|------|------|
| 钢琴 | Piano |
| 吉他 | Guitar (Acoustic/Electric) |
| 小提琴 | Violin |
| 大提琴 | Cello |
| 弦乐组 | Strings |
| 萨克斯 | Saxophone |
| 小号 | Trumpet |
| 长笛 | Flute |
| 鼓 | Drums |
| 贝斯 | Bass |
| 合成器 | Synth / Synthesizer |
| 电子鼓 | Electronic drums |
| 管弦乐 | Orchestra |
| 合唱团 | Choir |
| 竖琴 | Harp |
| 古筝 | Guzheng |
| 二胡 | Erhu |
| 琵琶 | Pipa |

### 人声类型 (Vocals)
| 中文 | 英文 |
|------|------|
| 女声 | Female vocal |
| 男声 | Male vocal |
| 童声 | Children vocal |
| 合唱 | Choir |
| 说唱 | Rap / Hip-hop vocal |
| 哼唱 | Humming |
| 无歌声 | Instrumental |
| 低吟 | Whisper |
| 高音 | High-pitched vocal |
| 沙哑 | Raspy vocal |

### 母带处理 (Mastering)
| 中文 | 英文 |
|------|------|
| 专业级 | Professional |
| 电台级 | Radio-ready |
| 商业级 | Commercial quality |
| 动态 | Dynamic |
| 压缩 | Compressed |
| 响亮 | Loud |
| 平衡 | Balanced |
| 温暖 | Warm |
| 明亮 | Bright |
| 清晰 | Clean |
| 有力 | Punchy |
| 饱满 | Full |
| 流媒体优化 | Streaming optimized |
| CD音质 | CD quality |
| 黑胶准备 | Vinyl ready |

### 时代感 (Era)
| 中文 | 英文 |
|------|------|
| 50年代 | 1950s |
| 60年代 | 1960s |
| 70年代 | 1970s |
| 80年代 | 1980s |
| 90年代 | 1990s |
| 2000年代 | 2000s |
| 2010年代 | 2010s |
| 2020年代 | 2020s |
| 现代 | Modern |
| 复古 | Retro |
| 怀旧 | Vintage |
| 经典 | Classic |
| 未来感 | Futuristic |
| 蒸汽波 | Synthwave |
| 迪斯科 | Disco era |
| 摇滚黄金时代 | Golden age of rock |
| 嘻哈黄金时代 | Golden age of hip-hop |

## 进阶技巧

### 1. 组合多种风格
```
A fusion of jazz and hip-hop, featuring saxophone and boom-bap drums
```

### 2. 指定时代感
```
80s synthwave, retro electronic with analog synths
```

### 3. 参考具体艺术家风格
```
In the style of Hans Zimmer, epic cinematic orchestral
```

### 4. 指定结构变化
```
Starts slow and acoustic, builds up to an energetic electronic drop
```

### 5. 添加制作细节
```
With reverb-heavy production, analog warmth, vinyl crackle
```

### 6. 母带处理 (Mastering)
```
Professional mastering, radio-ready quality, dynamic range optimized
```

**Mastering 关键词：**
- **音质**：Professional, Radio-ready, Commercial quality
- **动态**：Dynamic, Compressed, Loud, Balanced
- **音色**：Warm, Bright, Clean, Punchy, Full
- **用途**：Streaming optimized, CD quality, Vinyl ready

### 7. 指定时代感 (Era)
```
80s synthwave style, retro analog synths with modern production
```

**Era 关键词：**
- **年代**：1980s, 1990s, 2000s, Modern
- **风格**：Retro, Vintage, Classic, Futuristic
- **流派时代**：Disco era, Golden age of rock, Golden age of hip-hop
- **制作风格**：Analog warmth, Digital clarity, Vintage tube sound

## 常见场景示例

### 🎵 背景音乐
```
Corporate background music, uplifting and professional, light electronic with piano, mid-tempo, instrumental, professionally mastered for clear presentation audio
```

### 🎮 游戏音乐
```
8-bit chiptune, energetic and playful, retro game music style, fast tempo, instrumental, for arcade game
```

### 🎬 电影配乐
```
Cinematic trailer music, epic and dramatic, full orchestra with heavy percussion, building intensity, choir, for action movie
```

### ☕ 咖啡/学习音乐
```
Lo-fi chill hop, relaxing and cozy, with soft piano and vinyl crackle, slow groove, no vocals, for studying
```

### 💪 运动音乐
```
High-energy EDM, motivational and intense, with heavy bass and electronic drums, fast tempo 140 BPM, female vocal, radio-ready mastering for maximum impact
```

### 🌙 睡眠音乐
```
Ambient sleep music, peaceful and calming, with soft pads and nature sounds, very slow, no percussion, instrumental, for relaxation
```

## 歌词内容提示

如果需要在提示词中指定歌词内容，可以描述：

```
歌词关于 [主题], [语言], [风格描述]
```

**示例：**
- `Lyrics about summer love, English, poetic and romantic`
- `Lyrics about chasing dreams, Chinese, motivational and uplifting`
- `Lyrics about nature and peace, English, folk style storytelling`

## 母带处理示例

### 🎚️ Mastering 应用场景

**商业发行版本：**
```
Pop love ballad, romantic and emotional, with piano and soft strings, professionally mastered for commercial release with balanced dynamics and radio-ready loudness
```

**流媒体优化版本：**
```
Electronic dance track, energetic and euphoric, with synth leads and heavy bass, streaming-optimized mastering for platforms like Spotify and Apple Music
```

**温暖模拟风格：**
```
Acoustic folk song, warm and intimate, with vintage production, analog-style mastering with warm saturation and gentle compression
```

## 时代感示例

### 🕰️ Era 应用场景

**80年代复古风格：**
```
80s synthwave pop, nostalgic and dreamy, with analog synthesizers and gated reverb drums, retro production with modern clarity, for nostalgic electronic music
```

**90年代嘻哈风格：**
```
90s golden age hip-hop, raw and authentic, with sampled jazz loops and boom-bap drums, vintage vinyl crackle and warm analog mastering, for classic hip-hop vibe
```

**现代未来感：**
```
Futuristic electronic, cutting-edge and innovative, with AI-generated textures and spatial audio, modern digital production with crystal clear mastering, for next-gen music experience
```

**经典摇滚时代：**
```
Classic rock revival, powerful and timeless, with tube amplifiers and analog tape saturation, vintage 70s rock production with warm tube mastering, for authentic rock experience
```

## 输出格式要求

**重要规则：** 每个生成的英文提示词下方，必须提供中文翻译对照，格式如下：

```
英文提示词
---
中文翻译
```

**示例：**

```
UK drill, gritty and energetic, with heavy 808 bass and rapid hi-hats, fast tempo 140 BPM, male rap vocal, for street vibe
---
中文翻译：英国Drill说唱，粗犷且充满能量，配合重低音808和快速踩镲，快节奏140 BPM，男声说唱，适合街头氛围
```

```
A cinematic orchestral piece featuring strings and brass. The mood is epic and inspiring with a gradual build-up. No vocals. Perfect for movie trailers.
---
中文翻译：一首电影感管弦乐作品，以弦乐和铜管为主。氛围史诗且振奋，逐渐推进。无人声。适合电影预告片。
```

```
Walking through a rainy city at night. Jazz with a melancholic mood, featuring saxophone and double bass. Soft male vocal singing about lost love.
---
中文翻译：深夜走在雨中的城市。爵士乐配忧郁氛围，以萨克斯和低音提琴为主。柔和男声演唱关于失去的爱。
```

## 使用流程

```
用户描述需求
    ↓
分析关键要素（风格、情绪、场景）
    ↓
选择合适模板
    ↓
生成专业提示词
    ↓
提供优化建议
```

## 对话示例

**用户：** 我想做一首适合跑步时听的中文歌

**助手分析：**
- 场景：跑步/运动
- 风格：高能量
- 语言：中文

**生成提示词：**
```
High-energy Chinese pop, motivational and upbeat, with electronic beats and synth, fast tempo 130 BPM, energetic female vocal singing in Chinese, for running and workout
```

---

**用户：** 帮我写个悲伤的钢琴曲，适合分手场景

**助手分析：**
- 情绪：悲伤
- 乐器：钢琴
- 场景：失恋/分手

**生成提示词：**
```
Sad piano ballad, melancholic and emotional, solo piano with minimal accompaniment, slow tempo, soft male vocal singing about heartbreak, for emotional scene
```
