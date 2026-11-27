# 子技能 06 · 视频动态提示词 video_prompts
**来源**：drama-skills short-drama-video-prompts（只写起点到终点之间的动作推进和运镜；GROUP-* 多镜合生；逐镜挂图计划写清楚挂哪几张、什么顺序、每张管什么；跨镜配乐表），ai-short-drama-from-zero 的 Seedance / I2V / FLF2V 提示词打包。

## 目标
为每个 cut（或者同一 segment 内相邻短镜合并成的 GROUP）写一段可以直接复制使用的动态提示词，并绑定好参考图。

## 方法
1. **mode**：
   - 有首帧图时，默认用 `i2v`
   - 需要控制收尾画面时用 `flf2v`
   - 多参考图模型用 `ref2v`
   - 只有用户明确要求时才用 `t2v`
2. **prompt 只写变化**：动作怎么推进、视线怎么转移、运镜在什么时机、用多快速度。静态外观已经由首帧和参考图负责，不要重复描述，免得和首帧冲突。
3. **时长**：motion.duration_sec 必须等于它覆盖的 cut 时长之和（DUR_MISMATCH），并且不超过 max_clip_sec。
4. **GROUP 合生**：同一个 segment 里相邻的短镜可以合成一条 motion，按时间顺序列出 cut_ids，不能跨 segment。每个 cut 只能出现在一条 motion 里。
5. **ref_bindings**：
   - 槽位从 1 开始，不能重复
   - 首帧用 `FRAME:<cut_id>` 表示
   - 角色、场景、道具用资产 id
   - purpose 写清楚这张图负责什么（例如人脸、服装、空间）
6. **sound / music_cues**：每条 motion 写一句环境声或拟音；跨镜头的配乐在 music_cues 里按区间写情绪和 BPM。

7. **静帧段（render=still）**：不调用视频模型，只用首帧图做程序化运镜：
   - `still_move.type` 从分镜的 camera.movement 映射过来：缓推→push_in，拉远→pull_out，摇→pan_*，手持→shake，环绕→parallax
   - 推拉镜头的 from_scale 和 to_scale 必须不同，推近一般在 1.0→1.15 到 1.25 之间，不要超过 1.35，否则原图分辨率可能不够
   - 静帧通常一个 cut 一张图，单张不超过 8 秒，太长观众容易出戏
   - 需要动感时用 `layers` 叠加：雨（fx_rain）、墨迹扩散（fx_ink）、发光（fx_glow）、前后景分层视差（fg/bg）
   - 静帧段不受模型单次时长上限限制
   - `prompt` 写画面内的微动作，供剪辑做叠层参考

## 常见错误码
CUT_NO_MOTION、CUT_TWICE、DUR_MISMATCH、OVER_MODEL_MAX、NO_REF、GROUP_CROSS_SEG、RENDER_MODE、NO_STILL_MOVE、STILL_NO_DELTA
