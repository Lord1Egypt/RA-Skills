## Description: <br>
Selection Agent helps agents perform product research across keyword research, SEO analysis, competitor analysis, and TrendPlus data workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lygjoey](https://clawhub.ai/user/lygjoey) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to trigger structured product-selection research, including keyword metrics, competitor comparisons, deduplication checks, and priority scoring. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill relies on connected services and broad credential use. <br>
Mitigation: Review the referenced configuration before use, remove hard-coded tokens, and provide credentials through a secret manager or explicitly named environment variables. <br>
Risk: The quick-start command may send data to or write data through third-party services. <br>
Mitigation: Confirm which services and databases will be contacted before running the command, and run only in an environment approved for those data flows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lygjoey/selection-agent) <br>
- [Project repository listed by the skill](https://github.com/Arxchibobo/powerful-trendplus) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and structured JSON output examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces research workflow instructions and a fixed keyword-analysis JSON structure.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
