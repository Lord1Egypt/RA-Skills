## Description: <br>
VoooAI relays creative media requests to the VoooAI backend to generate workflows, execute them, poll status, retry failed nodes, upload reference media, and download generated image, video, music, storyboard, webtoon, manga, short-drama, and marketing assets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hkljjkl](https://clawhub.ai/user/hkljjkl) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, designers, studios, businesses, educators, game developers, and agent users use this skill to turn natural-language creative requests and optional reference media into VoooAI-generated workflows and downloadable multimedia outputs. It is intended for creative workflow operations such as generation, editing, status checks, retries, and result download, not account, billing, analytics, or administration tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and selected media files are submitted to VoooAI for creative workflow generation and execution. <br>
Mitigation: Install only if you trust VoooAI with the prompts and media you submit, and use a dedicated access key where possible. <br>
Risk: Setting VOOOAI_BASE_URL can route requests, access keys, prompts, and media to an alternate server. <br>
Mitigation: Keep VOOOAI_BASE_URL unset unless the alternate server is intentionally trusted. <br>
Risk: Workflow execution can consume VoooAI points or fail when points are insufficient. <br>
Mitigation: Review estimated point costs and points warnings before execution, and require user confirmation before running points-consuming workflows. <br>
Risk: Creative media capabilities can be misused for non-consensual impersonation, deepfakes, or political disinformation. <br>
Mitigation: Decline prohibited requests, require consent for real-person likeness or voice use, and follow applicable synthetic media labeling requirements. <br>


## Reference(s): <br>
- [VoooAI homepage](https://voooai.com) <br>
- [ClawHub skill page](https://clawhub.ai/hkljjkl/voooai) <br>
- [Publisher profile](https://clawhub.ai/user/hkljjkl) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, JSON, Files, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands, JSON responses from helper scripts, and downloaded multimedia files.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires VOOOAI_ACCESS_KEY; VOOOAI_BASE_URL is optional and defaults to https://voooai.com; reference media uploads are limited to 200 MB.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
