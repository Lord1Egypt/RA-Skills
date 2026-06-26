## Description: <br>
Comprehensive SaaS billing system with subscriptions, usage-based billing, invoicing, Stripe payments, dunning, proration, and multi-platform payment integration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sunshine-del-ux](https://clawhub.ai/user/Sunshine-del-ux) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and SaaS operators use this skill to plan billing workflows for subscriptions, metered usage, invoicing, payment setup, failed-payment recovery, and plan changes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill advertises billing and payment operations but documents commands that call a missing billing.sh script with a Stripe key. <br>
Mitigation: Obtain and inspect the actual billing.sh implementation before execution, and test only with restricted or test payment credentials until the behavior is verified. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sunshine-del-ux/saas-billing-system) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with bash command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires independent review of the referenced billing implementation and payment-provider credentials before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
