## Description:

Provides shared voice, tone, formatting, and publishing-safety rules for social media content, including a human-approval requirement before publishing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ahmadhussain0335](https://clawhub.ai/user/ahmadhussain0335)

### License/Terms of Use:

MIT-0

## Use Case:

Creators and social media teams use this skill while drafting, editing, and reviewing platform content. It applies brand voice, formatting, and disclosure guidance, and requires human approval before publishing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote media can change without invalidating approval.

Mitigation: Review each draft and its media before approving, and recheck remote media before publishing.

Risk: Untrusted post folders may compromise the approval workflow.

Mitigation: Keep post folders trusted and have the user review and approve the exact content in their own terminal.

Risk: Companion publishing skills may have different account access and posting behavior.

Mitigation: Review each companion publishing skill's account access and publishing behavior separately.

## Reference(s):

- [Voice rules](references/voice.md)
- [Formatting rules](references/formatting.md)
- [Platform limits](references/platform-limits.md)
- [Brand voice template](assets/voice-template.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance, Shell commands]

**Output Format:** [Social media drafts and review guidance in text or Markdown, with shell command examples for approval workflows.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Content follows the selected brand voice and platform formatting guidance.]

## Skill Version(s):

0.3.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
