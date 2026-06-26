## Description: <br>
Use when converting Markdown into WeChat-compatible inline HTML with theme styles for preview, copy-paste, or downstream draft publishing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhylq](https://clawhub.ai/user/zhylq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, publishers, and agent operators use this skill to convert Markdown files into WeChat-compatible HTML with inline CSS themes for preview, copy-paste editing, or downstream draft publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The converter may contact npm to install runtime dependencies during conversion. <br>
Mitigation: Run it only in environments where outbound npm access and temporary .wechat-temp creation and deletion are acceptable. <br>
Risk: Untrusted Markdown or CSS inputs can affect the generated HTML that is copied into WeChat. <br>
Mitigation: Use trusted Markdown and theme CSS inputs, and inspect the generated HTML before publishing. <br>
Risk: Choosing an existing output path may overwrite an important file. <br>
Mitigation: Select an explicit output path that is safe to replace. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhylq/zhy-markdown2wechat) <br>
- [README](artifact/README.md) <br>
- [Skill definition](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Files, Code, Guidance] <br>
**Output Format:** [HTML file plus concise text or Markdown status guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generates a WeChat-oriented HTML file with an MdWechat section wrapper and inline theme CSS.] <br>

## Skill Version(s): <br>
0.1.0 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
