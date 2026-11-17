## Description:

Diagnose and document assembly, calibration, deployment, communication, camera, motion, and obstacle-avoidance problems for a lightweight OpenClaw smart cart using a 12V battery, a multi-channel servo controller, three ST3215 servos, omnidirectional wheels, and a USB camera.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jason15336804](https://clawhub.ai/user/jason15336804)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to triage OpenClaw smart-cart integration failures, sequence safe hardware and software tests, isolate likely root causes, and produce repeatable diagnostic reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Hardware troubleshooting can create motion, electrical, or battery hazards if tests are performed on an unsecured cart or live wiring is changed.

Mitigation: Secure or lift the chassis for wheel tests, isolate the 12V supply before wiring changes, and stop immediately for overheating, smoke, damaged insulation, swelling, controller resets, or uncontrolled motion.

Risk: Diagnostic reports may use Chinese section headings that are not suitable for every deployment or review workflow.

Mitigation: Review the report headings and translate or adapt them before sharing in an environment that requires another language.

Risk: The skill can propose root-cause hypotheses that are not confirmed by evidence.

Mitigation: Treat each hypothesis as unconfirmed until a single-variable test produces repeatable acceptance evidence.

## Reference(s):

- [Project baseline](references/project-baseline.md)
- [Diagnostic matrix](references/diagnostic-matrix.md)
- [Sample diagnosis](examples/sample-diagnosis.md)
- [ClawHub skill page](https://clawhub.ai/jason15336804/skills/smart-cart-integration-troubleshooter)
- [Publisher profile](https://clawhub.ai/user/jason15336804)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown diagnostic report with optional shell command output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May use Chinese report section headings and can generate a local checklist when python3 execution is available.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
