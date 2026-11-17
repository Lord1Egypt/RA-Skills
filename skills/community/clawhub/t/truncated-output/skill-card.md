## Description:

The reply ends mid-sentence or mid-code-block because the model hit a token limit or was cut short.

This skill is ready for commercial/non-commercial use.

## Publisher:

[mvogt99](https://clawhub.ai/user/mvogt99)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to help agents detect truncated responses and decide whether to retry, trim context, summarize remaining work, or warn the user.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Completion checks can change response handling when truncation signals are ambiguous.

Mitigation: Prefer explicit provider finish reasons when available, check visible truncation symptoms, and surface uncertainty to the user when completion cannot be confirmed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/mvogt99/skills/truncated-output)
- [Publisher Profile](https://clawhub.ai/user/mvogt99)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guides agents to inspect finish reasons, code fences, list endings, and token or context limits before replying.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
