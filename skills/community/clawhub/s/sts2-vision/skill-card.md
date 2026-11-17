## Description:

Sts2 Vision captures the Slay the Spire 2 game window and uses OCR to monitor combat data, DPS statistics, and JSON combat reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[erebuscry](https://clawhub.ai/user/erebuscry)

### License/Terms of Use:

MIT-0

## Use Case:

Players, streamers, and developers use Sts2 Vision to monitor Slay the Spire 2 combat state, calibrate screen regions, and produce DPS or combat reports from local screen captures.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures a local game window and can write screenshots or JSON combat reports.

Mitigation: Run it only against the intended Slay the Spire 2 window, review ROI and screenshot settings before use, and keep generated reports in a local path you control.

Risk: The security evidence flags under-disclosed system-wide mouse click monitoring in monitor_v2.py.

Mitigation: Review or disable monitor_v2.py before use, and use a non-click-monitoring entry point when click attribution is not needed.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/erebuscry/skills/sts2-vision)

## Skill Output:

**Output Type(s):** [guidance, shell commands, configuration, JSON]

**Output Format:** [Markdown guidance with inline shell commands and JSON configuration examples; generated combat reports are JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May read a local game window and write local screenshots or combat report files when configured.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
