## Description:

Coach Pybricks and LEGO robot debugging through evidence, one-variable tests, and observable pass/fail checks.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aimasterhao](https://clawhub.ai/user/aimasterhao)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, educators, and learners use this skill to debug Pybricks programs and LEGO robot behavior from supplied evidence. It helps identify the earliest mismatch, state one likely cause, and propose one controlled experiment with observable pass/fail checks.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Users may paste secrets, private files, or identifying information about children while asking for debugging help.

Mitigation: Ask for code, logs, telemetry, and non-identifying robot descriptions; do not request or retain secrets or child-identifying information.

Risk: Robot motion or Bluetooth access could create safety or device-permission risks if handled inside the coaching workflow.

Mitigation: Keep hardware access in a separate user-controlled Pybricks bridge or runner, and stop before motion when configuration, clearance, surface, or nearby people make testing unsafe.

Risk: Incomplete telemetry or missing robot mapping can lead to unsupported diagnoses.

Mitigation: Name evidence gaps and request the smallest useful observation instead of guessing.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aimasterhao/skills/pybricks-debug-coach)
- [Project homepage](https://github.com/aiMasterHao/pybricks-debug-coach)
- [Official Pybricks documentation](https://docs.pybricks.com/)
- [Structured contract](references/contracts.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Guidance]

**Output Format:** [Markdown sections for normal conversation or a single JSON object when structured output is requested]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Normal output uses compact coaching sections; structured output follows the debug.coach.response.v0 contract.]

## Skill Version(s):

0.1.1 (source: server release metadata and changelog, released 2026-07-27)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
