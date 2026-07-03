## Description: <br>
Analyzes plant root images or videos from transparent pots and smart seedling boxes to report visual root health indicators, a 0-100 health score, a vitality grade, care guidance, and report links. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to analyze root imagery from transparent pots, smart seedling boxes, plant factories, and hydroponic systems. It helps identify visual signs such as root tip color, root hair density, branching structure, and possible root rot so users can adjust care practices. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security scan reports that plant images or videos may be sent to a cloud service. <br>
Mitigation: Use only with media that is acceptable to share with the publisher's cloud service, and avoid sensitive greenhouse, home, or business footage unless consent and retention expectations are clear. <br>
Risk: The security scan reports persistent identities and locally stored tokens used for account-linked history queries. <br>
Mitigation: Review identity and token handling before deployment, and limit use to environments where account-linked report history is acceptable. <br>
Risk: The skill returns visual plant-health assessments that may be incomplete or misleading for severe root disease. <br>
Mitigation: Treat results as care guidance rather than a definitive diagnosis, and seek professional agronomy support for serious root rot or crop-impacting findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-root-health-transparent-pot-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON analysis results, including report links and Markdown tables for history queries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Supports local image/video files, remote media URLs, configurable detail level, optional output files, and cloud-backed history report queries.] <br>

## Skill Version(s): <br>
1.0.3 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
