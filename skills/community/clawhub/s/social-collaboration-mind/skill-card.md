## Description:

Social Collaboration Mind helps agents infer collaborator state from expertise, confidence, workload, trust, mood, and history signals, then choose an adaptive collaboration strategy such as delegate, consult, monitor, pair, or avoid.

This skill is ready for commercial/non-commercial use.

## Publisher:

[qq435912743](https://clawhub.ai/user/qq435912743)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent builders use this skill to select collaboration actions in human-agent or multi-agent workflows based on collaborator signals. It is suited to workflows where the useful output is a collaboration decision rather than a direct task answer.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can keep local cross-session memory in learned_patterns.json, which may retain sensitive notes or preferences.

Mitigation: Avoid storing sensitive information in the memory file and treat its contents as untrusted data during review and use.

Risk: Saved preferences or accumulated usage history could influence future agent behavior without sufficient review.

Mitigation: Require explicit confirmation before applying saved preferences and do not allow automatic rewrites of SKILL.md from usage history.

Risk: Collaboration strategy decisions can be wrong when collaborator signals are inaccurate or overconfident.

Mitigation: Review recommendations before acting on them and cross-check important delegation decisions with independent monitoring or validation.

## Reference(s):


## Skill Output:

**Output Type(s):** [Guidance, JSON, Shell commands]

**Output Format:** [JSON strategy recommendation with optional shell command usage examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces a strategy, reason, communication tone, and watch items from collaborator signal inputs.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
