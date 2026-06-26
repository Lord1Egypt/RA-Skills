## Description: <br>
Automatically distributes products from the Kuairui premium product catalog to the Ozon e-commerce platform. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[famechyu](https://clawhub.ai/user/famechyu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External marketplace operators use this skill to collect category, store, and price-range inputs, then run browser automation that synchronizes selected products to Ozon. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a fixed remote service and embedded account credentials. <br>
Mitigation: Install and run it only when the publisher, remote service, and account are trusted; prefer a test store and replace shared credentials before production use. <br>
Risk: The automation can submit a live product distribution action. <br>
Mitigation: Require manual confirmation of the category, store, price range, affected products, and target marketplace before any send or publish action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/famechyu/test-publish-dev1) <br>
- [Automation target service](http://139.9.192.16:9089/) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Files] <br>
**Output Format:** [Task status text with script execution output and a screenshot file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires category, store, and price-range values before execution.] <br>

## Skill Version(s): <br>
1.1.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
