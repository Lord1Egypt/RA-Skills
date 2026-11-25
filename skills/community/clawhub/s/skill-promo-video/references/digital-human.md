# 数字人引擎决策树——skill-promo-video v2

> 选错引擎=构图漂移/口型不齐/文字花版的根因。先查表再提交。

## 一、决策表（按输入查行）

| 场景 | 引擎 | 原因 |
|---|---|---|
| 旁白 ≤5.1s 的口播段 | **H3-TALK**（ref2va 音频驱动） | 口型与音频天生同步；8 步 INT8 ~13min/段 |
| 旁白 >5.1s 的长口播 | **S2V 720p**（Wan2.2-S2V） | H3 单 clip 上限 124 帧≈5.2s |
| 无旁白、首帧微动 | **H3-I2V**（严格首帧） | 呼吸/眨眼/微晃，构图零漂移 |
| 卡面有文字对位 | H3-I2V 或（TALK+文字稳定性闸门） | ⛔ r2v 构图漂移已证伪 |
| 自由生成身份参考 | （尽量不用） | r2v 构图会漂：人物漂成中央特写、文字全错位 |

## 二、H3-TALK 要点

- 模型四件：`minimax_h3_ref2va_pruned_int8_convrot`（DiT）+ `qwen3vl_32b_minimax_h3_nvfp4_awq`（TE）+ video VAE fp16 + audio VAE fp32。
- 节点连线：`BasicGuider{model,conditioning}`、`BasicScheduler{model}`、`VAEDecodeAudio` 输入名是 `vae`；音频经 `H3ReferenceAudio(max_seconds=8.0)` 进 `ref_audios.ref_audio_0`（带点嵌套）。
- 采样：euler/beta/**8 步**；1344×768@24fps；length=ceil(秒×24)+4 上限 124。
- 提示词骨架：`Use <Picture 1> as the identity reference. The same woman speaks directly to the camera; her lip movements match <Audio 1> exactly.` + 场景/机位正向描述（固定机位/中景/自然眨眼）。
- 首帧=PE `layout=talker`（唇轻闭、面向镜头）；⛔直接喂角色卡走参考生成=脸特征消失（实测两轮）。
- 输出保留源音轨（口型同源），但入合成前一律 `-an` 剥掉、旁白统一 adelay 注入。

## 三、S2V 要点（>5.1s 长口播）

- 必须原生 720p（1280×720）——480p 非原生嘴部 ~40px 放大 2.3×=「香肠嘴」根因。
- 帧数=ceil(秒×16) 取整 4n+1；16fps；KSampler 默认 Lightning 4 步 cfg=1（~14min/113f）；全质量 20 步 cfg6 ≈2h/段。
- ⛔cfg=1 时负向提示**无效**——唇妆/质感/口型幅度约束全部写进正向 prompt。
- ⛔音频编码器必须 `wav2vec2_large_english`（chinese-base 13vs25 维度报错）。
- 模型五件：S2V-14B GGUF + wav2vec2 + umt5_xxl_fp8 + wan_2.1_vae + lightx2v 4step LoRA（≤4 步时挂）。

## 四、时长换算速查

| 旁白秒 | H3 帧数(24fps) | 可行性 |
|---|---|---|
| ≤5.1 | ≤123+4（上限 124 截断） | H3-TALK 单 clip ✓ |
| 5.2~8 | ≥129 | 超 124 上限 → S2V |
| 图页旁白（无人） | — | 静态图+TTS，不进引擎 |

## 五、GPU 串行纪律

- PE 生图（TE 常驻 ~16G）/ H3 / S2V / TTS **严禁并发**——24G 单卡一轮只驻留一个大模型。
- 切换顺序：当前任务完 → 释放（kill 残留进程 + 实例 /free）→ 下一模型加载。
- TTS 批量前确认生图队列已清（OOM 假 OK 根因）；nvidia-smi 进程级核对 <2G 残留再开新引擎。

## 六、运动链路备用方案（不依赖以上引擎时）

- 静帧+ffmpeg zoompan 推拉：确定性运镜兜底（Blender 段不过验收时的降级路线）。
- Blender 直接渲染动画：几何/运动 100% 一致，适合运镜镜头（本技能 blender_scene.py）。
