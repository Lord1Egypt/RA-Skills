## Description: <br>
把抖音/小红书短视频拆成「故事+心理学」式爆款拆解报告，覆盖选题、一句话总结、内容描述、视频结构、事件推进、落幕文案、受众启示、核心爆点、节奏和 BGM 辅助分析。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jack-yang-ai](https://clawhub.ai/user/jack-yang-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content operators, marketers, and agent workflows use this skill to turn a local short-form MP4 into a narrative viral-content breakdown for scripting, storyboarding, and creative analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uploads chosen videos, optional extracted speech, and transcript-derived context to StepFun for analysis. <br>
Mitigation: Use only media approved for StepFun processing, avoid sensitive or regulated videos unless StepFun privacy and retention terms fit the use case, and review provider handling before deployment. <br>
Risk: The quickstart includes unsafe credential-handling guidance and a literal-looking API key example. <br>
Mitigation: Use a user-owned scoped StepFun API key through environment variables or a protected local secret file, rotate any copied or exposed key, and do not commit credentials. <br>
Risk: The --keep-upload option can retain uploaded media with the provider beyond the default cleanup flow. <br>
Mitigation: Use the default cleanup behavior for routine analysis and enable --keep-upload only when provider-side retention is intentional and approved. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/jack-yang-ai/video-deconstruct) <br>
- [README](artifact/README.md) <br>
- [Quickstart Guide](artifact/guides/01-quickstart.md) <br>
- [Narrative Breakdown Guide](artifact/guides/02-叙事式拆解说明.md) <br>
- [Prompt Engineering Guide](artifact/guides/03-prompt-engineering.md) <br>
- [StepFun Platform](https://platform.stepfun.com) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files, Guidance] <br>
**Output Format:** [Markdown report, JSON analysis, and optional transcript text files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes output/{video_stem}-report.md, output/{video_stem}-analysis.json, and optional output/{video_stem}-transcript.txt when ASR is enabled.] <br>

## Skill Version(s): <br>
2.0.1 (source: ClawHub release metadata; artifact frontmatter lists 2.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
