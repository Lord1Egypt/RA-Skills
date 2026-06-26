## Description: <br>
Safe Skill is a programmatic static-analysis scanner that vets AI agent skills for suspicious code, URLs, credential access, obfuscation, and permission scope. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ZJZAC](https://clawhub.ai/user/ZJZAC) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and security reviewers use Safe Skill to triage ClawHub, GitHub, or local agent skills before installation by running static scans and reviewing scored findings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release includes executable malicious fixture files for scanner tests. <br>
Mitigation: Do not run files under tests/ as standalone programs; use the documented scan commands against explicit target paths. <br>
Risk: The environment audit mode can inspect sensitive local OpenClaw memory, credential metadata, installed skills, and persistence locations. <br>
Mitigation: Run --env-check only when a host audit is intended and review the target OpenClaw home path before execution. <br>
Risk: Static analysis can miss runtime-only behavior or produce false positives for legitimate automation. <br>
Mitigation: Use scan results as first-pass triage and manually review medium, high, or extreme findings before installing a skill. <br>


## Reference(s): <br>
- [Safe Skill ClawHub page](https://clawhub.ai/ZJZAC/safe-skill) <br>
- [README](artifact/README.md) <br>
- [Skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown or JSON security scan report with scored findings and command-line guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can write reports to files and returns process exit codes by risk level.] <br>

## Skill Version(s): <br>
1.2.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
