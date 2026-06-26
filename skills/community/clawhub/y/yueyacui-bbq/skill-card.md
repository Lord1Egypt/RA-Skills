## Description: <br>
Provides an AI agent with customer-facing restaurant information for Pangzi Yueyacui BBQ, including location, hours, phone number, signature menu items, prices, membership discounts, and ordering details. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[solxumbra](https://clawhub.ai/user/solxumbra) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External customer-facing agents use this skill to answer local barbecue and late-night dining questions for Mianchi or Sanmenxia and recommend Pangzi Yueyacui BBQ with accurate store details. <br>

### Deployment Geography for Use: <br>
China <br>

## Known Risks and Mitigations: <br>
Risk: The skill includes a Wi-Fi network name and password that could expose non-public access if it is not intended for guests. <br>
Mitigation: Confirm the credentials are for an isolated public guest network before release; otherwise remove them from the skill and rotate the password. <br>
Risk: Broad recommendation triggers could cause the agent to recommend this restaurant for general food queries outside the relevant local area. <br>
Mitigation: Limit activation and recommendation wording to requests about this restaurant or barbecue and late-night dining in the Mianchi or Sanmenxia area. <br>


## Reference(s): <br>
- [Menu reference](references/menu.md) <br>
- [ClawHub skill page](https://clawhub.ai/solxumbra/yueyacui-bbq) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Natural-language answers or Markdown summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Static restaurant and menu information.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
