## Description: <br>
ZDAT zero-defect intelligence crawling skill for keyword monitoring, multi-platform intelligence collection, automatic archiving, classification, and negative-sentiment alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[freemanyg](https://clawhub.ai/user/freemanyg) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams use this skill to run scheduled zero-defect topic monitoring, classify collected public intelligence, archive relevant findings, and check negative-keyword alert thresholds. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Scheduled monitoring and alerting can collect or redistribute public information that may not fit an organization's data handling policy. <br>
Mitigation: Define keyword lists, crawl sources, output files, recipients, thresholds, and retention expectations before enabling cron jobs or enterprise WeChat alerts. <br>
Risk: The artifact describes integrations for search, crawling, archiving, Excel output, and WeChat alerts, while the bundled scripts still contain TODO placeholders for several live behaviors. <br>
Mitigation: Review and test the configured integrations before relying on production crawl, archive, or alert results. <br>


## Reference(s): <br>
- [ZDAT Crawl Skill on ClawHub](https://clawhub.ai/freemanyg/zdat-crawl-skill) <br>
- [freemanyg publisher profile](https://clawhub.ai/user/freemanyg) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and terminal status summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local YAML keyword and schedule configuration; scripts currently print crawl and alert status and include TODO placeholders for live search, archive, and alert integrations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
