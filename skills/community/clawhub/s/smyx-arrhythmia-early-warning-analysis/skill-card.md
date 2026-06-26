## Description: <br>
Based on facial video, identifies abnormal rhythms such as premature beats, atrial fibrillation, tachycardia/bradycardia, assists in early detection of heart health risks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and health-oriented agents use this skill to submit facial video or video URLs for non-contact arrhythmia early warning analysis and to retrieve prior cloud-hosted reports. Results are screening guidance only and are not a substitute for ECG testing or clinician diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive facial videos, video URLs, and health report history may be sent to the publisher's cloud service. <br>
Mitigation: Use only with appropriate consent and after confirming the publisher's privacy, retention, deletion, and data-sharing terms. <br>
Risk: The skill may create or reuse an internal identity and store account tokens locally. <br>
Mitigation: Run it in a controlled workspace, inspect local storage before and after use, and avoid sharing the workspace with users who should not access the linked report history. <br>
Risk: Arrhythmia analysis is presented as early warning guidance and may be medically incomplete or incorrect. <br>
Mitigation: Treat outputs as screening information only and direct users to professional ECG testing or a clinician for diagnosis and high-risk findings. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-arrhythmia-early-warning-analysis) <br>
- [Publisher profile](https://clawhub.ai/user/18072937735) <br>
- [Skill usage guide](https://lifeemergence.com/guide.html) <br>
- [API interface documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON-like structured analysis reports, with optional saved output files and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk or recognition results, recommendations, report links, and cloud-hosted historical report tables.] <br>

## Skill Version(s): <br>
1.0.8 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
