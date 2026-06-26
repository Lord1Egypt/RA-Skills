## Description: <br>
Monitors whether personnel remain on duty in specified workplace areas by submitting video or images to a cloud computer-vision service and returning absence status, duration, and history reports. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Operations, safety, and facilities teams use this skill to analyze workplace camera video or images for leave-post and absence events in fixed-duty areas such as production lines, monitoring rooms, service windows, guard posts, toll stations, and business halls. The skill can also retrieve cloud-stored historical absence reports for a supplied user identifier. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends workplace images or video, user identifiers, and generated absence reports to the configured LifeEmergence cloud service. <br>
Mitigation: Use only with approved media and identifiers, review configured API endpoints before deployment, and apply applicable employee notice, consent, and data-retention controls. <br>
Risk: A development private-IP configuration is present in the artifact and could be inappropriate for production use. <br>
Mitigation: Confirm production deployments use the intended public service configuration and do not rely on development endpoints. <br>


## Reference(s): <br>
- [Personnel Absence Monitoring API Documentation](references/api_doc.md) <br>
- [ClawHub Release Page](https://clawhub.ai/18072937735/smyx-staff-absence-detection-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration] <br>
**Output Format:** [Markdown or JSON analysis reports with optional saved text output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Accepts local media paths or media URLs, an open-id user identifier, media type, confidence threshold, and absence threshold; can return current analysis results or historical report listings.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; skill frontmatter reports 1.0.4) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
