## Description: <br>
SharpAgent Content Safety Engine is a pluggable multi-jurisdiction content policy enforcer that blocks, flags, or passes content based on loaded rule sets. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yezhaowang888-stack](https://clawhub.ai/user/yezhaowang888-stack) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to apply jurisdiction-aware content safety policies before final agent output. It supports pass, flag, and block decisions with rule references and audit logging. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Unreviewed or incomplete rulesets can create incorrect compliance decisions. <br>
Mitigation: Review or supply the active rulesets before relying on the skill for compliance-sensitive workflows. <br>
Risk: Operators may not know which jurisdictions are active for a safety decision. <br>
Mitigation: Expose the active jurisdiction set in operator-facing configuration and logs. <br>
Risk: Safety logs may contain sensitive content or policy decisions. <br>
Mitigation: Define retention, access controls, and storage limits for safety logs before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yezhaowang888-stack/sharpagent-content-safety) <br>
- [Publisher profile](https://clawhub.ai/user/yezhaowang888-stack) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Configuration, Guidance] <br>
**Output Format:** [Markdown with structured YAML and JSON examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces safety verdicts, rule references, replacement text for blocked content, and audit-log records.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
