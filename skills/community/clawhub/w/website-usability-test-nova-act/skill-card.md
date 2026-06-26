## Description: <br>
AI-orchestrated usability testing using Amazon Nova Act that generates personas, runs browser-based workflow tests, interprets results, and produces HTML usability reports with safety guardrails. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adityak6798](https://clawhub.ai/user/adityak6798) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, QA teams, and product teams use this skill to test website usability with persona-based browser automation, especially for checkout, booking, posting, signup, and other end-to-end user journeys. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Live browser automation can affect carts, sessions, forms, checkout, booking, or posting flows. <br>
Mitigation: Run against staging or test sites with disposable accounts and synthetic data, and stop before final material-impact actions. <br>
Risk: Trace files and reports can capture screenshots, page content, PII, and other sensitive data from tested pages. <br>
Mitigation: Avoid private or production data where possible, review generated files before sharing, and delete local traces when they contain sensitive content. <br>
Risk: Auto-persona mode may send page-derived metadata to Anthropic when ANTHROPIC_API_KEY is available. <br>
Mitigation: Use explicit personas or disable that mode unless sending page-derived metadata to Anthropic is acceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/adityak6798/website-usability-test-nova-act) <br>
- [Nova Act cookbook](references/nova-act-cookbook.md) <br>
- [Persona examples](references/persona-examples.md) <br>
- [AWS Console for Nova Act API key](https://console.aws.amazon.com/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, HTML, JSON] <br>
**Output Format:** [Markdown guidance with shell commands plus generated JSON test results, HTML reports, and Nova Act trace files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local files such as nova_act_logs/, test_results_adaptive.json, and nova_act_usability_report.html when tests run.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata; artifact frontmatter and manifest report 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
