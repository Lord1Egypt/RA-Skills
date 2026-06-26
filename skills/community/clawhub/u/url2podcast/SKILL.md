---
name: podcast-maker
description: "Use when 需要把网页内容转成双人中文播客，并按脚本逐句参数合成音频后输出成品"
metadata: { "openclaw": { "emoji": "🎙️", "requires": { "bins": ["ffmpeg", "curl", "python3"], "env": ["VOLC_APPID", "VOLC_TOKEN"] } } }
---

# Skill: 链接转播客制作器

输入一个链接，输出一个可播放的双人播客音频文件。

## 固定约束

- TTS 服务：火山引擎 HTTP 接口（`https://openspeech.bytedance.com/api/v1/tts`）
- 集群固定：`volcano_tts`
- 主持人音色固定：`zh_female_qingxinnvsheng_uranus_bigtts`（小何）
- 嘉宾音色固定：`zh_male_taocheng_uranus_bigtts`（小天）
- 必须先生成完整对话内容，再生成json脚本文件
- 所有文件都必须生成在skills/podcast-maker/workspace目录下
- 每次执行之前必须清空skills/podcast-maker/workspace目录
- 只能生成skill内规定的文件，不要生成其它不相关的文件，你的文件工作区仅限于skills/podcast-maker/workspace

## 标准流程

1. 读取链接正文
2. 先生成素材摘要文件 `source_brief.json`
3. 生成完整对话内容文件 `podcast_content.md`
4. 对内容做质量评分，不达标则重写（最多2轮）
5. 基于内容生成结构化脚本 `podcast_script.json`（按上下文补情感）
6. 读取脚本 `lines[]` 逐句调用 TTS，生成 `chunks/*.wav`
7. 生成 `chunks/list.txt` 并顺序合并
8. 导出 `podcast_final.mp3` 并发送

## 素材摘要契约（新增）

先生成 `source_brief.json`，避免直接写空泛文案：

```json
{
  "topic": "主题",
  "core_claims": ["3-5条核心观点"],
  "key_facts": ["3-8条可复述事实"],
  "debate_points": ["1-3个可讨论分歧点"],
  "actions": ["2-4条可执行建议"]
}
```

要求：

- `core_claims` 必须和原文一致，不可臆造
- `key_facts` 尽量具体，少用空泛词
- 后续 `podcast_content.md` 必须覆盖大部分 `core_claims`

## 内容稿契约（先于脚本）

先生成 `podcast_content.md`，结构最少包含：

- 开场（主持人）
- 主题展开（主持人与嘉宾轮流）
- 结尾总结（主持人）

要求：

- 内容自然口语化，不要照读原文
- 保留对话上下文，后句能承接前句
- 每句尽量 10-30 字，便于 TTS 自然停顿
- 角色前缀只保留在内容稿中；生成脚本时要去掉前缀
- 每个角色至少 2 次追问/反问，避免“轮流念稿”
- 结尾必须有 2-3 条行动建议

## 内容质量评分（不达标重写）

对 `podcast_content.md` 做 1-10 分评分：

- 信息密度（是否具体，不空泛）
- 逻辑连贯（是否有承接）
- 对话感（是否有互动追问）
- 可听性（句长、停顿是否自然）
- 可执行性（结尾建议是否可落地）

规则：

- 任一项 `<8`：必须重写
- 最多重写 2 轮，仍不达标则返回问题点

## 脚本文件契约（强制）

脚本阶段必须输出 JSON 文件 `podcast_script.json`：

```json
{
  "title": "播客标题",
  "summary": "一句话摘要",
  "lines": [
    {
      "idx": 1,
      "speaker": "host",
      "text": "欢迎收听，今天我们先说核心结论。",
      "voice_type": "zh_female_qingxinnvsheng_uranus_bigtts",
      "emotion": "neutral",
      "speed_ratio": 0.95
    },
    {
      "idx": 2,
      "speaker": "guest",
      "text": "好的，我补充两个关键原因。",
      "voice_type": "zh_male_taocheng_uranus_bigtts",
      "emotion": "neutral",
      "speed_ratio": 0.95
    }
  ]
}
```

## 脚本校验规则

- `idx` 必须递增、连续
- `speaker` 仅允许 `host` 或 `guest`
- `speaker=host` 必须映射 `zh_female_qingxinnvsheng_uranus_bigtts`
- `speaker=guest` 必须映射 `zh_male_taocheng_uranus_bigtts`
- `text` 不允许带“主持人：/嘉宾：”前缀
- `emotion` 推荐值：`neutral` / `happy` / `sad` / `serious` / `excited`
- 若使用了接口不支持的 `emotion`，自动回退为 `neutral`
- `speed_ratio` 建议范围 `0.90-1.05`

## Emotion 建议映射

- 开场欢迎、轻松过渡：`happy`
- 客观陈述、数据说明：`neutral`
- 风险提醒、负面新闻：`serious` 或 `sad`
- 观点碰撞、结论强调：`excited`
- 不确定时：`neutral`（默认）

## 生成脚本 Prompt（建议）

```text
你是播客脚本生成器。请基于 podcast_content.md 生成 JSON，不要输出其他文本。

要求：
1) 输出结构必须符合 podcast_script.json 契约（title/summary/lines）
2) lines 每句都要有 idx/speaker/text/voice_type/emotion/speed_ratio
3) 主持人固定音色：zh_female_qingxinnvsheng_uranus_bigtts
4) 嘉宾固定音色：zh_male_taocheng_uranus_bigtts
5) text 中不要出现角色前缀（例如“主持人：”）
6) emotion 必须结合上下文：承接、转折、强调、风险提示分别给出不同情感
7) emotion 优先从 `neutral/happy/sad/serious/excited` 选择；不确定用 `neutral`
8) 默认 speed_ratio=0.95
9) 严禁输出脚本以外的解释文本
```

## 最小播客模板

### 模板1：快讯简报（2-3分钟）

- 开场：一句话讲发生了什么
- 中段：3个关键信息点
- 结尾：一个建议 + 下一步观察点

### 模板2：深度拆解（4-6分钟）

- 开场：背景与核心问题
- 中段：原因 -> 影响 -> 应对
- 结尾：3条可执行结论

### 模板3：观点辩论（3-5分钟）

- 开场：抛出争议问题
- 中段：正反观点各2点并交叉追问
- 结尾：边界条件下的平衡结论

## TTS 执行（按脚本逐句）

环境变量（必填）：

```bash
export VOLC_APPID="你的AppID"
export VOLC_TOKEN="你的AccessToken"
```

单句请求模板（从 `lines[i]` 取值）：

```bash
curl -sS "https://openspeech.bytedance.com/api/v1/tts" \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer;${VOLC_TOKEN}" \
  -d "{
    \"app\": {\"appid\": \"${VOLC_APPID}\", \"token\": \"${VOLC_TOKEN}\", \"cluster\": \"volcano_tts\"},
    \"user\": {\"uid\": \"podcast-maker\"},
    \"audio\": {\"voice_type\": \"${VOICE_TYPE}\", \"encoding\": \"wav\", \"speed_ratio\": ${SPEED_RATIO}, \"emotion\": \"${EMOTION}\"},
    \"request\": {\"reqid\": \"${REQID}\", \"text\": \"${TEXT}\", \"text_type\": \"plain\", \"operation\": \"query\"}
  }" > "${OUT_JSON}"
```

解码 `data(base64)` 到 wav：

```bash
python3 - <<'PY'
import base64, json, sys
p = sys.argv[1]
o = sys.argv[2]
data = json.load(open(p, "r", encoding="utf-8"))
b64 = data.get("data")
if not b64:
    raise SystemExit(f"TTS failed: {data}")
open(o, "wb").write(base64.b64decode(b64))
PY "$OUT_JSON" "$OUT_WAV"
```

## 顺序合并

```bash
ls chunks/*.wav | sort | sed "s/^/file '/;s/$/'/" > chunks/list.txt
ffmpeg -f concat -safe 0 -i chunks/list.txt -c copy podcast_final.wav
ffmpeg -i podcast_final.wav -codec:a libmp3lame -b:a 192k podcast_final.mp3
```

## 最小执行模板

```javascript
// 1) 先提炼 source_brief.json
const brief = await llm_generate_source_brief(content);
writeFile("source_brief.json", brief);

// 2) 基于 source_brief 生成完整对话稿
let contentDraft = await llm_generate_podcast_content(content, brief);
writeFile("podcast_content.md", contentDraft);

// 3) 质量评分，不达标重写（最多2轮）
for (let i = 0; i < 2; i++) {
  const score = await llm_score_content(contentDraft);
  if (score.min >= 8) break;
  contentDraft = await llm_rewrite_content(contentDraft, score.issues);
  writeFile("podcast_content.md", contentDraft);
}

// 4) 基于对话稿生成结构化脚本
const script = await llm_generate_script_json(contentDraft);
writeFile("podcast_script.json", script);

// 5) 读取并校验脚本
const parsed = JSON.parse(readFile("podcast_script.json"));
validate(parsed);

// 6) 逐句合成
for (const line of parsed.lines) {
  const wav = await volcTts(line.text, line.voice_type, line.emotion, line.speed_ratio);
  saveToChunks(line.idx, line.speaker, wav);
}

// 7) 按 idx 顺序合并并导出 mp3
mergeChunksToMp3();
```

## 常见问题

- `401`：检查 `Authorization: Bearer;${VOLC_TOKEN}`，分号不可漏
- 无 `data`：查看返回 `code/message`，常见是 token 或 voice_type 不匹配
- emotion 参数报错：将该句 `emotion` 改为 `neutral` 后重试
- 中文不自然：去掉角色前缀，缩短句长，`speed_ratio` 调到 `0.92-0.98`
- 合并失败：先确认 `chunks/*.wav` 可播放，再检查 `chunks/list.txt`

## 输出标准

- 必须产出 `source_brief.json`
- 必须产出 `podcast_content.md`
- 必须产出 `podcast_script.json`
- 必须产出 `podcast_final.mp3`（或 `podcast_final.wav`）
- 失败时必须附带错误原因和可重试命令