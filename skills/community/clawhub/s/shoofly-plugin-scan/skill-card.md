## Description: <br>
Pre-install plugin security scanner for OpenClaw plugins. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wow-leeroy-jenkins05](https://clawhub.ai/user/wow-leeroy-jenkins05) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to scan OpenClaw plugin directories before installation for credentials, obfuscated code, unusual network calls, sensitive path access, and risky exec patterns. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The submitted artifact is instruction-only, but use depends on a separate shoofly-plugin-scan executable. <br>
Mitigation: Install or run that executable only from a trusted source before scanning plugin directories. <br>
Risk: Plugin scans may inspect sensitive local directories if pointed at the wrong path. <br>
Mitigation: Run scans only against plugin directories intentionally selected for review. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/wow-leeroy-jenkins05/shoofly-plugin-scan) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Text, Guidance] <br>
**Output Format:** [Markdown with shell command examples and concise scan-result guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires the separate shoofly-plugin-scan executable to come from a trusted source.] <br>

## Skill Version(s): <br>
0.1.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
