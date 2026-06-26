## Description: <br>
AI-powered plant root health analysis from transparent pots or smart seedling boxes that analyzes root images or videos, identifies visual root-health indicators, and returns a health score, vitality grade, and care-direction guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and plant-care operators use this skill to analyze transparent-pot, seedling-box, plant-factory, or hydroponic root media for visible signs of root health, rot risk, and care adjustments. It can also query cloud-stored historical root-health reports for an open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Uploaded plant images, videos, or media URLs may be sent to remote services and associated with an open-id. <br>
Mitigation: Review the publisher's data handling before installation, avoid sensitive media, and use a non-sensitive identifier instead of a phone number. <br>
Risk: The security evidence reports under-disclosed identity, account, token, history, and mismatched analysis components. <br>
Mitigation: Review the publisher and bundled behavior before execution, and remove or disable unrelated account, payment, camera-management, and history capabilities before production use. <br>
Risk: The security guidance calls for removal and rotation of an embedded API key. <br>
Mitigation: Require the publisher to remove the embedded key, rotate any exposed credential, and document account creation, retention, and deletion behavior. <br>


## Reference(s): <br>
- [API interface documentation](references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-root-health-transparent-pot-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration guidance] <br>
**Output Format:** [Markdown or JSON report text; history queries render Markdown tables with report links.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts a local image/video path or public media URL plus an open-id; results may also be saved to an output file.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
