## Description: <br>
This skill helps agents identify likely plant leaf diseases from images or videos, returning lesion descriptions, confidence scores, severity, and general prevention guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Home gardeners, greenhouse operators, plant factories, and farm inspectors can use this skill to analyze leaf images or videos for likely disease type, symptom features, confidence, severity, and broad next-step guidance. It can also retrieve cloud-backed historical plant disease reports for the same user identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review says the skill sends plant images or videos and an identifier such as a username, phone number, or open-id to the publisher's cloud service. <br>
Mitigation: Install only when that data sharing is acceptable, avoid sensitive identifiers where possible, and review account and token handling before use. <br>
Risk: The security review reports under-disclosed account creation, token storage, history access, and generic or video health-analysis plumbing. <br>
Mitigation: Treat reports and history as cloud-backed account activity and review the publisher's documentation and returned outputs before relying on them. <br>
Risk: Visual plant disease identification can be uncertain when symptoms overlap or images are low quality. <br>
Mitigation: Use clear close-up leaf images, treat results as diagnostic support, and consult a plant health professional before taking high-impact treatment actions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-plant-leaf-disease-identification-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [API reference](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, guidance] <br>
**Output Format:** [Markdown reports, JSON responses, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May require an open-id and sends plant images or videos plus an identifier to the publisher's cloud service; history queries are cloud-backed.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
