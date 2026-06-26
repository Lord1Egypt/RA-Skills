# memory-system.md — 记忆系统设计

---

## 记忆分层架构

```
┌─────────────────────────────────────────┐
│  热数据层（history.json）                │
│  - 每次交互完整快照                      │
│  - 最近 50 条                           │
│  - 可直接读取，用于快速检索              │
└──────────────┬──────────────────────────┘
               ↓ 压缩提取
┌─────────────────────────────────────────┐
│  长期记忆层（patterns.log）               │
│  - 成功案例的核心标签模式                │
│  - 无上限，追加写入                      │
│  - 承载历史偏好信号                      │
└──────────────┬──────────────────────────┘
               ↓ 读取
┌─────────────────────────────────────────┐
│  工作内存（Agent 上下文）                 │
│  - 注入 Step 2 第2、3轮的偏好信号         │
└─────────────────────────────────────────┘
```

---

## 用户评价体系（核心）

**重要设计原则：** 偏好记忆的质量取决于用户反馈的丰富度。每次生成结果展示后，须主动引导用户进行多维度评价，而非简单"喜欢/不喜欢"。

### 评价话术（展示给用户）

每次生成结果返回后，使用以下话术引导用户评价：

```
🎵 第 X 版已就绪（相关性：X.X）

【歌名】{title}
【试听】{audio_url}
【风格】{theme_summary}

请告诉我：
1. 这首歌的整体感觉怎么样？（1-5星）
2. 哪个部分最吸引你？哪个部分最想改？
3. 下次创作时，你希望我往什么方向调整？

（您的评价会帮助我记住您的偏好，生成越来越符合您口味的音乐）
```

### 评分维度

| 维度 | 说明 | 权重 |
|------|------|------|
| 整体感受 | 1-5星 | 主导 |
| 风格匹配度 | 和你的预期有多接近 | 参考 |
| 歌词质量 | （有歌词时）叙事/表达是否满意 | 参考 |
| 音乐性 | 乐器/节奏/氛围是否满意 | 参考 |

### 用户反馈类型

| 反馈 | 触发操作 | HISTORY_WEIGHT |
|------|---------|----------------|
| ⭐⭐⭐⭐⭐（5星）+ 详细描述 | 写入 history.json + patterns.log | +3 |
| ⭐⭐⭐⭐（4星）+ 描述 | 写入 history.json + patterns.log | +2 |
| 喜欢（简单确认）| 写入 history.json（不带 patterns.log）| +1 |
| 一般/普通 | 不存档，但可继续生成下一轮 | 0 |
| 不喜欢/停止 | 停止，汇总结果 | -1（影响后续信号权重）|

---

## 文件格式

### history.json（热数据）

**路径：** `suno-claw/memory/history.json`

**结构：**
```json
{
  "version": 1,
  "last_updated": "2026-04-01T15:30:00+08:00",
  "entries": [
    {
      "id": "uuid-v4",
      "timestamp": "2026-04-01T15:30:00+08:00",
      "user_idea": "制作一首 Kill This Love 风格的歌曲",
      "is_instrumental": false,
      "suno_prompt": {
        "style_tags": "Korean pop, female vocals, upbeat, synth, 80s retro, driving beat",
        "lyrics": "[Verse 1]\n...\n[Chorus]\n...",
        "title": "Night Fire",
        "relevance_score": 1.0
      },
      "audio_url": "https://...",
      "user_feedback": "liked",
      "user_rating": 4,
      "user_comment": "副歌hook很抓人，但Verse可以再强化一下",
      "round_used": 1,
      "agent_a_tags": ["激烈", "释放", "黑暗荣耀"],
      "agent_b_tags": ["synth-pop", "driving beat", "high energy"]
    }
  ]
}
```

**维护策略：**
- 超过 50 条时，合并最旧的 10 条到 `patterns.log` 后删除
- 每次写入前检查文件大小（上限 1MB）

---

### patterns.log（长期记忆）

**路径：** `suno-claw/memory/patterns.log`

**结构：** 每行一条记录，Tab 分隔

```
[TIMESTAMP]\t[STYLE_TAGS_CLUSTER]\t[EMOTION_WORDS]\t[LYRIC_THEMES]\t[HISTORY_WEIGHT]
```

**示例：**
```
2026-04-01T15:30:00+08:00	Korean pop|synth-pop|upbeat	激烈|渴望|失去感	爱情|复仇|释放	3
2026-03-28T10:00:00+08:00	West coast rap|chill|lo-fi	放松|街头|自由	金钱|梦想|兄弟情	2
```

**HISTORY_WEIGHT 权重规则：**
- 用户反馈5星 + 详细描述 → +3
- 用户反馈4星 + 描述 → +2
- 用户反馈"喜欢" → +1
- 多次相同风格累积 → 叠加

**读取策略：**
- 取最近 5 条记录
- 按 HISTORY_WEIGHT 排序
- 将前 3 条编码为偏好信号注入 Step 2

---

## 偏好信号的编码与注入

### 编码格式

从 `patterns.log` 读取历史后，编码为如下文本块：

```
## 历史偏好信号（来自您的创作记忆）
- 您偏好的风格标签：[标签1]、[标签2]、[标签3]（来自您过去喜欢的作品）
- 您偏好的情绪基调：[情绪词1]、[情绪词2]
- 您偏好的歌词主题：[主题词1]、[主题词2]
- 偏好强度：HIGH / MEDIUM / LOW（根据 HISTORY_WEIGHT 总和判断）

【注入指令】在当前 RELEVANCE_LEVEL=X.X 的约束下，可适度向以上偏好方向倾斜，
但不得完全复现，须保持 X.X 对应的新鲜探索感。
```

### 注入位置

- **Agent A（歌词）** 第2、3轮 system prompt 末尾
- **Agent B（音乐性）** 第2、3轮 system prompt 末尾
- **第1轮不注入**（保持纯创意探索）

---

## 记忆写入时序

```
[Step 4 完成] → [展示评价话术] → [用户评分+反馈]
    ├─ 5星+详细 → 写入 history.json + patterns.log
    ├─ 4星+描述 → 写入 history.json + patterns.log
    ├─ 喜欢 → 写入 history.json（不追加 patterns.log）
    ├─ 一般 → 不存档，继续下一轮
    └─ 不喜欢 → 停止
```

---

## 冷启动策略

如果 `history.json` 和 `patterns.log` 均为空（首次使用），则在 Step 2 第2、3轮注入空信号（无偏好约束），完全自由探索。

---

## 数据隔离

- 所有记忆文件保存在 `suno-claw/memory/` 目录下
- 不与 `~/suno/` 或其他技能共享（避免风格污染）
- 用户可随时删除 `memory/` 目录内容进行"风格重置"
