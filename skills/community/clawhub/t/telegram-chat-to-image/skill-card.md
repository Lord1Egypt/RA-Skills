## Description:

Converts Telegram Desktop JSON chat exports into long screenshot-style PNG images with bubble-style message rendering, avatars, timestamps, and text wrapping.

This skill is ready for commercial/non-commercial use.

## Publisher:

[reetyo](https://clawhub.ai/user/reetyo)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to turn trusted Telegram Desktop JSON chat exports into shareable screenshot-style PNG images for reviewing or sharing conversation history.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Untrusted Telegram export files may contain unexpected content or very large message sets.

Mitigation: Run the tool only on Telegram exports you trust and use message limits for large conversations.

Risk: Very large exports or extreme width values can create very tall images and consume significant local resources.

Mitigation: Use conservative width values, HD mode only when needed, and generate partial exports with --limit when appropriate.

Risk: The output path can overwrite an existing file.

Mitigation: Choose an output path that will not replace important files.

Risk: The skill depends on Pillow being installed in the execution environment.

Mitigation: Install Pillow in a virtual environment and consider pinning the dependency version before use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/reetyo/skills/telegram-chat-to-image)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Guidance]

**Output Format:** [Markdown guidance with CLI examples; generated output is a PNG image file.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires a Telegram Desktop JSON export and Pillow; optional inputs include message limit, sender identity, width, HD mode, and custom font.]

## Skill Version(s):

1.2.1 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
