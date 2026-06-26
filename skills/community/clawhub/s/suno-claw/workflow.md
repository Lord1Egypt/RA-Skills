# workflow.md — 工作流详细说明

---

## 整体 Pipeline

```
Step 1: 收集阶段
  └ 主代理解析用户创意，判断 IS_INSTRUMENTAL
  └ 输出《信息收集表》

Step 2: 双轨并行解析（3轮 × 2轨或1轨）
  └ IS_INSTRUMENTAL = false → 唤醒 Agent A（歌词）+ Agent B（音乐性）
  └ IS_INSTRUMENTAL = true  → 仅唤醒 Agent B（音乐性）
  └ Agent A/B 各跑 3 轮（Relevance: 1.0 → 0.7 → 0.5）

Step 3: 封包阶段
  └ IS_INSTRUMENTAL = false → 3个完整封包（歌词+标签）
  └ IS_INSTRUMENTAL = true  → 3个纯音乐封包（仅标签）

Step 4: 渐进生成（用户确认制）
  └ Prompt 1 → 展示 → 用户确认 → Prompt 2 → 展示 → 用户确认 → Prompt 3

Step 5: 记忆存档
  └ 用户"喜欢" → 写入 history.json + 追加 patterns.log
```

---

## Step 1：收集阶段

**目标：** 将用户模糊创意扩展为丰富的结构化信息池，并**判断是否为纯音乐需求**

### 判断逻辑（主代理自行决策）

```
用户输入 → 解析关键词：
  - 含"纯音乐" / "instrumental" / "不要歌词" / "无人声" → IS_INSTRUMENTAL = true
  - 含"说唱" / "唱歌" / "有歌词" / "vocal" → IS_INSTRUMENTAL = false
  - 模糊不清 → 默认 IS_INSTRUMENTAL = false，走歌词模式
```

**操作：**

1. 语义解析 — 解析风格、流派、情绪关键词
2. 多源信息收集（并行 web_search）：
   - 搜索风格/歌曲的乐评、Wikipedia
   - 搜索该流派的乐器特点、代表作品
3. 判断 IS_INSTRUMENTAL
4. 输出《信息收集表》

**《信息收集表》输出格式：**

```
## 信息收集表
- 原始创意：[用户输入原文]
- IS_INSTRUMENTAL：[true / false]
- 风格定位：[具体流派 + 时代背景]
- 代表艺术家：[2-3个，仅作参考]
- 歌词主题方向：[描述性主题，2-3个]（IS_INSTRUMENTAL时标注"不适用"）
- 叙事视角：[第一人称/第三人称/故事叙述]（IS_INSTRUMENTAL时标注"不适用"）
- 乐器编配：[主要乐器 3-5种]
- 唱腔特征：[描述唱法]（IS_INSTRUMENTAL时标注"不适用"）
- 情绪基调：[2-3个情绪词]
- BPM 预期范围：[如 90-120]
- 参考资料：[URL或来源]
```

---

## Step 2：双轨并行解析

### 子代理启动策略

| IS_INSTRUMENTAL | 唤醒的子代理 |
|----------------|------------|
| `false`（有歌词）| Agent A（歌词）+ Agent B（音乐性）并行 |
| `true`（纯音乐） | 仅 Agent B（音乐性） |

### 子代理 Prompt 组装规则（主代理负责）

每个子代理的 System Prompt 由主代理按以下结构组装：

```
【系统级角色定义】（来自 agent-a.md / agent-b.md）
---
【当前轮次任务】
INFO_COLLECTION_TABLE = [信息收集表全文]
RELEVANCE_LEVEL = X.X
HISTORY_SIGNAL = [来自 patterns.log 的偏好材料]
---
【关键定义】
- RELEVANCE_LEVEL = 本轮输出相对于 INFO_COLLECTION_TABLE 的相关性
- HISTORY_SIGNAL = 参考材料，子代理自行判断如何使用（不是约束）
---
【输出格式要求】
（JSON Schema，详见 agent-a.md / agent-b.md）
```

### 三轮 Relevance 策略

| 轮次 | Relevance | Agent A 策略 | Agent B 策略 |
|------|-----------|-------------|-------------|
| 第1轮 | 1.0 | 严格还原创意 | 精准匹配风格 |
| 第2轮 | 0.7 | 引入关联主题（+ HISTORY_SIGNAL 参考） | 引入关联流派变化 |
| 第3轮 | 0.5 | 高度发散，远距联想（+ HISTORY_SIGNAL 最多参考） | 大胆跨风格混搭 |

### 子代理输出校验（主代理执行）

每收到子代理输出，立即校验：

```python
def validate_agent_a(output_json: dict, expected_round: int) -> tuple[bool, list]:
    import re
    errors = []
    if "round" not in output_json or output_json["round"] != expected_round:
        errors.append(f"round字段不匹配：期望{expected_round}，实际{output_json.get('round')}")
    if "lyrics" not in output_json or "full_text" not in output_json["lyrics"]:
        errors.append("lyrics.full_text 字段缺失")
    lyrics_text = output_json["lyrics"]["full_text"]
    if "[Verse]" not in lyrics_text:
        errors.append("歌词缺少[Verse]标签")
    if "[Chorus]" not in lyrics_text:
        errors.append("歌词缺少[Chorus]标签")

    # 中文歌词行数检查：每段 Verse/Chorus ≥ 4 行
    import re
    verse_matches = re.findall(r'\[Verse\]([^[]+)', lyrics_text, re.IGNORECASE)
    chorus_matches = re.findall(r'\[Chorus\]([^[]+)', lyrics_text, re.IGNORECASE)
    for v in verse_matches:
        lines = [l.strip() for l in v.split('\n') if l.strip()]
        if len(lines) < 4:
            errors.append(f"[Verse] 段落行数不足4行：{len(lines)}行")
    for c in chorus_matches:
        lines = [l.strip() for l in c.split('\n') if l.strip()]
        if len(lines) < 4:
            errors.append(f"[Chorus] 段落行数不足4行：{len(lines)}行")

    # 中文歌词总字数 ≥ 400
    if len(lyrics_text) < 400:
        errors.append(f"歌词总字数不足400字：{len(lyrics_text)}字")

    # 歌手名检测
    ARTIST_PATTERN = re.compile(
        r'([A-Z][a-z]+ [A-Z][a-z]+|Taylor|BTS|BLACKPINK|Drake|周杰伦|蔡依林|林俊杰)',
        re.IGNORECASE
    )
    if ARTIST_PATTERN.search(lyrics_text):
        errors.append("歌词中出现歌手/艺人名字")

    # 参考歌曲名称检测
    SONG_NAME_PATTERN = re.compile(r'(东风破|晴天|以父之名|叶惠美|七里香|青花瓷|稻香|告白气球|夜曲|发如雪)')
    if SONG_NAME_PATTERN.search(lyrics_text):
        errors.append("歌词中出现参考歌曲名称（违规）：禁止直接提及任何参考曲目的歌名")

    return len(errors) == 0, errors

def validate_agent_b(output_json: dict, expected_round: int) -> tuple[bool, list]:
    errors = []
    if "round" not in output_json or output_json["round"] != expected_round:
        errors.append(f"round字段不匹配：期望{expected_round}，实际{output_json.get('round')}")
    tags = output_json.get("suno_style_tags", {})
    if tags.get("char_count", 0) > 115:
        errors.append(f"style_tags超长：{tags.get('char_count')}字符 > 115")
    if has_artist_name(tags.get("raw_tags", "")):
        errors.append("style_tags中出现歌手/艺人名字")
    if len(output_json.get("instrumentation", {}).get("primary", [])) < 3:
        errors.append("主乐器少于3种")
    return len(errors) == 0, errors
```

**校验失败时**：主代理将完整校验结果反馈给子代理，要求**重新生成当前轮次**。

---

## Step 3：封包阶段

### 任务分配

- **有歌词模式**（IS_INSTRUMENTAL=false）：
  - `Packager-1`：Agent A Round1 + Agent B Round1 → Suno Prompt 1
  - `Packager-2`：Agent A Round2 + Agent B Round2 → Suno Prompt 2
  - `Packager-3`：Agent A Round3 + Agent B Round3 → Suno Prompt 3

- **纯音乐模式**（IS_INSTRUMENTAL=true）：
  - `Packager-1-B`：Agent B Round1 → Suno Prompt 1（仅音乐性）
  - `Packager-2-B`：Agent B Round2 → Suno Prompt 2
  - `Packager-3-B`：Agent B Round3 → Suno Prompt 3

### 封包校验规则

1. `style_tags.char_count ≤ 115`
2. `lyrics` 含至少 1 个 `[Verse]` + 1 个 `[Chorus]`（有歌词模式）
3. `title ≤ 80 字符`
4. `style_tags` 无歌手名

---

## Step 4：渐进生成（用户确认制）

**核心原则：先展示，后确认，节约 API 用量**

### 流程

```
生成 Prompt 1
    ↓
返回用户：试听链接 + 完整歌词 + 核心描述（≤2句）
    ↓
询问用户反馈：【喜欢】/【一般】/【不要了】
    ↓
  ┌─ 喜欢 → 存档（Step 5）→ 可选继续生成下一轮
  ├─ 一般 → 直接生成下一轮（不存档）
  └─ 不要了 → 停止，汇总最终结果
```

### 返回用户的信息格式

```
🎵 第 X 版（相关性: X.X）

【歌名】Title
【试听】https://suno.com/...

【歌词】
[FULL_LYRICS_WITH_METATAGS]

【风格描述】
（≤2句话）
```

---

## Step 5：记忆存档

### 触发条件

用户对某版生成反馈**"喜欢"**

### 存档内容（写入 history.json）

```json
{
  "id": "uuid-v4",
  "timestamp": "ISO8601",
  "user_idea": "用户原始创意",
  "is_instrumental": "boolean",
  "suno_prompt": {
    "style_tags": "...",
    "lyrics": "...",
    "title": "...",
    "relevance_score": "X.X"
  },
  "audio_url": "https://...",
  "user_feedback": "liked",
  "round_used": 1
}
```

### 长期记忆追加（patterns.log）

```
[ISO8601]\t[STYLE_TAGS_CLUSTER]\t[EMOTION_WORDS]\t[LYRIC_THEMES]\t[HISTORY_WEIGHT]
```

**HISTORY_WEIGHT**：用户反馈"喜欢" → +1；"超级喜欢" → +2

### 历史偏好注入（后续任务）

从 `patterns.log` 读取最近 5 条 → 编码为 `HISTORY_SIGNAL` → 注入 Step 2 第2、3轮

---

## 分支场景

### 场景1：纯音乐用户输入

```
用户："制作一首chill lo-fi背景音乐"
  → Step 1 判断 IS_INSTRUMENTAL = true
  → Step 2 仅唤醒 Agent B
  → Step 3 封包仅含 style_tags + title
  → Step 4 生成纯音乐
  → 记忆存档时 lyrics 字段为空
```

### 场景2：某轮子代理校验失败

```
Agent A Round 2 校验失败（缺少[Chorus]）
  → 主代理将错误信息反馈给子代理
  → 子代理重新生成 Round 2
  → 重新校验，通过后继续 Round 3
  → 最多重试 3 次，超过则放弃该轮
```
