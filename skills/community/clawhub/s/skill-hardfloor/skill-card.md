## Description: <br>
Protects against malicious or compromised OpenClaw skills by auditing newly installed skills before first use, detecting red-flag patterns, and enforcing hard-floor safety rules. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kimmi2ue](https://clawhub.ai/user/kimmi2ue) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use Skill Sentinel to review newly installed OpenClaw skills, identify red flags around credentials, external transmission, persistence, and authority escalation, and decide whether to approve first use. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The guardrail may interrupt use of other skills until the user approves them. <br>
Mitigation: Review the quarantine summary and approve only when the described behavior matches the intended use. <br>
Risk: Publisher provenance is limited, so the skill should not be treated as a complete security control on its own. <br>
Mitigation: Read the rules before relying on it and install only skills from sources the user is willing to review. <br>


## Reference(s): <br>
- [Skill Audit Checklist](references/audit-checklist.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/kimmi2ue/skill-hardfloor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown audit summaries and plain-language review prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May request explicit user approval before an unfamiliar skill is used.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
