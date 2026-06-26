## Description: <br>
Analyzes pet toy-area videos or video URLs through server-side APIs to summarize interaction frequency, duration, toy preference, daily activity curves, trend comparisons, and activity-decline alerts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to submit pet toy-area media for interaction activity analysis and to retrieve prior activity reports. The skill is intended for descriptive pet interaction monitoring rather than veterinary or emotional diagnosis. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends pet media, video URLs, and user identifiers to a backend service. <br>
Mitigation: Review the publisher's privacy and retention terms before use; avoid submitting media or URLs containing people, private home details, signed links, internal network resources, or a personally identifying open-id. <br>
Risk: Server security evidence reports that documented and implemented outputs include unrelated face and health analysis that do not fit the stated pet-toy purpose. <br>
Mitigation: Treat results as descriptive pet interaction data only, review outputs for off-purpose health or face-analysis content, and do not rely on the skill for diagnosis or wellness decisions. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/smyx-pet-toy-interaction-activity-analysis) <br>
- [Pet Toy Interaction API Documentation](artifact/references/api_doc.md) <br>
- [Shared Analysis API Documentation](artifact/skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown tables and structured text or JSON returned from API-backed analysis scripts.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include links to exported report images for historical reports.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
