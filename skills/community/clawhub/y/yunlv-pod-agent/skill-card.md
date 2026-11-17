## Description:

Helps users build or optimize a print-on-demand business with AI-assisted product listing, design, customer service, tool selection, and sales strategy guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangm-a3](https://clawhub.ai/user/wangm-a3)

### License/Terms of Use:

MIT-0

## Use Case:

External POD sellers, operators, and developers use this skill to select AI tools, plan store operations, assess product and platform fit, and produce practical recommendations for POD design, listing, and customer-service workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Store automation advice could be applied to refunds, address changes, listings, or customer data without adequate oversight.

Mitigation: Keep the skill in an advisory role unless automation is protected by customer verification, least-privilege permissions, audit logs, transaction limits, and human approval for nontrivial cases.

Risk: AI-generated POD designs may resemble protected IP, trademarks, celebrity likenesses, competitor artwork, or unlicensed fonts.

Mitigation: Require human review, image and trademark checks, commercial font and asset license verification, and platform policy review before publishing designs.

Risk: API keys and customer-service conversation data could expose sensitive business or customer information if mishandled.

Mitigation: Store API keys outside code and logs, use minimal permissions, rotate credentials regularly, and avoid sending store API keys, sales data, or customer information to external services.

## Reference(s):

- [POD Tool Comparison](references/pod_tool_comparison.md)
- [POD Design Safety Formula](references/pod_design_formula.md)
- [POD Store Operations Checklist](references/pod_operations_checklist.md)
- [Yunlv AI Homepage](https://yunlvai.com)
- [Yunlv AI TradeGPT API](https://api.yunlvai.com)
- [ClawHub Skill Page](https://clawhub.ai/wangm-a3/skills/yunlv-pod-agent)

## Skill Output:

**Output Type(s):** [guidance, markdown, code, shell commands, configuration]

**Output Format:** [Markdown guidance and JSON analysis from the included CLI script]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses TRADEGPT_API_KEY for Yunlv AI TradeGPT API access when strategy recommendations require the external service.]

## Skill Version(s):

1.1.0 (source: server release and clawhub.yaml)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
