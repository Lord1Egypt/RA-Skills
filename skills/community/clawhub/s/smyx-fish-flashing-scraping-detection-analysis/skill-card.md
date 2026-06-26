## Description: <br>
Analyzes fixed aquarium camera videos to detect fish flashing and scraping behavior, count abnormal contact frequency, and produce ectoparasite risk warnings with observation guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Aquarium owners, public aquarium operators, quarantine tank managers, and aquaculture teams use this skill to analyze fish behavior videos or report history for flashing and scraping signals. It helps agents return structured warning reports, friction metrics, alert levels, recommended observation steps, and disclaimers that AI vision is not a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium videos, remote video URLs, and user identifiers are sent to the Life Emergence cloud service, and report retention or deletion controls are not clearly disclosed in the evidence. <br>
Mitigation: Use a dedicated pseudonymous open-id where possible, avoid sensitive footage, and confirm retention, deletion, access control, and report sharing terms with the publisher before production use. <br>
Risk: The security review reports local token storage and insufficient clarity around account login or registration. <br>
Mitigation: Use low-privilege credentials, avoid using a phone number as the open-id when a pseudonymous identifier is acceptable, protect local configuration files, and rotate tokens if the workspace is shared or exposed. <br>
Risk: Fish behavior warnings can be misleading if camera coverage, frame rate, lighting, fish species baseline, or physiological context is poor. <br>
Mitigation: Review the generated metrics and uncertainty flags, ensure the camera covers tank walls, substrate, and rockwork at adequate quality, and treat the output as an observation aid rather than a veterinary diagnosis. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-fish-flashing-scraping-detection-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-style structured reports with fish behavior metrics, alert levels, recommended actions, report links, and command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires video input or a remote video URL plus an open-id; sends aquarium video data and user identifiers to the Life Emergence cloud service for analysis and history lookup.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
