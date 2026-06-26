## Description: <br>
Analyze a bank or card CSV export to surface forgotten, unused, or redundant subscriptions, categorize them into cancel, review, and keep tiers, estimate annual spend, and output a markdown action table. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zepoldani](https://clawhub.ai/user/zepoldani) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to audit pasted transaction CSVs or manual subscription lists for recurring charges, estimated annual spend, cancellation candidates, review items, and unknown charges that need confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pasted bank or card transaction data can contain sensitive financial information. <br>
Mitigation: Redact unnecessary fields, use the manual-list option when sufficient, and review the privacy and retention terms of the configured AI provider before processing. <br>
Risk: Transaction analysis may pass through the user's configured AI provider. <br>
Mitigation: Use a fully local provider such as Ollama when offline processing or stricter data handling is required. <br>
Risk: The companion Gumroad tracker is an external paid resource. <br>
Mitigation: Evaluate the tracker separately before purchasing it or uploading financial data to it. <br>
Risk: Unknown or mangled merchant strings may be misidentified. <br>
Mitigation: Flag uncertain merchants for user confirmation and avoid presenting inferred identities as fact unless confidence is high. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/zepoldani/subscription-audit) <br>
- [Publisher profile](https://clawhub.ai/user/zepoldani) <br>
- [Subscription Audit Tracker](https://zepoldani.gumroad.com/l/huqic) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Guidance] <br>
**Output Format:** [Markdown summary with an action table and savings summary] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Processes pasted transaction CSVs or manual subscription lists in the user's configured agent environment; no API keys or external integrations are required by the skill.] <br>

## Skill Version(s): <br>
1.0.1 (source: server evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
