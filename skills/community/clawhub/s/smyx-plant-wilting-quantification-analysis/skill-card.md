## Description: <br>
Analyzes full-plant images or videos to quantify wilting severity, estimate droop and turgidity indicators, distinguish likely underwatering from overwatering when moisture context is available, and return intervention direction without specific watering amounts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, plant-care operators, greenhouse teams, and smart-pot workflows use this skill to analyze plant media, quantify wilting severity, and decide whether the likely intervention direction is watering, drainage, ventilation, or observation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant photos or videos and an open-id, username, or phone-number-like identifier may be sent to the Life Emergence backend. <br>
Mitigation: Use only non-sensitive plant media, avoid people, private interiors, and location-revealing details, and run the skill only when that data sharing is acceptable. <br>
Risk: The skill may create or log into a backend account and persist returned tokens locally for later requests. <br>
Mitigation: Install only if the publisher and backend are trusted; use a dedicated identifier where possible and review local configuration or token storage after use. <br>
Risk: Wilting-cause analysis can be uncertain without soil-moisture context and may confuse underwatering with overwatering. <br>
Mitigation: Treat the result as advisory, confirm soil moisture and visible plant conditions before acting, and avoid relying on the skill for exact watering amounts. <br>


## Reference(s): <br>
- [Plant Wilting Quantification API Documentation](artifact/references/api_doc.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-plant-wilting-quantification-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Structured text, JSON responses, and Markdown tables for historical report lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can save results to a local output file and may include links to backend-hosted report exports.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; source frontmatter reports 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
