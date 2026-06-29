## Description: <br>
AI-powered flowering-date prediction for ornamental and cut-flower plants using bud-stage images or videos, optional temperature and light data, and a phenology model to estimate full-bloom timing for production planning. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External growers, greenhouse operators, botanical gardens, and tourism park teams use this agent to analyze flower-bud media and estimate the likely full-bloom date within the next 3-7 days. The output supports scheduling decisions for pollination, harvesting, and visitor planning while remaining advisory. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant media and supplied URLs are processed by a cloud service. <br>
Mitigation: Use only media that may be shared with the service provider, and confirm the receiving service and data-retention expectations before deployment. <br>
Risk: The skill silently creates or reuses a local identity and stores service tokens. <br>
Mitigation: Review identity and token storage behavior before installation, restrict local file access where possible, and define a token revocation or deletion process. <br>
Risk: The artifact contains pet and video-analysis remnants in a flowering-date skill. <br>
Mitigation: Have the publisher clarify the remaining references and verify that the deployed behavior matches the flowering-date use case. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-flowering-date-prediction-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API documentation](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown or text report, with JSON available through the skill's detail mode and optional file output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include predicted flowering date, confidence, phenological stage, advisory notes, historical report tables, and report links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release metadata; artifact frontmatter reports 1.0.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
