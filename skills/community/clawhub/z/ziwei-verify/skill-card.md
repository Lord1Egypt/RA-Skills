## Description:

Ziwei Verify calibrates Ziwei Doushu birth times from verification points by evaluating nearby Chinese-hour offsets and returning calibrated packets or review candidates.

This skill is ready for commercial/non-commercial use.

## Publisher:

[caojyb](https://clawhub.ai/user/caojyb)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill after a Ziwei chart calculation to test whether nearby birth-time offsets improve chart confidence. It can automatically return a calibrated StandardDataPacket or provide candidates for human verification.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Simulated calibration can be treated as a successful result before the Ziwei dependency path is implemented.

Mitigation: Replace and review the Ziwei invocation path, require real chart output, and block production reliance on CALIBRATION_DONE until that path is verified.

Risk: Birth time, gender, location, and chart outputs are sensitive personal data.

Mitigation: Collect the minimum needed data, avoid logging sensitive fields, and get explicit consent before sending generated prompts or packets to external LLMs.

Risk: Interactive session state lacks clear ownership checks, expiration, and deletion behavior.

Mitigation: Do not deploy the interactive handler in a shared service until per-user ownership, session expiry, and deletion controls are implemented.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/caojyb/skills/ziwei-verify)
- [Artifact README](artifact/README.md)
- [Skill definition evidence](artifact/SKILL.md)
- [Delivery report](artifact/DELIVERY.md)
- [API documentation](artifact/API文档.md)

## Skill Output:

**Output Type(s):** [JSON, markdown, text, guidance]

**Output Format:** [JSON-compatible StandardDataPacket objects with optional Markdown tables and human-facing prompt text.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may use CALIBRATION_DONE, LOW_CONFIDENCE, NEED_VERIFICATION, INVALID_INPUT, or CALIBRATION_FAILED status values.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
