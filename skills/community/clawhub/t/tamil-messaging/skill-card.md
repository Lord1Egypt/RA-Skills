## Description:

Handle Tamil, Tanglish and code-mixed text messages - spoken-register replies, spelling-tolerant matching, plain-text formatting, and cultural greetings for Tamil Nadu users.

This skill is ready for commercial/non-commercial use.

## Publisher:

[vigneshpy](https://clawhub.ai/user/vigneshpy)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to draft short Tamil, Tanglish, and code-mixed replies for SMS, WhatsApp, Telegram, RCS, and in-app chat while matching the user's script, tone, and channel constraints.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SMS replies in Tamil script can use UCS-2 encoding and increase message segments and cost.

Mitigation: For SMS, prefer Tanglish unless the user wrote in Tamil script first, or override this preference when preserving Tamil script matters more than segment count.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/vigneshpy/skills/tamil-messaging)
- [Publisher profile](https://clawhub.ai/user/vigneshpy)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Plain text or Markdown guidance for short-message replies]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No code execution; replies may use Tamil script, Tanglish, or code-mixed English depending on the user's message and channel.]

## Skill Version(s):

1.2.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
