## Description: <br>
Based on computer vision, this skill analyzes pet feeding, drinking, excretion, mental state, vomiting, and limping indicators from camera or feeder monitoring videos and outputs health monitoring reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Pet owners, caretakers, and agents assisting them use this skill to analyze pet monitoring images or videos and generate structured daily health monitoring reports. It can also query cloud-hosted historical reports associated with the local identity used by the skill. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet camera, feeder, or uploaded media may be sent to the lifeemergence cloud service with identity-linked report data. <br>
Mitigation: Use only media you are permitted to upload, avoid private household footage unless that upload risk is acceptable, and review data retention expectations before installation. <br>
Risk: The skill may create or reuse a local identity and store backend tokens in a shared SQLite database. <br>
Mitigation: Inspect local identity and API key material before use, restrict filesystem access, and rotate or remove stored tokens when they are no longer needed. <br>
Risk: Pet health reports may be incomplete or misleading if treated as a diagnosis. <br>
Mitigation: Use reports as informational monitoring only and consult a veterinarian for abnormal findings or medical decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-health-monitoring-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Pet health analysis API documentation](references/api_doc.md) <br>
- [SMYX analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown and JSON health monitoring reports, with optional Markdown tables for historical report lists] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include report links, structured analysis fields, warnings, and saved output files when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.7 (source: ClawHub release metadata; artifact frontmatter says 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
