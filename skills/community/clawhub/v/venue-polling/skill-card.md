## Description: <br>
Helps agents poll gym venue availability, inspect or modify the venue_polling.py order-signing flow, and run signature replay or public-key verification helpers for mini-program booking APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ruokkkkk](https://clawhub.ai/user/ruokkkkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation operators use this skill to inspect or modify a gym mini-program venue polling workflow, debug RSA request signatures, and test booking API behavior only when they intentionally configure and authorize it. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The bundled workflow can automatically place a live venue reservation using account credentials without a clear confirmation step. <br>
Mitigation: Review before installing or running, disable auto-booking by default, and add an explicit confirmation step before any createOrder request. <br>
Risk: The artifact includes embedded account tokens and captured request examples that may expose sensitive booking credentials. <br>
Mitigation: Remove or rotate embedded tokens, sanitize captured request examples, and use only credentials that the operator controls. <br>
Risk: The polling and signing scripts require local RSA private key material. <br>
Mitigation: Provide keys only from a controlled local environment, keep private keys out of published artifacts and logs, and verify signing behavior with the replay helpers before live use. <br>


## Reference(s): <br>
- [Venue Polling on ClawHub](https://clawhub.ai/ruokkkkk/venue-polling) <br>
- [Create Order Analysis](references/create-order-analysis.md) <br>
- [Captured List Area Lease Request](references/captured-list-area-lease.txt) <br>
- [Captured Create Order Request](references/captured-create-order.txt) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with code and shell command suggestions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May direct agents to edit bundled Python scripts and use local RSA key material only when intentionally provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
