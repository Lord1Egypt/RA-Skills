## Description: <br>
Checks Taobao and Tmall product prices from product URLs and returns current product price details, while the release also describes monitoring, history, alert, and comparison workflows. <br>

This skill is for research and development only. <br>

## Publisher: <br>
[275254cl-hash](https://clawhub.ai/user/275254cl-hash) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External shoppers, purchasing agents, and e-commerce operators can use this skill to query Taobao/Tmall product price information and plan price-tracking workflows. Reviewers should treat it as a basic price-query script unless the missing monitoring, history, alert, comparison, export, and API components are supplied. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for persistent Taobao cookie use. <br>
Mitigation: Avoid using a primary Taobao account cookie; if a cookie is required, use a low-risk account and remove or rotate the cookie after use. <br>
Risk: The release advertises monitoring, alerts, history, comparison, export, API, and cron workflows that are not fully present in the artifact. <br>
Mitigation: Treat the artifact as a simple price-query script until the missing components are provided and reviewed. <br>
Risk: Scheduled monitoring or local API exposure can create ongoing access to account-linked shopping data. <br>
Mitigation: Do not enable cron jobs or expose a local API unless the deployment model, stored credentials, and access controls have been reviewed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/275254cl-hash/taobao-price-monitor) <br>


## Skill Output: <br>
**Output Type(s):** [Text, JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON examples; query_price.py returns JSON.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and requests; optionally uses TAOBAO_COOKIE and performs network requests to Taobao/Tmall endpoints.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter; artifact changelog lists v0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
