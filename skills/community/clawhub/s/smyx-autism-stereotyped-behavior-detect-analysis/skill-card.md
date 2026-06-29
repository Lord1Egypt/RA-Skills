## Description: <br>
Analyzes fixed-camera child behavior videos to identify repetitive stereotyped behaviors such as spinning, hand flapping, and body rocking, then produces objective behavior statistics and reports for therapists and guardians. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External therapists, special-education staff, and guardians use this skill to analyze child behavior videos for event-level stereotyped behavior counts, duration summaries, trends, and report links. Results are descriptive behavior observations for professional review, not autism diagnosis or treatment prescriptions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive child behavior videos or video URLs may be sent to an external service. <br>
Mitigation: Use only with guardian consent, avoid unnecessary sensitive footage, and review the publisher's retention, deletion, and privacy controls before deployment. <br>
Risk: Analysis results may be linked to an automatically managed account and local identity or token data. <br>
Mitigation: Run the skill only in an approved environment, restrict local file access, and review token storage and cleanup controls before use. <br>
Risk: Automated behavior detection may be incorrect or misleading in complex scenes. <br>
Mitigation: Require qualified professional review of outputs and do not use the skill as a substitute for clinical diagnosis, standardized assessment, or treatment planning. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-autism-stereotyped-behavior-detect-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Files] <br>
**Output Format:** [Markdown or JSON analysis report with report links; optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs visual behavior statistics and descriptive guidance; does not provide diagnosis or treatment prescriptions.] <br>

## Skill Version(s): <br>
1.0.2 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
