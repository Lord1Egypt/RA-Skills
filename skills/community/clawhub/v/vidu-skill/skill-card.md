## Description: <br>
Generate video and images by calling the official Vidu API via vidu CLI for text-to-image, text-to-video, image-to-video, reference generation, lip-sync, text-to-speech, video composition, and task checks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[calvinzhao](https://clawhub.ai/user/calvinzhao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, creators, and agent developers use this skill to submit, monitor, and retrieve Vidu media-generation tasks through the vidu-cli command line. It supports generating and editing images, videos, speech, lip-sync outputs, video timelines, reference elements, quota checks, and cost estimates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends prompts, media files, URLs, task details, and quota or credit queries to Vidu through vidu-cli. <br>
Mitigation: Use it only with content approved for Vidu processing, avoid private or regulated media unless approved, and confirm the selected Vidu region endpoint is appropriate. <br>
Risk: A VIDU_TOKEN is required for API access. <br>
Mitigation: Use a limited token where possible, keep it in the environment rather than in prompts or files, and rotate it if it is exposed. <br>
Risk: VIDU_DEBUG may print full response bodies to stderr during troubleshooting. <br>
Mitigation: Leave VIDU_DEBUG off except for trusted local debugging and review logs before sharing them. <br>
Risk: The npm install path installs vidu-cli and its platform binary dependency. <br>
Mitigation: Install only in environments where vidu-cli is trusted and where Node.js, npm, and downloaded binaries are allowed. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/calvinzhao/vidu-skill) <br>
- [Vidu Homepage](https://www.vidu.cn/) <br>
- [vidu-cli npm package](https://www.npmjs.com/package/vidu-cli) <br>
- [Vidu Task Parameters Reference](references/parameters.md) <br>
- [Video Compose Reference](references/compose.md) <br>
- [Errors and Retry Strategy](references/errors_and_retry.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal-oriented guidance with vidu-cli commands, JSON stdout fields, task identifiers, trace identifiers, status results, error fields, and downloaded file paths when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires Node.js, npm, vidu-cli, and VIDU_TOKEN; generated media is processed asynchronously by Vidu and must be polled or downloaded through task commands.] <br>

## Skill Version(s): <br>
1.4.9 (source: server-resolved release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
