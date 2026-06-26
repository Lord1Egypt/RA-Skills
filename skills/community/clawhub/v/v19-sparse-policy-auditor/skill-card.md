## Description: <br>
Audits whether agent behavior stays within a defined minimal necessary behavior set and identifies redundant, missing, or drifting constraints for governance review. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[liuyanfeng1234](https://clawhub.ai/user/liuyanfeng1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent governance reviewers use this skill to audit whether an agent's actions stay within a minimal necessary behavior set and to identify redundant, missing, or drifting behavior constraints. The resulting findings can support governance or constitution-style policy updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill examples send governance and audit data to an external service. <br>
Mitigation: Use only if you trust the endpoint, use a dedicated limited key, and redact secrets, private logs, user data, and operational details before submitting evidence. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/liuyanfeng1234/v19-sparse-policy-auditor) <br>
- [V19 Trust Manifesto](https://clawhub.com/skills/v19-trust-manifesto) <br>
- [V19 Certified Agent Workflow](https://clawhub.com/skills/v19-certified-agent-workflow) <br>
- [V19 Trust Engine](https://clawhub.com/skills/v19-trust-engine) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration, JSON] <br>
**Output Format:** [Markdown guidance with YAML, JSON, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes example requests for an external governance endpoint.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
