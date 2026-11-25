## Description:

Composite editable TextPanel text or timed captions between an original background plate and an exactly aligned background-removed foreground duplicate. Use when a creator asks for text behind a person or subject, subtitles behind the speaker, text between foreground and background, or the cutout text-behind effect. Do not use for ordinary top-layer text or standalone background removal.

This skill is ready for commercial/non-commercial use.

## Publisher:

[prosamik](https://clawhub.ai/user/prosamik)

### License/Terms of Use:

MIT-0

## Use Case:

External video creators use this skill to place editable titles or captions behind a person while keeping the original footage and text editable. It guides the agent through creating and checking an aligned foreground cutout composite in Subclip.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A foreground duplicate with mismatched timing or framing can drift from the base footage and weaken the text-behind effect.

Mitigation: Match the duplicate's source window and visual properties to the base, then inspect representative frames before completing the composite.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/prosamik/skills/subclip-text-behind-subject)

## Skill Output:

**Output Type(s):** [Guidance, API Calls]

**Output Format:** [Editable three-plane Subclip timeline composite]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preserves the base media and middle text or captions while placing a muted, background-removed duplicate above them.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
