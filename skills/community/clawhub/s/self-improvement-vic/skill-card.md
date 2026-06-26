## Description: <br>
Captures learnings, errors, and corrections to enable continuous improvement for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chungvic](https://clawhub.ai/user/chungvic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to capture corrections, command failures, feature requests, and reusable learnings in local Markdown logs so later sessions can review and promote durable guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill writes local learning logs that could capture sensitive context if used carelessly. <br>
Mitigation: Follow the skill's guidance to avoid secrets, tokens, private keys, environment variables, full source files, and full transcripts; use short summaries or redacted excerpts instead. <br>
Risk: Optional hook and cross-session workflows may inspect or share session context in trusted environments. <br>
Mitigation: Enable hooks or cross-session sharing only when explicitly wanted, and share sanitized summaries and relevant file paths rather than raw transcripts. <br>
Risk: The release has no server-resolved import provenance for this version. <br>
Mitigation: Review the visible skill files during installation and avoid granting credentials or write access unless the skill clearly explains why it needs them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/chungvic/self-improvement-vic) <br>
- [Agent Skills specification](https://agentskills.io/specification) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and structured logging templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or appends local .learnings Markdown files; users should avoid logging secrets or full transcripts.] <br>

## Skill Version(s): <br>
2.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
