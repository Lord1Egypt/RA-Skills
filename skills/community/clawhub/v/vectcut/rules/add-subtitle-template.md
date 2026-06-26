---
name: add-subtitle-template
description: "根据用户输入的音视频与结构化字幕信息，先生成或整理可上屏字幕，再自动选择并套用字幕模板，生成并执行 VectCut execute_workflow 批量写回字幕。用户提到“生成字幕并上屏/套字幕模板/按词字幕动画/基于音频或视频自动出字幕”时务必使用本技能；只要结果用于字幕上屏，严禁使用 basic 转写，必须走 nlp。若只是单纯添加一段文字、标题、标签、贴纸文案，不要使用本技能，应先走 vectcut-api-search 查找合适文字接口。"
---

# Add Subtitle Template Skill

把“字幕生成/整理 -> 模板匹配 -> 工作流执行”做成一条稳定链路，目标是批量添加模板字幕并返回可继续编辑的 `draft_id`。

技能内置脚本（按 skill-creator 规范打包在 `scripts/`，必须优先用这些脚本）：
- `<skill-path>/scripts/apply_subtitle_template.py`（统一入口：自动标准化 + 自动选模板）
- `<skill-path>/scripts/template_word_pop.py`（词块弹入）
- `<skill-path>/scripts/template_roll_focus.py`（滚动聚焦）
- `<skill-path>/scripts/template_slide_in_out.py`（句级上滑入/上滑出）
- `<skill-path>/scripts/template_karaoke_highlight.py`（逐词高亮 Karaoke）
- `<skill-path>/scripts/template_dual_track_motion.py`（交替轨道 + 关键帧上移）
- `<skill-path>/scripts/template_bilingual_keyword.py`（中英双语 + 关键词高亮）
- `<skill-path>/scripts/template_preset_transition.py`（主字幕 + 预设转场）
- 要求：先把用户输入字幕标准化为模板可接收结构，再调用模板函数产出 `draft_id + inputs + script`
- 禁止直接重写模板逻辑；只允许做“输入映射/补齐”和“执行 workflow”

## 字幕上屏硬约束

- 只要进入“字幕模板/字幕上屏/草稿写回”链路，`effect_mode=basic` 一律拒绝执行
- `basic` 仅允许用于素材分析与粗预览，不得作为上屏输入
- 发现输入里标记为 `basic`（如 `meta.effect_mode=basic` 或 `meta.asr_effect_mode=basic`）时，必须报错并要求改为 `llm-asr --effect-mode nlp`

字幕输入对齐规则（把用户字幕向 `scripts/` 模板输入靠拢）：
- 所有模板函数签名都按 `func(segments, draft_id)` 调用，核心是先构造 `segments`
- `segments` 标准项优先包含：`start`、`end`、`text`，单位统一毫秒
- 若用户给的是秒：乘以 `1000` 转毫秒；若已是毫秒：保持不变
- 若缺 `end`：用下一段 `start`，无下一段则用 `start + 1000~2000ms` 兜底
- 若要走词块模板（`template_word_pop.py`）：尽量补 `phrase=[{text,start_time,end_time}]`，无词级时间则按句子时长均分
- 若只具备句级字幕：优先走句级模板（`template_slide_in_out.py` / `template_roll_focus.py` / `template_dual_track_motion.py` / `template_preset_transition.py`）

模板调用方式（固定）：
- 优先调用统一入口：`python <skill-path>/scripts/apply_subtitle_template.py --input <subtitle_json> --draft-id <draft_id>`
- 默认随机选模板；如需复现可追加 `--selection-mode stable`
- 所有模板统一通过“命名入口函数”调用：`apply_template(segments, draft_id)`
- 模板函数返回值直接作为 `execute_workflow` 的请求体（或其主体字段），不要手工重拼一套新脚本
- 若用户显式指定模板文件名，优先按用户指定模板执行

工作流接口文档：
- https://docs.vectcut.com/363414609e0

## 鉴权前置（必须）

- 在调用 `llm-asr`、`execute_workflow` 或任何 VectCut 接口前，先检查环境变量 `VECTCUT_API_KEY`
- 若未设置 `VECTCUT_API_KEY`，必须先调用 `vectcut-login` 技能完成登录和 token 校验，再继续本技能流程
- 禁止在缺少 token 的情况下直接继续执行模板写入或工作流调用

## 适用边界（必须先判断）

- 本技能解决的是“字幕上屏”：字幕来源可以是已有 `segments`，也可以先从 `audio_url` / `video_url` 生成
- 若用户只有音频或视频，本技能链路是“先用 `llm-asr(effect_mode=nlp)` 生成结构化字幕，再套模板写回草稿”
- 若用户已经有结构化字幕和对应媒体，本技能直接做模板化上屏
- 若用户只是要“添加一段文字/标题/说明文案/标签/贴纸文案”，这不是字幕生成链路，禁止触发本技能
- 遇到“纯文字添加”诉求时，必须先转到 `vectcut-api-search` 检索合适接口（通常优先查 `add_text` 及其衍生能力）

## 何时使用

- 用户要“生成字幕并上屏”“添加模板字幕”“套用字幕模板”“词级字幕动画”
- 用户给了音频或视频素材，希望先自动生成字幕，再完成模板字幕上屏
- 用户给了结构化字幕 + 对应媒体，想把字幕批量写回已有或新建草稿
- 用户给了 `draft_id`，希望在已有草稿继续做模板字幕上屏

## 何时不要使用

- 用户只是要加一句固定文案、标题、角标、贴纸文字、口播标题条
- 用户的目标不是“字幕跟随时间轴上屏”，而是普通文字元素写入
- 这类请求必须先走 `vectcut-api-search`，确认使用 `add_text`、`add_title` 或其他更合适接口

## 输入识别（严格三分支）

先判断用户输入是否包含以下数据：
- 结构化字幕：`segments`（句级或词级时间戳，至少有 `start/end/text`）
- 媒体信息：`audio_url` / `video_url`（可单独一种，也可都有）

按以下顺序分流：

1. **仅有字幕，无音视频（情况 1.1）**
- 不执行模板写入
- 明确提示用户补充可访问的 `audio_url` 或 `video_url`
- 说明原因：缺少媒体来源会影响时间轴校验与可复现执行

2. **仅有音视频，无结构化字幕（情况 1.2）**
- 必须先调用 `llm-asr` 技能提取结构化字幕
- 默认 `effect_mode` 固定 `nlp`
- 必须先把原始素材写入草稿，再进入模板匹配：
  - 有 `video_url`：调用 `add_video`（文档：https://docs.vectcut.com/321243745e0）
  - 仅有 `audio_url`：调用 `add_audio`（文档：https://docs.vectcut.com/321196190e0）
  - 默认参数约定：`start=0`、`end=0`（表示取到源素材结尾）、`target_start=0`
  - `add_video` 关键字段：`video_url`, `start`, `end`, `target_start`, `track_name`, `draft_id`
  - `add_audio` 关键字段：`audio_url`, `start`, `end`, `target_start`, `track_name`, `draft_id`
  - `add_video` 请求示例：

```bash
curl --location --request POST 'https://open.vectcut.com/cut_jianying/add_video' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <VECTCUT_API_KEY>' \
  --header 'Accept: */*' \
  --header 'Host: open.vectcut.com' \
  --header 'Connection: keep-alive' \
  --data-raw '{
    "video_url": "https://cdn.wanx.aliyuncs.com/wanx/1719234057367822001/text_to_video/092faf3c94244973ab752ee1280ba76f.mp4?spm=5176.29623064.0.0.41ed26d6cBOhV3&file=092faf3c94244973ab752ee1280ba76f.mp4", // 视频链接
    "start": 0, // 原视频的截取开始时间，默认0
    "end": 0, // 原视频的截取结束时间，默认视频时长
    "target_start": 0, // 视频插入轨道的开始时间，默认0
    "track_name": "video_main",
    "draft_id": "<draft_id>"
  }'
```

  - `add_audio` 请求示例：

```bash
curl --location --request POST 'https://open.vectcut.com/cut_jianying/add_audio' \
  --header 'Content-Type: application/json' \
  --header 'Authorization: Bearer <VECTCUT_API_KEY>' \
  --header 'Accept: */*' \
  --header 'Host: open.vectcut.com' \
  --header 'Connection: keep-alive' \
  --data-raw '{
    "audio_url": "https://lf3-lv-music-tos.faceu.com/obj/tos-cn-ve-2774/oYACBQRCMlWBIrZipvQZhI5LAlUFYii0RwEPh",
    "start": 0, // 原音频的截取开始时间，默认0
    "end": 0, // 原音频的截取结束时间，默认音频时长
    "target_start": 0,// 音频插入轨道的开始时间，默认0
    "track_name": "audio_main",
    "draft_id": "<draft_id>"
  }'
```
  - 必须使用素材写回接口返回的 `draft_id` 作为后续编辑草稿 ID
  - 后续 `llm-asr`、模板脚本与 `execute_workflow` 必须显式传入同一个 `draft_id`，禁止新建草稿分支
- 拿到 `segments` 后，基于上述同一 `draft_id` 进入“模板匹配”步骤

3. **音视频 + 结构化字幕都已具备（情况 1.3）**
- 直接进入“模板匹配”步骤

## 模板匹配（两种情况）

### 情况 2.1：可直接套用

当字幕结构满足模板最低要求时，直接套用。默认选型顺序：

1. 有 `en` 字段或用户要求双语 -> `template_bilingual_keyword.py`
2. 有完整 `words[].start_time/end_time` 且要逐词高亮 -> `template_karaoke_highlight.py`
3. 用户要求预设样式/预设贴纸感 -> `template_preset_transition.py`
4. 用户要求交替轨道、字幕位移动画 -> `template_dual_track_motion.py`
5. 用户要求词块弹入 -> `template_word_pop.py`
6. 用户要求滚动聚焦 -> `template_roll_focus.py`
7. 仅句级普通上屏（无特殊效果）：
   - 不要固定死一个模板；默认随机分流（可切换稳定模式用于复现）
   - 可在 `template_slide_in_out.py` / `template_roll_focus.py` / `template_dual_track_motion.py` / `template_preset_transition.py` 间自动选择

### 情况 2.2：需调整后套用

若字幕结构不完整，先做最小补齐再套用模板：

- 缺 `end`：用下一句 `start` 或当前 `start + 1~2s` 兜底
- 缺词级时间戳：按句子时长均分到词/字
- 毫秒与秒混用：统一转换为秒（float）
- 空文本段：剔除
- 时长异常（`end < start`）：修正为 `end = start`

补齐完成后再次判断模板可用性，再进入套用。

## 工作流构建规范

目标是产出 `workflow_json`：
- 顶层字段：`draft_id`（可选）、`inputs`、`script`
- `script` 内步骤使用 `action/for/if/set_var`
- 批量字幕写入优先用 `for + add_text (+ add_video_keyframe)`

建议输出结构：

```json
{
  "draft_id": "可选，存在则复用",
  "inputs": {
    "subtitles": []
  },
  "script": []
}
```

说明：
- 若用户已有 `draft_id`，必须放入请求体，基于原草稿继续编辑
- 若没有 `draft_id`，不传该字段，由服务端新建草稿

## 执行步骤（必须执行）

1. 完成输入分流（1.1/1.2/1.3）
2. 完成模板匹配（2.1/2.2）
3. 生成 `workflow_json`（含 `inputs+script`，必要时含 `draft_id`）
4. 调用 `POST /cut_jianying/execute_workflow`
5. 返回结果中的：
   - `success`
   - `output.draft_id`
   - `output.draft_url`
   - `error`（若失败）

## 口播自动包装

当用户目标是“剪网感口播/开始剪口播/一键成片”，在字幕执行成功后必须追加以下步骤：

1. `add-effect_audio`：开头 `target_start=0` 添加一次提示音
2. `add-effect`：开头与重点句时间段各添加一次特效
3. `add-bgm`：查询草稿时长后自动铺满背景音乐

## 与用户交互规则

- 情况 1.1 只做补全提示，不编造素材 URL
- 情况 1.2 先告知“将先做 ASR 再套模板”，再执行
- 模板不唯一时，给出简短推荐并默认选更稳的模板：
  - 词级数据充分 -> 模板 A
  - 仅句级数据 -> 模板 B

## 输出要求

- 成功：给出本次使用模板、关键处理（是否做补齐）、`draft_id`、`draft_url`
- 失败：给出失败步骤（ASR / 模板构建 / execute_workflow）与原始错误信息
- 不要输出与用户请求无关的长解释
