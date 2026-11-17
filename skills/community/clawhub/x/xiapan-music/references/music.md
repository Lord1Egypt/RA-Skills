# 中文写词 & 风格标签方法论（虾盘云音乐）

> 目标：让「一句话」变成**能唱、不翻车、出整歌**的歌词 + 风格标签。
> 核心事实（2026-10-28 真机实测）：把**完整歌词**放进 `prompt` → 一次出 2 首、各约 2 分钟；
> 把**一句风格描述**放进 `prompt` → 只出 24–35 秒短 clip。**风格必须放 `tags`，歌词必须放 `prompt`。**

## 1. 段落结构（必须带标签）

用方括号英文标签，模型/上游识别最稳：

| 标签 | 作用 | 建议 |
|---|---|---|
| `[Verse 1]` / `[Verse 2]` | 主歌，讲故事 | 每段 4–8 行，画面感+细节 |
| `[Pre-Chorus]` | 过渡，蓄力 | 2–4 行，短句升高情绪 |
| `[Chorus]` | 副歌，记忆点 | 4–6 行，重复 2 次，最好有一句「钩子」 |
| `[Bridge]` | 桥段，转折 | 2–4 行，口气变化（安静/自问） |
| `[Outro]` | 收尾 | 1–3 行，情绪落地 |

- 中文歌建议总行数 **12–28 行、180–600 字**（实测 318 字出 2:11 完整歌）；上限 5000 字（接口硬限）。
- 不要写括号舞台说明（"（此处转调）"），模型会当真唱出来。

## 2. 中文歌词写法（可唱性优先）

1. **口语化**：能说出口的句子才唱得顺；少用书面长句、生僻字、拗口三连。
2. **每行 8–16 字**：太短碎、太长唱不下；主歌紧、副歌舒展。
3. **押韵**：一段内同一韵脚（如 ao/ang/ian），副歌换韵更有层次。
4. **副歌重复**：核心句原样重复 2 次以上，形成钩子（例："晚风会替我把答案吹来"）。
5. **具体意象 > 抽象口号**：写"末班车开过空空的街"而不是"感到孤独"。
6. **一段一个画面/一层情绪**，别在 4 行里塞 3 个故事。
7. 全篇统一人称与语言（中英混写容易翻车）；默认 **不改编用户原词**。

## 3. 风格标签（tags）公式

`语言 + 曲风 + 年代/参考感 + BPM + 人声 + 配器 + 情绪 + 制作`，英文、逗号分隔。

模板：

```
Mandarin indie folk pop, 96 BPM, warm male vocal with clear diction, acoustic guitar, soft live drums, warm bass, subtle strings, hopeful and gentle, clean studio recording
```

- 长度推荐 **80–200 字符**，上限 1000；**不要放中文**（中文放曲风词会被模型当歌词/理解不稳）。
- 不要写具体艺人名或受版权歌曲名（"像周杰伦"→"Mandarin pop with guofeng elements and rhythmic piano"）。
- 想要"唱得上去"就加 `comfortable vocal range, singable melody, no excessive vocal runs`。

### 常用词表

- **曲风**：indie folk pop / city pop / guofeng pop-rock / Mandopop ballad / synthwave / lo-fi hip hop / acoustic ballad / rock anthem
- **情绪**：hopeful, healing, bittersweet, nostalgic, uplifting, melancholic, playful, cinematic
- **人声**：warm male mid-range, clear female vocal, breathy, youthful, gentle spoken-word intro + sung verse
- **配器**：acoustic guitar, piano, guqin, pipa, bamboo flute, strings, live drums, soft synth pads
- **节奏**：96 BPM, 4/4, mid-tempo, slow build, half-time
- **制作**：clean studio recording, warm lo-fi texture, wide chorus, keep vocal upfront

## 4. 纯音乐 / BGM 的 prompt 写法

- 只写**风格/情绪/场景/配器/节奏**，**不要写歌词**，不要带 `[Verse]` 标签。
- 例：`轻快温馨的钢琴曲，适合短视频结尾，明亮、治愈、不抢人声`（中文 prompt 对 BGM 模型有效）。
- BGM 走 `bgm.mjs`（约 ¥1/首）；要"有人声的完整歌"走 `song.mjs`。

## 5. 出歌流程中的对应关系

| 内容 | 放哪 | 示例 |
|---|---|---|
| 完整歌词（带结构标签） | `song.mjs --lyrics*` → 请求 `prompt` | `[Verse 1]\n路灯把影子拉得很长…` |
| 风格标签（英文） | `--tags` / `--style` → 请求 `tags` | `Mandarin indie folk pop, 96 BPM, warm male vocal…` |
| 歌名 | `--title` → 请求 `title` | `晚风里的答案` |

## 6. 实测样例（2026-10-28）

- 完整歌词 318 字 + 英文 tags 223 字 + `mv: chirp-v5-5` → **SUCCESS，2 首，131.36s / 131.16s**。
- 一句中文描述（约 30 字）放 prompt → 2 首 **34.8s / 24.68s**（同一上游、同样出 2 首）。
- 两次返回的 `model_name` 都是 `chirp-hawk`、`major_model_version` 都是 `v6`，说明 **mv 不是时长开关**，时长取决于 prompt 是否是完整歌词。

## 7. 常见坑

| 坑 | 后果 | 修法 |
|---|---|---|
| 把一句风格描述当 prompt | 只出 24–35 秒短歌 | 先写成完整歌词（`lyrics.mjs`） |
| tags 写中文 | 曲风理解偏差/被当歌词 | tags 用英文风格词 |
| 歌词超 5000 字 | 提交被拒 | 精简到 12–28 行 |
| 副歌完全没有重复 | 记忆点弱、容易提前收尾 | 核心句重复 2 次 |
| 歌词里写舞台说明 | 被唱出来 | 删除括号说明 |
| 模仿具体歌手 | 效果不稳、版权风险 | 转译成高层音乐特征 |
