## Description: <br>
Creates and updates WeChat article works with Weipaiban templates, AI-assisted color plans, text replacement, and optional image replacement. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[weipaiban](https://clawhub.ai/user/weipaiban) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, marketers, and operators use this skill to create or update WeChat article designs from Weipaiban templates while reviewing template choices, color changes, generated text, image classification, optional generated images, and the final update summary. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses sensitive Weipaiban API credentials and may optionally use Volcengine/Jimeng credentials for image generation. <br>
Mitigation: Install only when comfortable providing those credentials; use scoped Weipaiban keys and prefer temporary Volcengine credentials with limits when enabling image generation. <br>
Risk: Prompts, generated images, and uploaded assets may be sent to weipaiban.cn and, when Step 8 is enabled, Jimeng/Volcengine services. <br>
Mitigation: Review generated text, image prompts, image outputs, and the final change summary before approving updates; skip image generation when external image processing is not appropriate. <br>
Risk: The workflow writes task data and images under /tmp/weipaiban-task-* and may cache the rembg u2netp model under ~/.u2net/u2netp.onnx. <br>
Mitigation: Run in an isolated workspace for sensitive projects and delete /tmp/weipaiban-task-* or ~/.u2net/u2netp.onnx after completion if local residue is a concern. <br>
Risk: Optional dependency installation can add local packages or skills. <br>
Mitigation: Only run installation commands after reviewing the displayed command and confirming the dependency is needed; the artifact states that pip or skill installation is not automatic. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/weipaiban/weipaiban-skill) <br>
- [Publisher profile](https://clawhub.ai/user/weipaiban) <br>
- [API endpoints and response formats](references/api-formats.md) <br>
- [Runtime dependencies and data flow](references/runtime-dependencies.md) <br>
- [Error handling](references/error-handling.md) <br>
- [Usage example](examples/usage-example.md) <br>
- [Weipaiban API key settings](https://weipaiban.cn/settings/api-keys) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, JSON files] <br>
**Output Format:** [Markdown guidance with inline shell commands, JSON task files, API request templates, progress summaries, and a final edit link.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a WEIPAIBAN_API_KEY; optional image generation uses Volcengine/Jimeng credentials, jimeng-ai, python3, and rembg.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
