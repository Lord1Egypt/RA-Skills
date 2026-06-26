## Description: <br>
Automate login and page capture for WHUT AI Augmented sites using agent-browser. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[dongxingao](https://clawhub.ai/user/dongxingao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users working with WHUT AI Augmented pages use this skill to open authenticated pages, handle login prompts, and capture page text and questions for later review. The skill requires user-provided WHUT credentials and should be used only on intended WHUT URLs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can use stored WHUT credentials on an arbitrary supplied URL. <br>
Mitigation: Verify the target URL before execution and provide credentials only through environment variables or a local secret file for the intended WHUT site. <br>
Risk: The workflow can submit answers or forms without a clear approval step. <br>
Mitigation: Require explicit user approval before allowing the agent to submit answers, forms, or other page changes. <br>
Risk: latest_page_dump.json can contain private coursework, prompts, account data, or other sensitive page text. <br>
Mitigation: Review and delete latest_page_dump.json after use when it contains sensitive information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/dongxingao/ya) <br>
- [Workflow conventions](references/workflow.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance, shell command invocations, and JSON page dumps written to latest_page_dump.json] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses agent-browser to open the target page, fills login fields from configured credentials, and captures page URL, text, extracted questions, timestamp, and status.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
