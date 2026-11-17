## Description:

Convert an X/Twitter post URL into a polished share card image by capturing the tweet content and compositing it on a styled background.

This skill is ready for commercial/non-commercial use.

## Publisher:

[efficiency97](https://clawhub.ai/user/efficiency97)

### License/Terms of Use:

MIT-0

## Use Case:

External users and content creators use this skill to turn X/Twitter post links into square social-share images with selectable background styles.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A crafted tweet URL may be passed into local browser automation before strict validation.

Mitigation: Use only trusted tweet URLs and validate or safely escape the URL before browser navigation or AppleScript execution.

Risk: Visible-browser screenshot capture can include more browser content than the intended tweet area.

Mitigation: Use a dedicated browser profile, inspect output before sharing, and delete uncropped intermediate screenshots after composing the final card.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/efficiency97/skills/tweet-share-card)
- [Skill README](README.md)

## Skill Output:

**Output Type(s):** [Files, Guidance]

**Output Format:** [PNG image file with an optional short text caption]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Square share card output; supported style presets include pink, blue-purple, purple-blue, peach, and mint.]

## Skill Version(s):

0.1.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
