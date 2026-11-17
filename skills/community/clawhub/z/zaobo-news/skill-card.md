## Description:

Generates a Zao Live morning-news audio share card when a user asks to listen to 早播, news, or podcast-style audio.

This skill is ready for commercial/non-commercial use.

## Publisher:

[emotibot5](https://clawhub.ai/user/emotibot5)

### License/Terms of Use:

MIT-0

## Use Case:

External users and chat-agent operators use this skill to turn Chinese news, podcast, or audio listening requests into a clickable Zao Live share link for the latest 早播 audio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad Chinese news, podcast, or audio trigger phrases may route ambiguous requests to a Zao Live share link unexpectedly.

Mitigation: Narrow trigger phrases or require clarification for ambiguous news, podcast, or audio requests before deployment.

Risk: Generated share links may expire or become inaccessible.

Mitigation: Regenerate the share link when access fails and communicate that links may be time-sensitive.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/emotibot5/skills/zaobo-news)
- [Zao Live](https://zao.live)
- [Zao Live new share endpoint](https://zao.live/zaobo/newshare)

## Skill Output:

**Output Type(s):** [text, markdown]

**Output Format:** [Markdown link]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Clickable link containing a time-sensitive Zao Live share URL.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact notes)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
