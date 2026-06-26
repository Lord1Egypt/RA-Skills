## Description: <br>
Analyzes fixed-camera aquarium video to detect abnormal fish swimming posture, quantify abnormal-duration ratio, and produce structured posture reports and alert guidance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External aquarium owners, public aquarium staff, ornamental fish farms, and developers integrating aquarium monitoring use this skill to analyze fish swimming videos, identify posture anomalies such as side-swimming, upside-down posture, floating or sinking, and generate daily health posture reports. The output is visual posture analysis and suggested follow-up actions, not a veterinary diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Aquarium videos and a user identifier may be sent to the Life Emergence/SMYX cloud service. <br>
Mitigation: Install only after confirming trust in the publisher and use a non-phone identifier for open-id when possible. <br>
Risk: Local workspace data may contain authentication tokens or other sensitive account material. <br>
Mitigation: Treat the workspace database and configuration files as sensitive and restrict access to authorized users. <br>
Risk: Security evidence reports an unsafe dependency entry. <br>
Mitigation: Review or remove the bad yaml dependency before installation or deployment. <br>
Risk: Posture analysis may be mistaken for a veterinary diagnosis or used with inappropriate species baselines. <br>
Mitigation: Use the output as visual posture analysis only, configure species-specific baselines, and require human review for health decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/smyx-fish-abnormal-swimming-detection-analysis) <br>
- [API interface documentation](artifact/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON-style structured analysis with command examples and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include event IDs, tank IDs, scene labels, abnormal-duration ratios, alert actions, daily report fields, and recommended user actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
