## Description: <br>
Generate TikTok-style short-form ad videos with animated pill captions and built-in product presets for TikTok ads, Reels, and YouTube Shorts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External creators, marketers, and developers use this skill to turn a base MP4 into short-form product ad content with animated caption overlays and product-specific callouts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local video rendering can consume noticeable CPU, memory, and disk resources. <br>
Mitigation: Run the skill on media files you choose in an environment with adequate local resources and available output storage. <br>
Risk: Untrusted input videos or font files may increase media-processing risk. <br>
Mitigation: Prefer trusted videos and fonts, and review inputs before rendering. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-tiktok-ads-video) <br>
- [Publisher profile](https://clawhub.ai/user/Zero2Ai-hub) <br>
- [uv runtime requirement](artifact/SKILL.md) <br>
- [Example captions JSON](artifact/scripts/example_captions.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline bash commands and file path references] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Guides an agent to run local video-processing commands that produce an MP4 output file.] <br>

## Skill Version(s): <br>
2.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
