## Description: <br>
Helps POD sellers build or optimize print-on-demand businesses with AI-assisted strategy, tool selection, product listing, design, customer-service, and sales recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[wangm-a3](https://clawhub.ai/user/wangm-a3) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External POD sellers and e-commerce operators use this skill to plan AI-assisted print-on-demand workflows, compare tools, score product categories, select platform strategies, and prepare operational guidance before human-approved execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires TRADEGPT_API_KEY and may use an external strategy API. <br>
Mitigation: Store the token securely, rotate it when needed, and avoid placing it in logs, prompts, source files, or shared outputs. <br>
Risk: POD strategy details sent to the external API could include sensitive business information. <br>
Mitigation: Share only the minimum category and operating context needed for strategy generation, and do not send customer data, store credentials, sales exports, or platform secrets. <br>
Risk: Generated recommendations may touch high-impact store actions such as refunds, address changes, bulk listings, pricing, or promotions. <br>
Mitigation: Require human review and explicit approval before applying recommendations in commerce platforms or customer-service systems. <br>
Risk: AI-generated POD designs and tool recommendations can still create copyright, trademark, likeness, or platform-policy exposure. <br>
Mitigation: Perform manual IP checks, image reverse searches, trademark checks, font-license review, and platform-policy review before publishing designs. <br>


## Reference(s): <br>
- [YunlvAI Homepage](https://yunlvai.com) <br>
- [YunlvAI TradeGPT API](https://api.yunlvai.com) <br>
- [ClawHub Release Page](https://clawhub.ai/wangm-a3/yunlv-pod-agent) <br>
- [POD AI Tool Comparison](references/pod_tool_comparison.md) <br>
- [POD Design Safety Formula](references/pod_design_formula.md) <br>
- [POD Store Operations Checklist](references/pod_operations_checklist.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and JSON from the bundled CLI analyzer] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TRADEGPT_API_KEY for external strategy API use; bundled analyzer commands print structured JSON.] <br>

## Skill Version(s): <br>
1.1.0 (source: ClawHub release evidence and clawhub.yaml) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
