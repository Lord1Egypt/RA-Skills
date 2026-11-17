## Description:

Helps the agent write clear git commit messages following the conventional summary line, blank line, and body format, with concrete rules for length, mood, and scope.

This skill is for research and development only.

## Publisher:

[kosmits-ai](https://clawhub.ai/user/kosmits-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers use this skill to draft, review, or improve Git commit messages, following clear rules for summaries, bodies, scope, issue references, and reverts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Commit messages remain in repository history, so including secrets, tokens, or internal hostnames could expose them over time.

Mitigation: Keep secrets, tokens, and internal hostnames out of drafted messages, and review message text before committing.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Guidance]

**Output Format:** [Plain text commit message with a summary line, blank line, and optional body and issue reference]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Does not execute Git commands.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
