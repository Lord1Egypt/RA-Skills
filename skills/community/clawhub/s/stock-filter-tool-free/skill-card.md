## Description: <br>
Helps individual investors screen A-share stocks with fundamental, technical, industry, and market-cap filters using public market data. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External individual investors and analysts use this skill to configure simple A-share stock screens, compare public market data, and review candidate results before doing their own investment analysis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may run Python commands and call external public market-data services. <br>
Mitigation: Review proposed commands before execution and run the skill in an environment where network access and Python dependencies are intentionally allowed. <br>
Risk: The artifact describes conflicting export behavior for the free edition. <br>
Mitigation: Treat the release as terminal-display only unless the publisher clarifies that file export is supported. <br>
Risk: Broad activation wording may cause the skill to be used for unrelated data-analysis tasks. <br>
Mitigation: Use it only for stock-screening workflows and avoid routing unrelated analytics or reporting requests to this skill. <br>
Risk: Screening results can be delayed, incomplete, or misleading if treated as investment advice. <br>
Mitigation: Require human review of candidates and use the output as informational screening support, not as an investment recommendation. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/stock-filter-tool-free) <br>
- [Publisher profile](https://clawhub.ai/user/thcjp) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell-command examples and terminal stock-screening results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Free edition is described as terminal-display only; results should be manually reviewed and are not investment advice.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
