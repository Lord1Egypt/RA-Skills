## Description: <br>
Secure Xianyu Guanjia API client with endpoint allowlisting, enforced confirmation for high-risk actions, dry-run mode, and unsafe methods for automation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[crab-xieyujin](https://clawhub.ai/user/crab-xieyujin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation agents use this skill to call the Xianyu Guanjia Open Platform for shop, product, order, category, logistics, and location workflows while retaining endpoint allowlisting, dry-run previews, and confirmation prompts for account-changing actions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make account-changing product, order price, shelf-status, and logistics API calls on a Xianyu shop. <br>
Mitigation: Install it only for Xianyu shop automation, use least-privilege dedicated credentials, and prefer the confirmed methods with dry-run review before execution. <br>
Risk: Explicit _unsafe methods can skip interactive confirmation in automation workflows. <br>
Mitigation: Allow _unsafe methods only in controlled and audited automation after the exact request payload has been reviewed with dry_run=True. <br>
Risk: Xianyu API credentials are required and could grant access to marketplace operations if exposed. <br>
Mitigation: Store credentials in environment variables or a secret manager, avoid hardcoding them, rotate them periodically, and revoke them when the skill is no longer trusted. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/crab-xieyujin/xianyu-api-client-skill) <br>
- [Xianyu Guanjia Open Platform](https://www.goofish.pro) <br>
- [OpenClaw source metadata](https://clawhub.com/skills/xianyu-api-client) <br>


## Skill Output: <br>
**Output Type(s):** [Code, API Calls, Configuration, Guidance] <br>
**Output Format:** [Python client methods, JSON API responses, and Markdown setup guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires XIAN_YU_APP_KEY, XIAN_YU_APP_SECRET, and Python; supports dry-run previews and confirmation-gated write operations.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
