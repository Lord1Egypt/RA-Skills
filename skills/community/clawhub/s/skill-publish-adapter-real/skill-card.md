## Description: <br>
Helps agents validate, repair, package, and publish OpenClaw or ClawHub skills through shell-based publishing workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[puppetcat-fire](https://clawhub.ai/user/puppetcat-fire) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill publishers use this skill to inspect skill packages, get repair guidance, prepare archives, and run publishing workflows for ClawHub or GitHub releases. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Security evidence marks the release suspicious because its metadata presents a validator while its instructions describe publishing automation that can change files, download or run scripts, and publish to ClawHub or GitHub. <br>
Mitigation: Install only when publishing automation is explicitly needed, and review the artifact, target directory, account, file changes, generated archives, and commands before execution. <br>
Risk: The artifact describes remote shell-script installation, chmod changes, retries, archive generation, and deletion commands that may affect local repositories or publishing accounts. <br>
Mitigation: Avoid running remote curl-installed scripts blindly; inspect scripts and proposed deletion or permission changes first, then run in a controlled workspace with the intended account. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/puppetcat-fire/skill-publish-adapter-real) <br>
- [Publisher Profile](https://clawhub.ai/user/puppetcat-fire) <br>
- [OpenClaw Documentation](https://docs.openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May recommend local file changes, permission changes, archive creation, and publishing commands that should be reviewed before execution.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
