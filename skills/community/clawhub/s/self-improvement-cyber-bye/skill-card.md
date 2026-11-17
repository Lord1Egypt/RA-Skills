## Description:

Captures agent errors, hallucinations, logic bugs, and user corrections, then uses persistent memory and scheduled reviews to triage, self-fix, or escalate them.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyber-bye](https://clawhub.ai/user/cyber-bye)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to give an agent persistent self-review workflows for capturing mistakes, reviewing them on a nightly schedule, and escalating unresolved issues to a workspace owner.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can persist user and session information as future memory.

Mitigation: Install only where users have reviewed the memory behavior and can inspect, limit, or remove stored memory files.

Risk: The skill is designed to mutate local tracking files automatically.

Mitigation: Review workspace changes after use and restrict write access to the intended skill state directories.

Risk: The skill includes a permanent nightly review cron that resists deletion.

Mitigation: Install only if scheduled review behavior is desired and the operator can disable or remove the cron files.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/cyber-bye/skills/self-improvement-cyber-bye)
- [JSON Schema Draft 7](http://json-schema.org/draft-07/schema#)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [Markdown guidance and local tracking files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create and update memory, error, review, stats, and cron files inside the workspace.]

## Skill Version(s):

4.0.1 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
