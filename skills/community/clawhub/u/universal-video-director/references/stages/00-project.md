# 子技能 00 · 立项 project
**来源**：drama-skills 的 short-drama 总控与初始化，claude-video-studio 的 studio.config 与关卡，ai-short-drama-from-zero 的项目诊断。

## 目标
把需求收敛成一份可执行的 `00_project.json`，后面所有阶段都从这里读参数。

## 方法
1. **先识别模式**：
   - 一句话创意 → 跳过 01，直接进 02
   - 小说或长剧本 → 先做 01
   - 参考视频 → 01 用 `reference_video` 模式
   - 已有素材 → `video_type=edit`，走 08
2. **选后端（backends）**：
   - image：如 gpt-image / seedream / comfyui
   - video：如 seedance / kling / minimax-h3 / veo
   - tts：如 elevenlabs / minimax-speech
   - compose：在 ffmpeg / remotion / hyperframes 中选
   - `max_clip_sec` 填所选模型单次能生成的最大时长
3. **gates 默认值**：
   - `story_approval`、`asset_approval`、`spend_approval` 都设为 true
   - `cut_min_sec=1`，`cut_max_sec=8`
   - `segment_max_sec` 设为 `max_clip_sec`
   - `chars_per_sec=4.5`（中文语速，英文改成约 2.8 词/秒）
   - `max_repair_rounds` 填 最大修复轮数（默认 3）
4. **按类型调整流程**：
   - comic：仍然写 06，但大部分段用 `render:"still"` 加 still_move，见第 5 条
   - promo / explainer：跳过 04，以音频节拍为时间轴
5. **render_mode（出片方式）**：
   - `video`：每个 cut 都走图生视频（drama 默认）
   - `still`：只出首帧图，用程序化运镜（推拉摇移、视差分层）加配音合成，成本约为 video 的 1/10（comic 默认）
   - `mixed`：大部分用 still，只对动作戏、高潮镜头单独标 `render:"video"`
   拿不准时，comic 推荐 mixed：既省钱，关键镜头又是动的
6. **预算**：只要用到付费接口，就要填 budget.limit。

## 产物要点
```json
{"schema":"uvd/project","version":"2","stage":"project","project_id":"ep-demo",
 "video_type":"drama","duration_sec":60,"aspect_ratio":"9:16","fps":24,"language":"zh",
 "backends":{"image":"gpt-image","video":"seedance","tts":"minimax-speech","compose":"ffmpeg","max_clip_sec":10},
 "gates":{"story_approval":true,"asset_approval":true,"spend_approval":true,"max_repair_rounds":3,
          "cut_min_sec":1,"cut_max_sec":8,"segment_max_sec":10,"chars_per_sec":4.5},
 "render_mode":"video","budget":{"currency":"CNY","limit":80}}
```
