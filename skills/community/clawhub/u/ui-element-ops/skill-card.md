## Description:

Parse UI screenshots into structured element JSON with type, OCR text, and bounding boxes, and operate desktop UI from parsed elements for locating controls, clicking, typing, taking screenshots, waiting for UI state, and calibrating coordinates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[murongg](https://clawhub.ai/user/murongg)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to inspect screenshots, identify UI elements by type, text, and coordinates, and perform requested desktop actions against parsed UI elements. It is useful for GUI automation workflows that need element JSON, overlay images, screenshots, click/type/key actions, waits, and coordinate calibration.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can capture the screen and operate the active desktop session, including clicks, typing, keys, hotkeys, and screenshots.

Mitigation: Use dry-run, list, find, and wait operations before actions; avoid running it around sensitive windows and keep GUI actions under user review.

Risk: The wait command supports a refresh shell hook that can run under-scoped commands during polling.

Mitigation: Review or remove refresh command usage and allow only explicitly approved, narrowly scoped refresh commands.

Risk: Bootstrap installs mutable third-party dependencies, clones OmniParser, and downloads model files.

Mitigation: Pin or verify the OmniParser repository, model files, and Python dependencies before running bootstrap.

## Reference(s):

- [Microsoft OmniParser](https://github.com/microsoft/OmniParser)
- [UI Element Ops ClawHub release page](https://clawhub.ai/murongg/skills/ui-element-ops)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands; generated artifacts include JSON element files and PNG overlay images.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May execute desktop actions in an active GUI session; parsing can be slow on CPU-only machines and should reuse recent elements.json outputs when practical.]

## Skill Version(s):

1.0.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
