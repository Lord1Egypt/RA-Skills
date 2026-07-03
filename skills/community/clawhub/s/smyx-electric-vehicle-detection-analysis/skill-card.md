## Description: <br>
Automatically detects electric motorcycles and e-bikes in restricted areas from video streams or images, counts illegal parking or driving instances, and produces violation alerts for safety management in parks, communities, and organizations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, facility managers, and safety operations teams use this skill to analyze surveillance images or video URLs for e-bike and electric motorcycle violations in restricted areas. It returns structured detection results, violation counts, warning levels, management suggestions, and cloud report history when requested. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Media submitted for detection is sent to a cloud service. <br>
Mitigation: Use the skill only with images or videos that are appropriate to share with the publisher-operated lifeemergence.com services, and apply any required privacy review before processing surveillance media. <br>
Risk: The skill can automatically query cloud report history linked to an account identity. <br>
Mitigation: Review report history behavior before installation and restrict use to workspaces where account-linked detection history may be accessed. <br>
Risk: The skill silently creates or reuses account identity and stores reusable tokens locally. <br>
Mitigation: Install only if the publisher and remote services are trusted, and periodically review local workspace data and credential storage according to your security policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-electric-vehicle-detection-analysis) <br>
- [Skill demo](https://lifeemergence.com/sample.html) <br>
- [Electric vehicle detection API documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON text, with optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include violation counts, risk or warning levels, management suggestions, structured API response fields, report links, and historical report listings.] <br>

## Skill Version(s): <br>
1.0.15 (source: server release evidence; artifact frontmatter reports 1.0.8) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
