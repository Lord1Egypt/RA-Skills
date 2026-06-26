## Description: <br>
Transforms text or image briefs into Victorian-industrial steampunk short-video generations using WeryAI Seedance 2.0. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zoucdr](https://clawhub.ai/user/zoucdr) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Creators and agents use this skill to turn user briefs or single images into confirmed WeryAI video-generation requests with steampunk prompt expansion, fixed Seedance 2.0 settings, and playable video links. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Video generation requires a WERYAI_API_KEY, network access, paid credits, prompts, and any images provided to WeryAI. <br>
Mitigation: Install only if the publisher and WeryAI are trusted, keep the API key secret, and review the full prompt and settings before submitting paid generation. <br>
Risk: Image-to-video inputs can include local image paths that the script reads and uploads to WeryAI. <br>
Mitigation: Prefer public HTTPS image URLs; use local paths only after explicit user consent and verification that the intended file should be uploaded. <br>
Risk: The generation script requires a model value but does not enforce this skill's SEEDANCE_2_0-only policy in code. <br>
Mitigation: Before running generation, confirm the JSON uses model SEEDANCE_2_0 and matches the documented duration, aspect ratio, resolution, and audio options. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zoucdr/steampunk-transform-video-gen-seedance2-0) <br>
- [Publisher profile](https://clawhub.ai/user/zoucdr) <br>
- [WeryAI video API reference](artifact/resources/WERYAI_VIDEO_API.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON command payloads and playable video links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires WERYAI_API_KEY, Node.js 18+, SEEDANCE_2_0 parameters, and user confirmation before paid generation.] <br>

## Skill Version(s): <br>
1.0.0 (source: evidence.release.version and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
