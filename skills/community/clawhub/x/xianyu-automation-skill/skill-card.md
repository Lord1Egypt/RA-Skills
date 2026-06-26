## Description: <br>
Enterprise-grade automated operations for Xianyu stores with full lifecycle management, confirmation safeguards, and intelligent decision engine. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crab-xieyujin](https://clawhub.ai/user/crab-xieyujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and agents use this skill to manage Xianyu listings, pricing, order workflows, and daily operation plans through automated workflows with confirmations for higher-impact actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks for sensitive Xianyu store authority. <br>
Mitigation: Use a dedicated low-permission Xianyu application key, keep credentials in environment variables or a secret manager, and revoke keys when the skill is no longer trusted. <br>
Risk: Advertised automation safety caps are not clearly enforced in the provided code. <br>
Mitigation: Keep semi-automatic mode enabled, require confirmation for listing, order, price, and shipping writes, and verify dependent skills before deployment. <br>
Risk: Automated listing, pricing, or order actions can affect store performance and compliance. <br>
Mitigation: Start with dry-run or semi-automatic workflows, monitor operation logs for anomalies, and review platform-rule compliance before enabling broader automation. <br>


## Reference(s): <br>
- [Goofish/Xianyu homepage](https://www.goofish.pro) <br>
- [ClawHub skill page](https://clawhub.ai/crab-xieyujin/xianyu-automation-skill) <br>
- [ClawHub source listing](https://clawhub.com/skills/xianyu-automation) <br>


## Skill Output: <br>
**Output Type(s):** [code, API calls, configuration, guidance] <br>
**Output Format:** [Python code, structured result dictionaries, and Markdown guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XIAN_YU_APP_KEY and XIAN_YU_APP_SECRET plus Python and dependent Xianyu skills.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
