## Description:

A text RPG skill for natural-language play across multiple fantasy and myth-inspired worlds, with persistent saves and multiplayer features in OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yumyumtum](https://clawhub.ai/user/yumyumtum)

### License/Terms of Use:

GPL-3.0-or-later

## Use Case:

Players use YumFu to play persistent, bilingual text adventures in shared fantasy, wuxia, and myth-inspired worlds. OpenClaw users can play cooperatively or competitively in supported group chats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Storybook delivery may send player content to a fixed recipient.

Mitigation: Confirm the destination and intended audience before enabling automatic delivery; avoid exporting sensitive session content until the recipient is verified.

Risk: The scan reports additional skill-install commands and external media processing whose behavior or data handling may be unexpected.

Mitigation: Review install commands before running them, confirm which media services process content, and disable image or voice features when those services are not acceptable.

Risk: The security scan is partial, with one component partially inspected and unresolved references or parser limits leaving behavior uncertain.

Mitigation: Review the partially inspected component and resolve referenced behavior before enabling the skill for sensitive use.

## Reference(s):

- [YumFu on ClawHub](https://clawhub.ai/yumyumtum/skills/yumfu)

## Skill Output:

**Output Type(s):** [Text, Images, Audio, HTML, PDF]

**Output Format:** [Interactive narrative text with scene images and voice narration; HTML storybook exports, with optional PDF export.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Bilingual Chinese and English gameplay; persistent game state and multiplayer features in supported OpenClaw chats.]

## Skill Version(s):

1.7.12 (source: package.json, release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
