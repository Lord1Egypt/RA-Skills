## Description: <br>
Security Constitution provides a four-level OpenClaw prompt-level security policy for classifying operations, requiring confirmation for high-risk actions, logging audits, and refusing critical or bypass attempts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[byronbanck-ai](https://clawhub.ai/user/byronbanck-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and operators use this skill to add a prompt-level security gate that classifies user requests, blocks critical actions, requires confirmation for high-risk actions, and records security-relevant activity. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to act as a broad prompt-level security gate, which can interrupt or refuse tasks. <br>
Mitigation: Install it only where that control behavior is intended, and define who controls security-policy.json before use. <br>
Risk: Password confirmation is under-scoped and may encourage entering reusable secrets in chat. <br>
Mitigation: Avoid reusable real passwords in chat; use a dedicated confirmation secret or an external approval process. <br>
Risk: Operation logging and notifications can expose sensitive content if ownership, access, retention, and redaction are not defined. <br>
Mitigation: Set explicit rules for what is logged, who can read logs or notifications, how secrets are redacted, and how long records are kept. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/byronbanck-ai/security-constitution) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration, Security decisions] <br>
**Output Format:** [Markdown guidance with policy examples, decision flows, JSON configuration snippets, and response templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces prompt-level allow, confirm, log, or refuse decisions; no external API output is described.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
