## Description: <br>
Identifies acquaintances in videos or images through face photo comparison, supports database enrollment, and reports who appears at which location for home or office identity-verification workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, and operators use this skill to compare faces in uploaded images or videos against an enrolled familiar-person database, then review structured recognition results, location annotations, recommendations, and report links. It is suited to home security monitoring and office personnel-management identity checks, but its own notes state results are for reference and not legal identity verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face images, videos, and identity-linked metadata are sent to the Life Emergence service. <br>
Mitigation: Use only with clear consent, legal authorization, and appropriate data-handling controls for the people and locations being analyzed. <br>
Risk: The skill silently creates or reuses identity state and stores service tokens in a local workspace database. <br>
Mitigation: Review local workspace storage before deployment, restrict workspace access, and remove or rotate stored tokens when the skill is no longer needed. <br>
Risk: Cloud history queries expose prior recognition reports with limited user control. <br>
Mitigation: Limit history-query use to authorized users and verify that report access aligns with the organization's retention and privacy requirements. <br>


## Reference(s): <br>
- [Familiar Person Recognition API Documentation](references/api_doc.md) <br>
- [SMYX Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>
- [Skill Demo](https://lifeemergence.com/sample.html) <br>
- [ClawHub Skill Page](https://clawhub.ai/18072937735/skills/smyx-familiar-person-recognition-analysis) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown or JSON analysis reports with optional saved text output and report links] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Can query cloud history, list prior reports as Markdown tables, and process local files or public media URLs up to the documented 10 MB limit.] <br>

## Skill Version(s): <br>
1.0.7 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
