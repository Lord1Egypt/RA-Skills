## Description: <br>
Fixes two OpenClaw Weixin plugin issues affecting runtime startup and Content-Length handling so the Weixin channel can send and receive messages normally. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[johnsonxuan](https://clawhub.ai/user/johnsonxuan) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators using @tencent-weixin/openclaw-weixin 2.4.1 on OpenClaw 2026.5.4+ use this skill to patch local plugin files and restore Weixin message send and receive behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill applies a local patch to installed OpenClaw Weixin plugin files, which can fail or leave the plugin in an unexpected state if the target version does not match. <br>
Mitigation: Install only for the affected Weixin plugin version, review install.sh before running it, keep the .bak backups, and restore or reinstall the plugin if the patch does not apply cleanly. <br>
Risk: Reinstalling the Weixin plugin can overwrite the patched files. <br>
Mitigation: Run the fix again after reinstalling the plugin and verify the channel with openclaw health --json. <br>


## Reference(s): <br>
- [OpenClaw GitHub Issue 78376](https://github.com/openclaw/openclaw/issues/78376) <br>
- [@tencent-weixin/openclaw-weixin npm package](https://www.npmjs.com/package/@tencent-weixin/openclaw-weixin) <br>
- [Weixin Fix Report](https://github.com/user-attachments/files/27447892/openclaw-weixin-fix-report.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell commands and patch guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May modify local OpenClaw Weixin plugin files and create .bak backups when the installation script is run.] <br>

## Skill Version(s): <br>
2.4.2 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
