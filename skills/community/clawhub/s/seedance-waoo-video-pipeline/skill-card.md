## Description: <br>
自动化短视频工作流（story-to-video pipeline）：从剧本/分镜到生成、字幕 ASR、TTS、合并交付，支持 Seedance / Vidu / MiniMax 多厂商路由。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wusyu](https://clawhub.ai/user/wusyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and creative operators use this skill to turn a story, novel scene, or short prompt into a short-video production flow with story pack, storyboard, video generation, subtitle alignment, TTS, ambience, merging, and delivery reporting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project text, scripts, images, audio, and generated media may be sent to configured third-party providers under the operator's API keys. <br>
Mitigation: Use low-privilege, rotatable keys, review provider configuration before execution, and require explicit confirmation before paid or quota-consuming generation. <br>
Risk: API-key-bearing configuration copies may be persisted in output folders. <br>
Mitigation: Keep configuration files out of version control, inspect output directories before sharing, and scrub secrets from copied artifacts. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/wusyu/seedance-waoo-video-pipeline) <br>
- [Pipeline Overview](references/pipeline-overview.md) <br>
- [Story Pack Spec](references/story-pack-spec.md) <br>
- [Model Routing](references/model-routing.md) <br>
- [Runtime Policy](references/runtime-policy.md) <br>
- [Output Contract](references/output-contract.md) <br>
- [Checkpoint Policy](references/checkpoint-policy.md) <br>
- [Audio Policy](references/audio-policy.md) <br>
- [Seedance Prompt Engineering](references/seedance-prompt-engineering.md) <br>
- [Configuration Template](references/configuration-template.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance, Files] <br>
**Output Format:** [Markdown guidance with JSON contracts, shell commands, configuration snippets, and generated media file paths] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May emit delivery manifests and paths for raw, subtitled, voiced, final, or merged video artifacts.] <br>

## Skill Version(s): <br>
1.1.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
