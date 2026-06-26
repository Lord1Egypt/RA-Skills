## Description: <br>
Analyzes fixed-angle indoor plant leaf image sequences or video to detect aging indicators and predict a 3-7 day leaf-fall risk window. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, plant-care operators, and developers use this skill to submit indoor houseplant leaf images or videos for cloud analysis, daily aging reports, predicted leaf-fall windows, and directional care suggestions. It can also list prior cloud-stored analysis reports for a supplied open-id. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Plant-camera media, URLs, user identifiers, and report history are sent to or retrieved from a third-party cloud service. <br>
Mitigation: Use the skill only with media and identifiers suitable for third-party processing, and confirm the publisher's retention, deletion, and access-control practices before submitting sensitive footage. <br>
Risk: The release guidance warns against reusing an API key as the open-id user identifier. <br>
Mitigation: Provide a non-secret username, phone number, or other non-secret identifier as open-id, and keep API keys separate from identity fields. <br>
Risk: The authoritative scan verdict is suspicious because account, token, history, and upload behavior are broad and under-disclosed. <br>
Mitigation: Review the publisher documentation and local configuration before deployment, restrict credentials to the minimum needed, and avoid installing where this data flow is unacceptable. <br>


## Reference(s): <br>
- [ClawHub skill listing](https://clawhub.ai/18072937735/smyx-leaf-aging-fall-prediction-analysis) <br>
- [API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown or JSON-like text with structured leaf-aging results, report links, shell command examples, and optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Results may include an aging index, predicted fall window, at-risk leaf locations, likely cause hints, care suggestions, and cloud report export URLs.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence; artifact frontmatter says 1.0.1) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
