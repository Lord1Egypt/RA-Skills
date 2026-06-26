## Description: <br>
Automated sports science intelligence engine that fetches 55+ sources across PubMed, expert blogs, and wearable technology news, filters noise, translates content, and syncs reports to Feishu or Notion. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[w2478328197-arch](https://clawhub.ai/user/w2478328197-arch) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and sports science practitioners use this skill to run a daily intelligence workflow that gathers public research and industry updates, filters and translates them, and publishes a consolidated report to configured destinations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated reports can be published to Feishu or Notion destinations using configured credentials. <br>
Mitigation: Use limited-scope Feishu and Notion credentials, verify recipient IDs before running, and review generated reports before relying on them. <br>
Risk: Fetched public content may be sent through external services such as Google Translate and platform APIs. <br>
Mitigation: Run the skill only for public research and news content, and confirm that external API use matches the deployment environment's data-handling requirements. <br>
Risk: The skill instructs the agent to run a Python command from the referenced external project. <br>
Mitigation: Review the external project code and dependency requirements before execution. <br>


## Reference(s): <br>
- [Project homepage](https://github.com/w2478328197-arch/sports-science-daily) <br>
- [ClawHub skill page](https://clawhub.ai/w2478328197-arch/sport-science-review) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Configuration] <br>
**Output Format:** [Markdown report with optional Feishu cloud document, Feishu notification card, and Notion page sync] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses CLI options for lookback period, history handling, source selection, and output language; updates local deduplication history.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
