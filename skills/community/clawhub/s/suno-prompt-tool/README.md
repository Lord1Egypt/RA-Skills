# Suno Prompt Tool 使用说明书

## 🎯 什么是Suno Prompt Tool（Suno提示词工具）？

**Suno Prompt Tool** 是一个「猫头鹰AI音乐训练营」专门为AI音乐创作者、音乐人设计的Suno AI提示词生成工具（OpenClaw Skill）。无论您是专业的音乐制作人、AI音乐爱好者还是内容创作者，这个工具都能帮助您快速生成高质量的Suno AI音乐创作提示词。

### ✨ 工具特色

- **🎵 专业级模板**：提供标准化、可复用的提示词模板
- **🌍 中英文翻译**：中英文提示词输出，更容易理解
- **🎨 丰富参数**：20+音乐风格、情绪氛围、乐器配置等
- **⚡ 高效实用**：高效沟通，一键生成，立即使用
- **📚 详细文档**：完整的教程和使用说明书

## 🚀 快速开始

### 第一步：了解基本功能

**支持的参数类型：**
- **音乐风格**：Pop, Rock, Jazz, Classical, Electronic, Hip-hop等
- **情绪氛围**：Happy, Sad, Energetic, Calm, Epic, Romantic等
- **乐器配置**：Piano, Guitar, Strings, Synth, Drums等
- **节奏快慢**：Slow, Mid-tempo, Fast, 120 BPM
- **人声类型**：Female vocal, Male vocal, Choir, Rap
- **主题场景**：Love song, Battle music, Lullaby, Workout
- **母带处理**：Professional, Radio-ready, Dynamic, Warm, Bright
- **时代感**：80s, 90s, Modern, Retro, Vintage, Futuristic等

### 第二步：选择适合的场景

根据您的使用场景，选择合适的提示词模板：

| 场景 | 推荐模板 | 适用音乐类型 |
|------|----------|-------------|
| 运动健身 | Template 1 | 电子舞曲、摇滚 |
| 背景音乐 | Template 2 | 爵士、古典 |
| 故事叙述 | Template 3 | 氛围音乐、叙事性音乐 |
| 游戏配乐 | 自定义组合 | 8-bit、电影配乐 |

### 第三步：查看示例

**运动健身音乐：**
```
High-energy EDM, motivational and intense, with heavy bass and electronic drums, fast tempo 140 BPM, female vocal, radio-ready mastering for maximum impact
```

**中文翻译：** 高能量电子舞曲，激励人心且充满力量，配合重低音和电鼓，快节奏140 BPM，女声演唱，电台级制作以达到最大冲击力

## 🛠️ 详细功能介绍

### 🎵 音乐风格库（20+种）

**主流风格：**
- Pop (流行)
- Rock (摇滚)
- Jazz (爵士)
- Classical (古典)
- Electronic / EDM (电子)
- Hip-hop / Rap (嘻哈)

**特色风格：**
- Metal (金属)
- Country (乡村)
- Blues (蓝调)
- Reggae (雷鬼)
- Folk (民谣)
- Ambient (氛围)

### 🎭 情绪氛围设置

**积极情绪：** Happy, Joyful, Energetic, Inspiring, Uplifting, Motivational  
**消极情绪：** Sad, Melancholic, Calm, Peaceful, Romantic, Mysterious  
**特殊情绪：** Epic, Tense, Nostalgic, Aggressive, Dreamy, Bright

### 🎸 乐器配置详解

**键盘类：** Piano, Keyboard, Synth, Harpsichord  
**弦乐类：** Guitar (Acoustic/Electric), Violin, Cello, Strings  
**管乐类：** Saxophone, Trumpet, Flute, Woodwind  
**打击乐：** Drums, Percussion, Electronic drums  
**特色乐器：** Orchestra, Choir, Guzheng, Erhu, Pipa

### 🎚️ 专业制作参数

**音质等级：** Professional, Radio-ready, Commercial quality, Streaming optimized  
**动态处理：** Dynamic, Compressed, Balanced, Loud  
**音色调整：** Warm, Bright, Clean, Punchy, Full  
**时代感：** 80s, 90s, Modern, Retro, Vintage, Futuristic

## 📖 使用方法详解

### 安装方法

**Dashboard 安装（新手推荐）**

1. 打开 OpenClaw Dashboard

2. 点击左边导航栏「技能」进入

3. 搜索技能「suno-prompt-tool」 → 点按钮「安装」一键安装

**手动复制粘贴文件夹**

1. 找到 OpenClaw 技能目录：

Windows: C:\Users\你的用户名\.openclaw\skills
Mac/Linux: ~/.openclaw/skills

2. 把技能「suno-prompt-tool」文件夹整个复制粘贴进去

3. 重载生效：

```
openclaw skill reload
```

**CLI安装**

1. 最新版本（推荐）

```
openclaw skill install suno-prompt-tool
```

2. 指定版本（1.1.0为版本号）

```
openclaw skill install suno-prompt-tool@1.1.0
```

**Github仓库安装**

```
openclaw skill install --github https://github.com/AIMusicAlliance/suno-prompt-tool
```

### 使用方法

在 OpenClaw 聊天对话框，输入以下任意一个触发词，即可触发 suno-prompt-tool Skill，然后按提示聊天即可：

**中文触发词：**

```
提示词，Suno提示词，SunoAI提示词，Suno提示词工具，提示词生成器，Suno提示词生成器，音乐提示词，AI音乐提示词
```

**英文触发词：**

```
Prompt，Suno Prompt，Suno Prompts，Suno AI Prompt，Suno Prompt Tool，Prompt Generater，Suno Prompt Generater，Music Prompt，AI Music Pronpt
```

## 提示词模板格式

suno-prompt-tool的输出结果目前提供以下三种提示词模板：

### Template 1：简洁风格
**格式：**
```
[风格], [情绪], with [乐器], [节奏], [人声类型], for [场景]
```

**示例：**
```
Pop, upbeat, with synth and electronic drums, mid-tempo, female vocal, for workout
```

**中文翻译：** 流行，轻快，配合合成器和电子鼓，中速节奏，女声演唱，适用于运动场景

### Template 2：详细描述
**格式：**
```
A [风格] song featuring [乐器]. The mood is [情绪] with [节奏描述]. [人声描述]. [额外细节].
```

**示例：**
```
A cinematic orchestral piece featuring strings and brass. The mood is epic and inspiring with a gradual build-up. No vocals. Perfect for movie trailers.
```

**中文翻译：** 一部电影配乐风格的管弦乐作品，以弦乐和铜管乐器为特色。情绪宏大而鼓舞人心，具有渐进式的构建过程。无声乐部分。非常适合电影预告片。

### Template 3：故事场景
**格式：**
```
[场景描述]. [音乐风格] with [情绪], [乐器配置]. [人声/歌词主题].
```

**示例：**
```
Walking through a rainy city at night. Jazz with a melancholic mood, featuring saxophone and double bass. Soft male vocal singing about lost love.
```

**中文翻译：** 在雨夜漫步城市。爵士乐带有忧郁情绪，以萨克斯风和低音提琴为特色。轻柔的男声演唱关于失去的爱情

## 🎯 实际应用场景

### 💪 运动健身场景

**高强度训练：**
```
High-energy EDM, motivational and intense, with heavy bass and electronic drums, fast tempo 140 BPM, female vocal, radio-ready mastering for maximum impact
```

**中文翻译：** 高能量电子舞曲，激励人心且充满力量，配合重低音和电鼓，快节奏140 BPM，女声演唱，电台级制作以达到最大冲击力

**有氧运动：**
```
High-energy Chinese pop, motivational and upbeat, with electronic beats and synth, fast tempo 130 BPM, energetic female vocal singing in Chinese, for running and workout
```

**中文翻译：** 高能量中文流行歌曲，激励人心且充满活力，配合电子节拍和合成器音效，快节奏130 BPM，充满活力的女声演唱中文歌词，适用于跑步和有氧运动

### ☕ 学习工作场景

**背景音乐：**
```
Corporate background music, uplifting and professional, light electronic with piano, mid-tempo, instrumental, professionally mastered for clear presentation audio
```

**中文翻译：** 企业背景音乐，鼓舞人心且专业，轻电子风格配钢琴，中速节奏，纯音乐，专业母带处理以确保清晰的演示音频效果

**专注学习：**
```
Lo-fi chill hop, relaxing and cozy, with soft piano and vinyl crackle, slow groove, no vocals, for studying
```

**中文翻译：** 低保真放松嘻哈音乐，舒缓而温馨，配合柔和的钢琴声和黑胶唱片噪音，慢节奏，无声乐部分，适合学习专注

### 🎮 游戏配乐场景

**8-bit复古游戏：**
```
8-bit chiptune, energetic and playful, retro game music style, fast tempo, instrumental, for arcade game
```

**中文翻译：** 8位芯片音乐，充满活力且有趣，复古游戏音乐风格，快节奏，纯音乐，适用于街机游戏

**电影感游戏：**
```
Cinematic trailer music, epic and dramatic, full orchestra with heavy percussion, building intensity, choir, for action movie
```

**中文翻译：** 电影预告片音乐，宏大而戏剧性，全管弦乐队配重打击乐，逐渐增强强度，合唱团，适用于动作片

### 🌙 睡眠放松场景

**助眠音乐：**
```
Ambient sleep music, peaceful and calming, with soft pads and nature sounds, very slow, no percussion, instrumental, for relaxation
```

**中文翻译：** 环境睡眠音乐，宁静而舒缓，配合柔和的合成音效和自然声音，极慢节奏，无打击乐，纯音乐，用于放松

## 💡 高级技巧与最佳实践

### 🎨 参数搭配建议

**BPM选择：**
- 60-80 BPM：舒缓、冥想、助眠
- 80-120 BPM：中等强度、背景音乐
- 120-140 BPM：运动、活力、兴奋
- 140+ BPM：高强度训练、激烈活动

**情绪匹配原则：**
- 选择与场景相符的情绪
- 考虑目标听众的感受
- 保持情绪的一致性

**乐器搭配技巧：**
- 避免过多乐器造成混乱
- 主乐器要突出，伴奏要协调
- 考虑音色的互补性

### 🔧 常见问题和解决方案

**问题1：生成的提示词不够详细？**
**解决方案：** 提供更多具体细节，如"BPM数值"、"具体乐器名称"、"特定效果"等

**问题2：想要特定风格但找不到合适参数？**
**解决方案：** 尝试组合关键词，如
```
"80s synthwave"、"British pub rock"、"vintage jazz"
```

**问题3：需要指定中文演唱？**
**解决方案：** 在提示词中添加
```
"Mandarin"、"Chinese"或"singing in Chinese"
```

**问题4：生成的音乐不符合预期？**
**解决方案：** 
1. 检查参数是否准确
2. 尝试不同的模板组合
3. 参考已有成功案例进行调整

## 🤝 贡献、支持与赞助

### 如何贡献

我们欢迎任何形式的贡献！请通过以下方式参与：

1. **报告问题**：发现bug或改进建议
2. **分享经验**：提交实用的使用案例
3. **完善文档**：帮助改进使用说明
4. **功能建议**：提出新的功能想法

### 获取支持

如果您在使用过程中遇到任何问题，可以通过以下方式获得帮助：

- **工具官网**：https://skill.sunoai.wiki
- **公众平台 & 社交媒体 & 短视频平台**：AI音乐训练营（微信公众号、视频号、小红书、抖音、快手、百度贴吧搜索"AI音乐训练营"，B站搜索账号"猫头鹰AI音乐训练营"）
- **问题反馈 & 技术交流 & 项目合作**：邮箱：aimusicalliance@gmail.com / aimusician@126.com，微信号：SunoMusic

### 如何赞助

本工具免费开源，没有任何收益来源，如果你觉得这个工具确实对您有帮助，可以赞助我们，建议订阅我们「AI音乐训练营」知识星球：https://t.zsxq.com/tt16V，后续我们会考虑弄个「赞助名单」把赞助的用户名单统一展示在这个页面，作为感谢。

## 🙏 致谢

感谢所有为这个项目提供帮助的开源社区以及做出贡献的用户朋友们！

特别鸣谢：
- Suno AI官方团队
- OpenClaw & Clawhub开源社区
- Github开源社区
- 所有测试和使用本工具的用户

---

**猫头鹰AI音乐训练营，成就你的音乐人梦想！**

⭐ 如果这个工具对您有帮助，请给个Star支持我们继续改进！
