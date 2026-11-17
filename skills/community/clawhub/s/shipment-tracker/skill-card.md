## Description:

Shipment Tracker helps agents track packages across USPS, UPS, FedEx, DHL, Amazon, OnTrac, and LaserShip by reading a markdown shipments file, detecting carriers from tracking numbers, checking basic web status, and suggesting browser-use for JS-heavy tracking pages.

This skill is ready for commercial/non-commercial use.

## Publisher:

[pfrederiksen](https://clawhub.ai/user/pfrederiksen)

### License/Terms of Use:

MIT

## Use Case:

External users and developers use this skill to maintain a markdown list of shipments, identify carriers from tracking numbers, and get delivery-status output or follow-up browser-use guidance when carrier pages require it.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The generated browser-use fallback can turn shipment-file link text into executable Python code if the command is run.

Mitigation: Review generated browser-use commands before execution, use only trusted shipment files, and pass tracking URLs as data rather than interpolated Python source.

Risk: The browser-use fallback sends tracking numbers, order information, package details, and carrier URLs to third-party cloud and LLM services.

Mitigation: Avoid browser-use for sensitive packages and use manual carrier tracking when shipment details should remain local.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/pfrederiksen/skills/shipment-tracker)
- [OpenClaw](https://openclaw.ai)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text status summaries, JSON objects, and inline shell commands for optional browser-use follow-up.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reads a user-provided markdown shipments table and may recommend cloud browser-use for pages that cannot be checked through direct HTTP.]

## Skill Version(s):

1.1.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
