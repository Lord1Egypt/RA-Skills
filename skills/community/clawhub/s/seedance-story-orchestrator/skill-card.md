## Description: <br>
Orchestrate script-to-final-video production with a strict stage-gated workflow (outline -> episode_plan -> storyboard -> storyboard_images -> render), using Seedream image generation, Seedance multi-shot rendering, checkpoint-based confirmation/resume, and optional FFmpeg concatenation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[KKenny0](https://clawhub.ai/user/KKenny0) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and content-production agents use this skill to convert text, JSON, or staged story artifacts into reviewed storyboard assets, generated shot videos, and an optional merged MP4. The staged checkpoints support manual review before each major production step. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts, source material, generated metadata, URLs, and media may be handled by an external generation provider or retained in local project outputs. <br>
Mitigation: Use a dedicated ARK_API_KEY, avoid sensitive inputs unless approved for the provider, and store project directories in locations appropriate for retained media and metadata. <br>
Risk: The workflow delegates rendering to a separate Seedance video skill and uses a local FFmpeg binary. <br>
Mitigation: Install only trusted versions of the Seedance dependency and FFmpeg, and review generated checkpoints before confirming each stage. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/KKenny0/seedance-story-orchestrator) <br>
- [Design document](artifact/docs/design-doc-v0.2.0-phase1.md) <br>
- [Stage-gated logic flow](artifact/docs/logic-flow-v0.2.0-phase1.md) <br>
- [Storyboard schema](artifact/references/storyboard-v1.schema.json) <br>
- [Assets schema](artifact/references/assets-v1.schema.json) <br>
- [Staged artifacts schema](artifact/references/staged-artifacts-v1.schema.json) <br>
- [Subagent parser contract](artifact/references/subagent-parser-contract.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, files] <br>
**Output Format:** [JSON artifacts, Markdown review notes, shell commands, generated image/video files, and optional MP4 output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates staged checkpoints, storyboard/assets JSON, result indexes, generated media files, and an optional final-video.mp4.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
