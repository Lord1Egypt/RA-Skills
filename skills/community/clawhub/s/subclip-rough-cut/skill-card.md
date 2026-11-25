## Description:

Build a clean first-draft spoken-video sequence by ordering uploaded clips, conservatively removing dead air from the actual media, transcribing each surviving item, and ripple-cutting standalone filler words such as um, uh, ah, and erm.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

Video creators and editors use this skill to assemble spoken clips in the requested order and make a conservative, editable rough cut by removing clear dead air and standalone filler words. It leaves uncertain pauses and fillers for manual review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Audio may be sent to an external cloud transcription service by default, which can expose private or confidential recordings.

Mitigation: Before use, confirm who receives the audio and that sharing is authorized; request disclosure and approval or use local transcription if available.

## Reference(s):

- [Rough-cut operating policy](references/workflow.md)
- [Subclip Rough Cut on ClawHub](https://clawhub.ai/prosamik/skills/subclip-rough-cut)

## Skill Output:

**Output Type(s):** [Editable video timeline, Editing guidance]

**Output Format:** [Editable first-assembly video timeline with a concise director-brief update]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Conservative cuts; uncertain pauses and fillers remain for manual review.]

## Skill Version(s):

1.0.0 (source: server-resolved release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
