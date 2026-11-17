## Description:

Checks an agent's success claims against session records, tool outcomes, outbound delivery evidence, and request status codes, then reports whether the record matches, exceeds, or contradicts the claims.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aeneassoft](https://clawhub.ai/user/aeneassoft)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill before reporting work as done, after long sessions, or when a user questions a result, to reconcile claimed accomplishments with recorded actions and failures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill depends on the ClawPhylax plugin and may read OpenClaw transcripts and local tool-outcome ledgers.

Mitigation: Install and enable it only after confirming the local plugin dependency and session-record access are acceptable for the environment.

Risk: The skill can identify contradicted success claims or unmentioned failures before the agent reports completion.

Mitigation: Use the reported action verdict to correct contradicted claims or mention failures before proceeding.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aeneassoft/skills/what-did-i-actually-do)
- [ClawPhylax project homepage](https://github.com/aeneassoft/clawphylax)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with a required action line, evidence sections, scope notes, and a claim list]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Returns one of RECORD_MATCHES_CLAIMS, CLAIMS_EXCEED_RECORD, RECORD_EXCEEDS_CLAIMS, or NO_CLAIMS and directs correction before further action when a claim is contradicted.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
