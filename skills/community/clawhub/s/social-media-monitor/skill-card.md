## Description: <br>
Social Media Monitor analyzes local social media CSV data for keyword monitoring, negative-sentiment alerts, volume trends, sentiment analysis, keyword extraction, and weekly Markdown reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Crystaria](https://clawhub.ai/user/Crystaria) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Brand, ecommerce, and operations users use this skill to review local exported social media CSVs, track monitored keywords, check negative-sentiment alerts, and generate weekly monitoring reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores monitoring keywords, alert settings, CSV-derived results, and generated Markdown reports in the local skill directory. <br>
Mitigation: Use data that is appropriate for local persistence, restrict access to the skill directory, and remove or back up generated reports according to the user's retention policy. <br>
Risk: Dictionary-based sentiment analysis can miss context or misclassify important posts. <br>
Mitigation: Treat alerts and sentiment labels as screening signals and manually review important or high-impact findings before acting on them. <br>
Risk: The skill depends on npm packages that may need reproducible dependency handling in controlled environments. <br>
Mitigation: Review the dependency lockfile and pin or mirror dependencies according to the deployment environment's software supply-chain policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Crystaria/social-media-monitor) <br>
- [Publisher profile](https://clawhub.ai/user/Crystaria) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [MCP tool responses as text-wrapped JSON, text charts, and Markdown report files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes monitoring keywords, alert settings, CSV-derived results, and generated reports locally in the skill directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
