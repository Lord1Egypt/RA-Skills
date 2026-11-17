## Description:

Collects public X (Twitter) posts for a handle with the Actionbook Rust CLI workflow, then helps summarize findings and draft neutral recap posts or threads.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jack4world](https://clawhub.ai/user/jack4world)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to collect public posts from a specified X handle, document coverage limits, summarize themes in Chinese working notes, and prepare neutral English recap copy for publication after confirmation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can help publish posts to X, which is an external action if the target account, final text, or image is wrong.

Mitigation: Confirm the target account, final copy, and any attached image before approving publication.

Risk: Browser automation over X may produce incomplete coverage because infinite scroll is not exhaustive.

Mitigation: State the requested time window, scrolling depth or cutoff, and any uncertainty in the recap.

Risk: Recaps can misattribute quoted material or imply intent beyond the collected public posts.

Mitigation: Use neutral framing, keep verbatim quotes tied to captured post evidence, and require exact links or timestamps for interview claims.

## Reference(s):

- [Templates](references/templates.md)
- [Extraction checklist](references/checklist.md)
- [Image card without Python](references/image-card.md)
- [ClawHub skill page](https://clawhub.ai/jack4world/skills/x-actionbook-recap)
- [Publisher profile](https://clawhub.ai/user/jack4world)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with inline shell commands and concise recap text]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include Chinese working notes, English post or thread drafts, and optional image-card guidance.]

## Skill Version(s):

0.1.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
