## Description: <br>
Tracks RedNote/Xiaohongshu account follower-growth rankings across daily, weekly, and monthly views, with options to generate ranking images, export data, and configure recurring deliveries. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuanyi-github](https://clawhub.ai/user/yuanyi-github) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, brand teams, MCNs, and content creators use this skill to monitor RedNote/Xiaohongshu follower-growth trends, create shareable ranking visuals, export ranking data, and receive scheduled ranking reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can store contact details for subscriptions and send recurring reports through configured email or WeChat services. <br>
Mitigation: Only enable subscriptions after reviewing local storage behavior, use limited delivery credentials, and avoid including sensitive contact details or report content. <br>
Risk: Fetched ranking data may be tamperable because the security evidence reports unsafe HTTPS settings. <br>
Mitigation: Treat ranking data as untrusted, verify important results before business use, and run the skill in a constrained environment. <br>
Risk: The skill can write report outputs to local locations, including user-selected or synced directories. <br>
Mitigation: Choose non-sensitive output paths and review generated files before sharing or syncing them. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/yuanyi-github/rednote-ranking) <br>
- [Publisher profile](https://clawhub.ai/user/yuanyi-github) <br>
- [Subscription tiers reference](references/subscription_tiers.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with command examples; generated JSON, Excel, and image files from scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can produce local files for ranking images, data exports, and subscription configuration.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
