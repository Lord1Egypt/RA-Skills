## Description: <br>
Security-first skill vetting for AI agents that helps review third-party skills for red flags, permission scope, suspicious patterns, and high-risk behavior before installation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[atlaszj](https://clawhub.ai/user/atlaszj) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to vet skills from ClawHub, GitHub, or other sources before installation by reviewing source, permissions, and security red flags. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The artifact claims automatic install blocking and scanner integration, but the supplied package does not include the scanner or integration code. <br>
Mitigation: Treat the skill as advisory documentation unless the missing scanner and integration code are supplied and audited. <br>
Risk: Automatic install-blocking or cleanup hooks could disrupt installations if enabled without operational safeguards. <br>
Mitigation: Require explicit opt-in, audit logs, and rollback instructions before enabling automated blocking or cleanup behavior. <br>
Risk: Publishing guidance references a local ClawHub token file. <br>
Mitigation: Treat token files as sensitive credentials and avoid sharing, logging, or packaging them with the skill. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/atlaszj/skill-vetter-hermes) <br>
- [README](README.md) <br>
- [Integration report](INTEGRATION_REPORT.md) <br>
- [Publishing guide](PUBLISH_GUIDE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with optional shell command snippets and JSON-oriented scan examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory security review output; automatic blocking behavior is not established by the supplied artifact.] <br>

## Skill Version(s): <br>
1.2.0 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
