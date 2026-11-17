## Description:

Anticipates needs, keeps work moving, and improves through use so the agent gets more proactive over time.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wjtmatch](https://clawhub.ai/user/wjtmatch)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and agent operators use this skill to make an agent anticipate blockers, propose timely next steps, recover active task state, and follow through within explicit boundaries.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Persistent local proactivity notes may accumulate sensitive personal or workflow data.

Mitigation: Review ~/proactivity/ periodically and avoid storing secrets or sensitive personal data there.

Risk: Workspace integration snippets can shape future agent behavior.

Mitigation: Approve AGENTS, TOOLS, SOUL, or HEARTBEAT changes only after reviewing the exact proposed lines.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wjtmatch/skills/tmp-proactivity-review)
- [Skill Homepage](https://clawic.com/skills/proactivity)

## Skill Output:

**Output Type(s):** [guidance, markdown, shell commands, configuration]

**Output Format:** [Markdown guidance with inline shell commands and configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create persistent local notes in ~/proactivity/ and propose workspace integration snippets only with approval.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact frontmatter reports 1.0.1)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
