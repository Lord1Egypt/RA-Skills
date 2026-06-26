# 背景音乐生成（Step 4）

生成无歌词的背景音乐(BGM)，时长等于视频总时长。

## 执行步骤

### 1. 分析故事情绪
从 `visual_desc` 中提取情绪基调：
- 温馨/治愈 → 轻柔钢琴、acoustic
- 冒险/动作 → 激昂管弦、epic orchestral
- 神秘/奇幻 → 空灵电子、ambient
- 欢快/童趣 → 活泼旋律、playful
- 史诗/宏大 → 交响乐、cinematic

### 2. 构建 prompt

```
[情绪基调] + [音乐类型] + instrumental, no vocals, no lyrics + [时长要求]
```

示例：
```
Warm and heartfelt acoustic guitar melody, gentle piano accompaniment,
cinematic film score style, emotional and touching,
instrumental only, no vocals, no lyrics,
suitable for storytelling video, 48 seconds duration
```

### 3. 调用 gen_music
- duration: 视频总时长（如 48 秒）
- style: instrumental / no vocals
- prompt: 基于情绪分析构建

### 4. 保存输出
`output/bgm.mp3`

## 音乐风格映射
| 视频类型 | 推荐风格 |
|---------|---------|
| 温馨故事 | soft piano, acoustic guitar, warm strings |
| 冒险动作 | epic orchestral, drums, brass |
| 童话奇幻 | magical bells, harp, ethereal synth |
| 日常治愈 | lo-fi, jazz piano, ambient |
| 史诗叙事 | cinematic orchestra |
| 自然风景 | ambient, nature sounds |

## 注意事项
1. **无歌词**: prompt 必须强调 instrumental, no vocals
2. **时长精确**: BGM 时长必须等于视频总时长
3. **情绪统一**: 音乐风格需与视频整体情绪匹配
