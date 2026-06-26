## Description: <br>
Runs a continuous self-improvement loop that helps the agent learn from mistakes, extract lessons, and refine its behaviour over time. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[assafster](https://clawhub.ai/user/assafster) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to maintain a privacy-safe self-improvement loop that records abstract process mistakes, extracts reusable lessons, and reviews recurring patterns across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill creates and uses persistent local agent-memory files that can influence later sessions without clear user confirmation. <br>
Mitigation: Install only when persistent local memory is intended, choose the storage location deliberately, and require confirmation before creating or modifying the memory files. <br>
Risk: Mistake logs could expose user content, credentials, or sensitive details if the privacy rules are not followed. <br>
Mitigation: Review memory files regularly and allow only abstract process observations; omit or paraphrase any detail that could reveal user-provided content or sensitive information. <br>


## Reference(s): <br>
- [Self-Improvement Protocol Reference](artifact/references/protocol.md) <br>
- [ClawHub Release Page](https://clawhub.ai/assafster/self-improvement-system) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Guidance, Configuration, Files] <br>
**Output Format:** [Markdown guidance and structured entries for local agent-memory files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates or updates local files such as mistakes.md, lessons.md, soul.md, playbook.md, session-log.md, and archived mistake logs.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
