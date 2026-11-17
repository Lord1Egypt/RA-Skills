## Description:

Use this skill when the user wants to poll gym venue availability, inspect or modify the `venue_polling.py` order-signing flow, or run the bundled signature replay and public-key verification helpers for the mini-program booking APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ruokkkkk](https://clawhub.ai/user/ruokkkkk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and operators use this skill to inspect, run, or modify a gym venue availability polling workflow and debug RSA-signed booking requests for mini-program APIs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled polling workflow includes a live-looking token-user credential.

Mitigation: Remove or rotate the exposed token before use and load credentials from the user's environment instead of hardcoding them.

Risk: The bundled polling script can automatically submit a booking order.

Mitigation: Disable automatic booking by default and require explicit user confirmation before calling createOrder.

Risk: Implicit invocation could run booking-related tooling outside an intended venue-booking task.

Mitigation: Limit invocation to explicit venue-booking, polling, or signature-debugging requests.

## Reference(s):

- [Create Order Analysis](references/create-order-analysis.md)
- [Captured createOrder request](references/captured-create-order.txt)
- [Captured listAreaLease request](references/captured-list-area-lease.txt)
- [ClawHub skill page](https://clawhub.ai/ruokkkkk/skills/venue-polling)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with code and shell command snippets when needed]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May inspect or modify bundled Python scripts and local configuration for venue polling, booking signatures, and replay checks.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
