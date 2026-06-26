## Description: <br>
Converts topics or articles into high-density Xiaohongshu/RedNote knowledge carousel PNG images for entrepreneurs, business owners, and knowledge IP creators. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[horisony](https://clawhub.ai/user/horisony) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External creators, business users, and agents use this skill to turn business or knowledge content into structured RedNote carousel assets with cover hooks, dense body slides, and a closing call to action. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires an external API key and may send relevant prompt or layout content to the LibTV/Liblib provider. <br>
Mitigation: Install only if the provider is trusted, store the access key as a secret, and avoid sending sensitive or confidential content unless approved. <br>
Risk: The artifact behavior includes local file cleanup and generated output paths that need clear containment. <br>
Mitigation: Run the skill in a sandboxed workspace and confirm output and cleanup directories are scoped to the intended folder before execution. <br>
Risk: Server security evidence marks the release as suspicious because credential use and file cleanup are not clearly disclosed. <br>
Mitigation: Review the skill before installation and inspect generated HTML, shell commands, and file operations before relying on the output. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/horisony/snapdesign-rednote) <br>
- [Liblib AI API provider](https://liblib.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with HTML/CSS/JavaScript and Python/Playwright snippets; PNG files when executed] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces 1080x1440 3:4 PNG carousel images and requires a LibTV/Liblib access key.] <br>

## Skill Version(s): <br>
2.0.2 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
