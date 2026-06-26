## Description: <br>
Audit third-party or custom skills for permission risk, unsafe commands, and integration safety. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sunbinnju-star](https://clawhub.ai/user/sunbinnju-star) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill before adopting ClawHub, Git, local, or unknown-source skills to identify permission risk, unsafe commands, source-trust gaps, and sandboxing needs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill's audit result could be mistaken for an automatic approval or rejection decision. <br>
Mitigation: Treat the output as advisory guidance and require human review before installing high-privilege skills, skills that use shell commands, credentials, broad local access, or unknown sources. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/sunbinnju-star/skill-security-auditor-jack) <br>
- [Publisher Profile](https://clawhub.ai/user/sunbinnju-star) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, text] <br>
**Output Format:** [Markdown or structured text describing risk level, suspicious actions, over-privileged permissions, installation recommendation, sandbox recommendation, and audit summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Advisory security assessment; does not execute code or automatically approve installations] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
