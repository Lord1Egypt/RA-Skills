## Description: <br>
Assisted Rappi ordering through a local openclaw-rappi service that drafts carts, summarizes checkout details, requests explicit approval, and submits purchases only after exact current-chat approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zarruk](https://clawhub.ai/user/zarruk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agents use this skill to assemble Rappi orders for food, groceries, pharmacy, convenience, and household items, then present cart or checkout details for human review. It is intended to keep final purchase submission gated by exact per-order approval in the current chat. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can bootstrap and run an unpinned external local service with access to a logged-in Rappi browser profile. <br>
Mitigation: Install only if the publisher and local service are trusted, review the service before use, use a dedicated visible browser profile, and keep separate stop or uninstall instructions available. <br>
Risk: The skill can prepare and submit purchases after approval. <br>
Mitigation: Review the checkout summary carefully, use the exact approval phrase only for orders intended for payment, and stop if checkout details differ from the approved summary. <br>
Risk: Ordering workflows may expose sensitive account, address, payment, verification, or restricted-item screens. <br>
Mitigation: Require manual intervention for login, captcha, 2FA, age verification, prescription medication, payment changes, address changes, identity validation, or other sensitive screens. <br>


## Reference(s): <br>
- [Openclaw Rappi on ClawHub](https://clawhub.ai/zarruk/rappi-ordering) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash, JSON, and HTTP API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires exact current-chat approval text before final purchase submission.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
