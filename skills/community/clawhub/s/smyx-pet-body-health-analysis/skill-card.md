## Description: <br>
Identifies obesity, emaciation, external injuries, skin abnormalities, and abnormal mental states in pet images or videos, helping pet owners detect health issues promptly. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and pet-care agents use this skill to submit pet photos, videos, or media URLs for body condition and visible health analysis. The skill returns structured findings, health-reference guidance, report links, and cloud-sourced history reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Pet media is sent to the provider's cloud service for analysis. <br>
Mitigation: Use only media that the user is comfortable sharing with the provider, and avoid private home videos or other sensitive media unless the publisher and retention claims have been reviewed. <br>
Risk: The skill creates or reuses a local identity and stores authentication tokens in the workspace. <br>
Mitigation: Install and run the skill only in a workspace where local token storage is acceptable, and review or clear stored credentials according to the deployment's credential handling policy. <br>
Risk: Pet-health analysis results may be mistaken for professional veterinary diagnosis. <br>
Mitigation: Present outputs as health-reference guidance only and direct users to consult a veterinarian when abnormalities or urgent symptoms are detected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-body-health-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Pet health analysis API documentation](references/api_doc.md) <br>
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, guidance] <br>
**Output Format:** [Markdown text with optional JSON analysis output and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save analysis output to a user-specified file; historical report queries are returned as Markdown tables from the cloud API.] <br>

## Skill Version(s): <br>
1.0.6 (source: ClawHub release metadata; artifact frontmatter lists 1.0.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
