## Description: <br>
Predicts near-term full-bloom dates for ornamental and cut-flower plants from bud images or videos, optional temperature and light data, and cloud API analysis. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External growers, greenhouse operators, botanical gardens, tourism-park teams, and developers use this skill to analyze plant bud media and optional environmental data for flowering-date predictions and historical report lookup. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Cloud processing of plant media, media URLs, and a persistent user identifier may expose sensitive greenhouse footage or identifying data. <br>
Mitigation: Use only non-sensitive plant media, avoid footage containing people or private facilities, and review the publisher's retention and authorization controls before deployment. <br>
Risk: Security evidence reports mismatched pet/human-health materials, broad cloud API access, local token storage, and an embedded API key. <br>
Mitigation: Review carefully before installing; require the publisher to remove mismatched materials, rotate embedded credentials, narrow the API surface, and document credential handling. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/18072937735/smyx-flowering-date-prediction-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Common analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, JSON API results, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [History queries may return Markdown tables with report links; prediction results include estimated dates and confidence.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter states 1.0.2) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
