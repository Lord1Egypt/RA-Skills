## Description: <br>
A shop health monitoring skill for cross-border e-commerce stores that checks site availability, response time, SSL certificate health, key page 404s, missing content, and sends Feishu alerts when issues are found. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zzhimin](https://clawhub.ai/user/zzhimin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and developers use this skill to run periodic health checks across configured e-commerce shops, inspect availability, SSL, and sampled product-page problems, and receive operational alerts through Feishu. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends HTTP requests to configured store domains and sampled product pages. <br>
Mitigation: Install and run it only for shops the user is authorized to monitor, and review the shop configuration before scheduling checks. <br>
Risk: Feishu webhook values and report details may expose operational information outside the local environment. <br>
Mitigation: Treat the webhook as a secret, prefer environment or protected configuration storage, and use the no-Feishu option when reports should remain local. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zzhimin/shop-health-check) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions, shell commands, console text reports, optional JSON report data, and Feishu message cards.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires configured shop domains, paths, thresholds, Python dependencies, and an optional Feishu webhook.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
