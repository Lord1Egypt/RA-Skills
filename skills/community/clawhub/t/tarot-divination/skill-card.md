## Description: <br>
塔罗牌占卜是一项付费每日抽牌服务，会从78张塔罗牌中随机抽取一张并提供牌意解读与行动指引。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guoshuai1](https://clawhub.ai/user/guoshuai1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill for paid daily tarot readings and lightweight reflective guidance. Operators configure payment recipient and encryption settings before creating orders and serving results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Payment configuration and local storage are under-scoped and partly inconsistent. <br>
Mitigation: Confirm the config file path, clawtip amount, and payment recipient manually before creating or paying an order. <br>
Risk: Questions, orders, payment metadata, and readings may be retained in local files or a local database. <br>
Mitigation: Avoid highly sensitive personal questions unless local retention is acceptable, and delete local order/database files when history should not be kept. <br>
Risk: The server security verdict is suspicious for this paid release. <br>
Mitigation: Review the skill before installation or payment and run it only in an environment where local file writes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/guoshuai1/tarot-divination) <br>
- [Publisher profile](https://clawhub.ai/user/guoshuai1) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and terminal text with order identifiers, payment status messages, and tarot reading text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local order JSON and SQLite fulfillment records when the scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
