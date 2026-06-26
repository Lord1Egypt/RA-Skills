## Description: <br>
Route Work invisibly classifies agent tasks and selects Codex or Claude, reasoning effort, context shape, execution style, and verification profile for agent, oneshot, Slack, CLI, repo, deploy, review, or operational work. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adwilkinson](https://clawhub.ai/user/adwilkinson) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to automatically route work between Codex and Claude and choose reasoning, context, execution, and verification settings without asking the user to make those selections manually. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently change provider routing, reasoning effort, execution style, and verification profile across broad operational and deployment work. <br>
Mitigation: Review routing decisions for high-impact tasks such as deploys, release promotion, Slack/email/admin operations, and production-service work; prefer an explicit routing notice or manual override in those cases. <br>
Risk: The skill instructs agents not to add approval or risk gates and to keep routing invisible in normal conversation. <br>
Mitigation: Apply the server security guidance before installation and require human review for workflows where invisible routing or reduced verification could affect production systems or external communications. <br>


## Reference(s): <br>
- [oneshot-cli repository](https://github.com/ADWilkinson/oneshot-cli) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with inline bash and JSON code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May use oneshot route JSON fields when the oneshot CLI is available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter metadata.version is 1.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
