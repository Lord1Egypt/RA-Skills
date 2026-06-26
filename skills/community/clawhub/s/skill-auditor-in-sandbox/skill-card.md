## Description: <br>
Launch a NovitaClaw (OpenClaw) sandbox, install a specified skill, and generate an installation and security audit report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freecodewu](https://clawhub.ai/user/freecodewu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use this skill to test ClawHub or GitHub skills in an isolated NovitaClaw sandbox before installing them locally. It installs a target skill, scans files for suspicious patterns, URLs, external paths, and dependencies, and produces a structured installation and risk report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The audit script can collect and print more skill file contents than the selected target, which may expose unrelated skill source text or secrets in the sandbox. <br>
Mitigation: Use only in a fresh disposable NovitaClaw sandbox with no unrelated installed skills or secrets, and prefer a version that limits scans to the requested skill directory and redacts likely secrets. <br>
Risk: The release security verdict is suspicious because the collected report may include raw source text from scanned files. <br>
Mitigation: Review generated reports before sharing or storing them, and remove sensitive source text or credentials if present. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/freecodewu/skill-auditor-in-sandbox) <br>
- [Project homepage from metadata](https://github.com/freecodewu/skill-auditor-in-sandbox) <br>
- [NovitaClaw documentation](https://novita.ai/docs/guides/novitaclaw) <br>
- [Claude Code documentation](https://claude.ai/claude-code) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown report with JSON script outputs and inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes installation status, installed files, security findings, URL references, external path references, dependencies, recommendations, and sandbox lifecycle commands.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
