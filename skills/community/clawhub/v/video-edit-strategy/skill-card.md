## Description: <br>
分析素材与用户意图，输出结构化 JSON 剪辑策略（分镜、时间线、转场、音频、文字）。当用户要求制作短视频、混剪、或提供了素材但未给出具体剪辑指令时调用。策略输出供 ffmpeg-cli / ffmpeg-video-editor 等下游 skill 执行。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Se7enElk](https://clawhub.ai/user/Se7enElk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and video-production agents use this skill to turn user intent and media metadata into a structured short-video editing plan. It is suited for planning timelines, pacing, transitions, audio treatment, text overlays, and downstream execution steps before an ffmpeg-based editor runs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated plans can include file paths and execution_plan steps for downstream ffprobe, ffmpeg-cli, ffmpeg-video-editor, or video-frames tools. <br>
Mitigation: Review paths and execution steps before running downstream tools, especially when paths point outside the intended media workspace. <br>
Risk: The strategy is a planning artifact and may contain incomplete or unsuitable editing decisions for the user's source media. <br>
Mitigation: Review the proposed timeline, transitions, audio levels, and text overlays before rendering the final video. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Se7enElk/video-edit-strategy) <br>
- [Strategy schema](artifact/strategy-schema.md) <br>
- [Examples](artifact/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, JSON, guidance] <br>
**Output Format:** [Structured JSON editing strategy with a short natural-language explanation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The JSON includes project settings, materials, timeline scenes, audio handling, text overlays, and an ordered execution_plan for downstream editing skills.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
