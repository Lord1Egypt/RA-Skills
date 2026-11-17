## Description:

Respond to review comments on a PR after evaluation and fixes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to respond to unreplied GitHub PR review comments after they have evaluated the feedback and made fixes or chosen a response strategy. It can post concise replies and resolve review threads by default.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can post replies and resolve GitHub PR review threads using the active gh login.

Mitigation: Use --pr to explicitly target the intended PR, review the queued comments before posting, and use --no-resolve when thread resolution should remain manual.

Risk: A fixed temporary jq file path can collide with another process or be overwritten.

Mitigation: Use a unique temporary file created with mktemp and remove it after the command completes.

Risk: Responding before evaluating feedback can produce incorrect or misleading PR discussion.

Mitigation: Run the prerequisite feedback-evaluation step first and only respond after each thread has a fix or an explicit response strategy.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown summary with GitHub CLI command guidance and PR reply text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May post GitHub PR review comment replies and resolve review threads through the active gh login.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
