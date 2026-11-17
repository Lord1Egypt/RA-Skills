## Description:

Decision aid that helps agents decide whether to continue, change approach, or stop and ask the user after repeated task failures based on recent attempts, successes, confidence bounds, and refusing hosts.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill when an agent is repeatedly failing, seeing no new evidence, encountering a refusing host, or preparing to ask whether to keep trying. It produces a concrete action recommendation and the evidence needed to either continue, change approach, or ask the user for specific access, tooling, or task changes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill works best with the ClawPhylax plugin, which keeps a local ledger of requests and tool outcomes.

Mitigation: Install and enable the plugin only after reviewing that local recordkeeping behavior; proceed without it when unavailable and state what could not be verified.

Risk: The skill can recommend stopping or changing approach based on observed attempts, but it does not know the task's value to the user.

Mitigation: When the user has marked a task as critical, include that context when stopping and ask for the specific access, tool, or task change needed.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/should-i-stop-and-ask)
- [Artifact homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown with a first-line ACTION verdict, evidence, constraints, next step, and confidence information]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include plugin installation or command guidance when the ClawPhylax plugin is not available]

## Skill Version(s):

1.0.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
