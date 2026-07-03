## Description: <br>
This skill analyzes ornamental fish images or videos to estimate body color saturation, brightness, vibrancy score, trends, and husbandry-oriented recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to assess ornamental fish color brightness from aquarium camera or uploaded media and generate structured color health reports with vibrancy scores, HSV measurements, trends, and recommended next steps. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium images or videos and identity-linked requests may be sent to the publisher's remote services. <br>
Mitigation: Use the skill only with media appropriate for remote processing, and review service endpoints and data handling before private camera feed use. <br>
Risk: The skill may silently create or reuse an identity and store account tokens locally. <br>
Mitigation: Review or disable automatic identity creation and local token storage before deployment in shared or sensitive environments. <br>
Risk: Arbitrary URL input can cause remote media retrieval through the publisher service. <br>
Mitigation: Restrict accepted URLs to trusted sources and avoid submitting sensitive internal or private media links. <br>


## Reference(s): <br>
- [API documentation](artifact/references/api_doc.md) <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-fish-color-brightness-assessment-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON or structured report output from the skill scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports may include vibrancy_score_0_100, HSV statistics, species baseline comparison, trend fields, recommended actions, and report links.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
