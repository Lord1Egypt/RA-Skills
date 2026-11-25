## Description:

Clear the comment inbox under the user's own LinkedIn posts. Pulls the comments that still need an answer (already answered, own, and hidden comments are filtered out), triages each one (question, pushback, lead signal, praise, spam), drafts a reply in the user's voice, and schedules the approved replies to post under their name. Use when the user says reply to my comments, what is waiting under my posts, or wants to keep the conversation going in the first hours after publishing. Requires the Taplio MCP to read the threads, save the reply drafts, commit them, and confirm they went live.

This skill is ready for commercial/non-commercial use.

## Publisher:

[porenes](https://clawhub.ai/user/porenes)

### License/Terms of Use:

MIT-0

## Use Case:

LinkedIn creators and professionals use this skill to review unanswered comments on their own posts, draft replies in their voice, and schedule approved replies through Taplio.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Approving a reply batch may also queue public comment likes, without clear consent for the likes.

Mitigation: Confirm the user wants each comment liked before queuing likes; reply approval alone may not signal consent.

Risk: The security review reports partial scan coverage because a local reference was missing.

Mitigation: Resolve the missing reference and rerun the scan before treating its results as comprehensive.

## Reference(s):

- [ClawHub release page](https://clawhub.ai/porenes/skills/taplio-linkedin-comment-reply-manager)

## Skill Output:

**Output Type(s):** [Text, Markdown]

**Output Format:** [Markdown comment triage, reply drafts, and queue summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reply drafts are scheduled after batch approval; comment likes may also be queued during the same approval step.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
