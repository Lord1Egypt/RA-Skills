## Description:

Summarizes a Xiaohongshu post and representative comments into a Chinese report covering main content and audience sentiment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[xiwei26](https://clawhub.ai/user/xiwei26)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to open a provided Xiaohongshu post URL, ask the user to complete browser login when required, and produce a concise Chinese summary of the post and comment sentiment.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow may lead an agent to request sensitive account credentials such as cookies or session tokens.

Mitigation: Use only browser-based user login flows such as QR login, and do not provide cookies, session tokens, passwords, one-time codes, or other credentials through chat or prompts.

Risk: Summaries may omit context or mischaracterize representative comment sentiment.

Mitigation: Review the generated report against the source post and sampled comments before relying on it for decisions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/xiwei26/skills/rednote-summarize)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Chinese Markdown report with separate main-post and comment-summary sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires browser access to the provided Xiaohongshu URL and may require user-completed QR login.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
