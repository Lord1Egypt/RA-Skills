## Description: <br>
Rice-tracker helps manage rice customer inventory, purchase batches, consumption tracking, receivables, payment status, and reconciliation reminders. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[swiftuis](https://clawhub.ai/user/swiftuis) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users such as rice sellers, group-buy organizers, and household managers use this skill to track customer stock, purchases, receivables, and month-end reconciliation reminders. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The local web server can expose customer inventory and payment records on the local network without login protection. <br>
Mitigation: Run only on a trusted machine and network, bind the server to 127.0.0.1, or add authentication before entering real customer data. <br>
Risk: Local JSON records and logs may contain customer and receivables information. <br>
Mitigation: Protect the records file and logs with appropriate local file permissions and avoid storing unnecessary sensitive data. <br>
Risk: The bundled start and stop scripts manage processes by port 5001 and may affect unrelated services using that port. <br>
Mitigation: Inspect the scripts before use and confirm no unrelated service is bound to port 5001. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/swiftuis/rice-tracker) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/swiftuis) <br>
- [Clawdis homepage](https://clawhub.com/skills/rice-tracker) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and text responses with JSON records and shell commands for local operation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local inventory, purchase, payment, reconciliation, and reminder outputs for a Flask-based tracker.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
