## Description: <br>
Detects cats, dogs, and birds in home monitoring images or video streams and returns structured pet detection reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit household pet images or videos for cat, dog, and bird detection, count detected animals, and retrieve structured current or historical detection reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Household pet images or videos and a username or phone-derived open-id are sent to a cloud service. <br>
Mitigation: Use only media you are comfortable sharing with the service, avoid sensitive household footage, and confirm retention and handling terms before production use. <br>
Risk: The skill may store local account tokens in a workspace SQLite database. <br>
Mitigation: Restrict workspace access, review or clear the workspace data directory after use, and rotate credentials if the workspace is shared or exposed. <br>
Risk: Historical report access can retrieve cloud report records associated with the supplied open-id. <br>
Mitigation: Use a dedicated non-sensitive open-id, avoid shared identifiers, and verify report access controls with the publisher. <br>
Risk: The security guidance notes a mismatch between pet detection behavior and health-analysis documentation. <br>
Mitigation: Validate the configured endpoints and returned report fields in a controlled environment before relying on the skill for normal workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/smyx-pet-detection-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Pet detection API documentation](artifact/references/api_doc.md) <br>
- [Shared analysis API documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown, JSON, and plain text reports with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Reports can include pet counts, structured detection payloads, historical report lists, and report export links.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release metadata; artifact frontmatter states 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
