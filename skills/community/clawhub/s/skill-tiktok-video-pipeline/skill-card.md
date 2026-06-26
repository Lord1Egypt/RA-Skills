## Description: <br>
End-to-end TikTok ad video pipeline. Product script -> Veo base video -> animated caption overlay -> audio mix -> final MP4. One command, full automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Zero2Ai-hub](https://clawhub.ai/user/Zero2Ai-hub) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and marketing teams use this skill to generate short-form TikTok product ad videos from product identifiers, scripts, optional logos, and background audio. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill runs user-influenced shell commands. <br>
Mitigation: Install and run it only in a contained workspace, and avoid passing untrusted captions, model names, language values, product IDs, or file paths. <br>
Risk: External skill dependencies are under-declared. <br>
Mitigation: Confirm required external video-generation skills and command-line tools are installed before use. <br>
Risk: ffmpeg filter values are influenced by input values. <br>
Mitigation: Prefer a version that validates ffmpeg filter values and replaces bash -lc shell invocation with argument-array subprocess calls. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Zero2Ai-hub/skill-tiktok-video-pipeline) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [Product configuration](artifact/config/products.json) <br>
- [Asset notes](artifact/assets/README.md) <br>


## Skill Output: <br>
**Output Type(s):** [Files, Shell commands, Configuration] <br>
**Output Format:** [MP4 video files with console progress output and MEDIA path markers] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires uv, ffmpeg, node, GEMINI_API_KEY for non-dry-run Veo generation, and compatible external video-generation skills.] <br>

## Skill Version(s): <br>
2.0.0 (source: SKILL.md frontmatter, artifact metadata, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
