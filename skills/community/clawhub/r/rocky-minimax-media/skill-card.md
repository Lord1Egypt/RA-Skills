## Description: <br>
Generates MiniMax images, videos, text-to-speech audio, and music through an OpenClaw plugin with interactive model and voice selection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[rockytian-top](https://clawhub.ai/user/rockytian-top) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to configure MiniMax credentials and generate images, videos, speech, and music from prompts through shell-driven plugin commands. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is flagged suspicious because an extra generate.sh script ships with a hardcoded MiniMax API key and weak credential handling. <br>
Mitigation: Do not run generate.sh as shipped; remove the embedded key, rotate any exposed key, and use a dedicated MiniMax API key. <br>
Risk: MiniMax credentials are stored in ~/.openclaw/openclaw.json or read from MINIMAX_API_KEY. <br>
Mitigation: Protect the OpenClaw config file as sensitive, restrict file permissions, and avoid committing or sharing it. <br>
Risk: Prompts, media text, and generation requests are sent to MiniMax APIs. <br>
Mitigation: Avoid sending confidential prompts or sensitive media text unless approved for that service. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/rockytian-top/rocky-minimax-media) <br>
- [MiniMax platform](https://platform.minimaxi.com/) <br>
- [MiniMax API base URL](https://api.minimaxi.com) <br>
- [MiniMax Anthropic provider endpoint](https://api.minimaxi.com/anthropic) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, API calls, Files, Guidance] <br>
**Output Format:** [Markdown documentation and bash commands; runtime output is generated image, video, MP3 speech, or music files saved to a local output directory.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, bash, and a MiniMax API key; MINIMAX_OUTPUT_DIR can override the default output directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter reports 1.3.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
