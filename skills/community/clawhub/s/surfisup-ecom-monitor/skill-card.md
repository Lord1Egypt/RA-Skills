## Description: <br>
Provides daily Shopify sales summaries, low-stock alerts, and competitor price tracking using a user-provided Shopify API key. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jamod](https://clawhub.ai/user/jamod) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Store operators and developers can use this skill to have an agent summarize Shopify sales, flag low inventory, and monitor competitor prices. The skill requires a user-provided Shopify API key and explicit alert destinations for email or Telegram notifications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill handles sensitive Shopify store data and may send sales or inventory information to outbound alert channels. <br>
Mitigation: Use a read-only, least-privilege Shopify API key and approve exact email or Telegram recipients before enabling alerts. <br>
Risk: The artifact gives contradictory signals about scheduled automation and persistence. <br>
Mitigation: Do not allow any cron or scheduled job unless the skill shows the schedule, the data sent, and clear removal steps. <br>
Risk: The authoritative security verdict is suspicious. <br>
Mitigation: Review the skill before installing and confirm that store access, alert destinations, and scheduling behavior match the intended use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jamod/surfisup-ecom-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/jamod) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with alert text, configuration details, and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference Shopify API access, email or Telegram recipients, and scheduling details.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
