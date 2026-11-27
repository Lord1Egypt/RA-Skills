# 子技能 09 · 评审 qa_report
**来源**：claude-video-studio 的 frame-critic（只看渲染帧不看代码，8 项评分加硬性上限，用接触表、360px 手机视图、剪辑点帧条和安全区叠层做证据），drama-skills short-drama-review（对照实拍效果排查是设定还是提示词出了偏差），ai-short-drama-from-zero 的根因阶段诊断。

## 目标
给出一份**可执行**的评审：分数、证据、每个问题的根因阶段和修法。

## 方法
1. **准备证据**：
   - 每镜首、中、尾帧拼成接触表
   - 每个剪辑点前后 ±6 帧做成帧条
   - 360px 宽的手机预览
   - 叠上安全区
   - 响度和时长的实测值
   - 证据文件路径写进 evidence_frames
2. **评审时切换到"独立评审"视角**，只看上面这些证据，不看提示词，避免被提示词"说服"。
3. **8 项评分（0–10）**：narrative、consistency、image_quality、camera、pacing、av_sync、captions、platform。
4. **hard_caps**：出现 identity_swap、limb_artifact、caption_unsafe、av_desync（>0.5 秒）、text_garble、axis_break 中任何一项，所有分数都不得超过 5。
5. **issues**：每个问题都要有：
   - target_ids：具体的 cut、beat 或资产 id
   - evidence：在哪一帧、看到了什么
   - root_stage：问题最早出在哪个阶段，判断方法见下表
   - fix_hint：怎么修

| 现象 | root_stage |
|---|---|
| 剧情看不懂、节奏拖沓 | story |
| 换脸、服装不一致 | assets |
| 越轴、人物位置跳变 | staging / storyboard |
| 跳切、镜头单调、镜头超长被截断 | storyboard |
| 动作不对、运镜方向错 | video_prompts |
| 伪影、畸形、单镜质量差 | production |
| 字幕、响度、入出点 | edl |

6. **pass**：所有分数 ≥ 8、没有 critical 或 major 问题、没有触发硬性上限，才算通过。是否通过由校验器复算。
