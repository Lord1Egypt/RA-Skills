## Description:

Summarizes pasted meeting transcripts into structured summaries with decisions, action items, owners, deadlines when stated, and open items.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangjipeng977](https://clawhub.ai/user/wangjipeng977)

### License/Terms of Use:

MIT-0

## Use Case:

Employees, external users, and productivity-focused agents use this skill to turn pasted meeting transcripts into concise summaries, decisions, assigned action items, and unresolved follow-ups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The README mentions API-key configuration and write-mode examples, but the security evidence does not identify a concrete implementation requiring those privileges.

Mitigation: Install the skill as a passive transcript summarization prompt and do not provide API credentials or file-write authority unless the publisher supplies implementation details.

Risk: Meeting transcripts may contain sensitive business or personal information.

Mitigation: Keep transcript handling within the current agent session and avoid storing or forwarding transcript content unless the deployment has approved data-handling controls.

## Reference(s):

- [Skill reference index](artifact/references/index.md)
- [ClawHub skill page](https://clawhub.ai/wangjipeng977/skills/wangjipeng-meeting-transcript-to-summary)
- [Source URL from skill metadata](https://github.com/MiniMax-AI/skills)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown structured summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include explicit notes when decisions, action items, speaker names, or dates are missing from the transcript.]

## Skill Version(s):

1.0.0 (source: server release metadata; artifact metadata and changelog report 1.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
