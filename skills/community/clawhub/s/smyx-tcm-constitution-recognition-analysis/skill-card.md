## Description: <br>
Analyzes face images or videos to identify nine Traditional Chinese Medicine constitution types and return constitution scores, tendencies, health risks, and personalized wellness suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and health or wellness practitioners use this skill to run wellness-oriented TCM constitution analysis from face media and to retrieve prior cloud-generated constitution reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Face photos, videos, and health-adjacent analysis data are sent to the Life Emergence cloud service. <br>
Mitigation: Use only media the user is comfortable uploading, review the configured service endpoints before use, and avoid uploading sensitive media unless necessary. <br>
Risk: The skill can create or reuse a persistent identity and associate reports with that identity. <br>
Mitigation: Tell users that report history is tied to a persistent identity and avoid exposing internal identity values in prompts, logs, or outputs. <br>
Risk: Authentication tokens may be stored locally for cloud API access. <br>
Mitigation: Protect the runtime environment and local configuration files, and rotate or clear stored credentials when the skill is no longer needed. <br>
Risk: Historical report lookup can expose private health-related records. <br>
Mitigation: Run history queries only for the current user context and treat returned report links and records as private. <br>


## Reference(s): <br>
- [ClawHub Skill Release](https://clawhub.ai/18072937735/skills/smyx-tcm-constitution-recognition-analysis) <br>
- [Life Emergence Skill Guide](https://lifeemergence.com/guide.html) <br>
- [TCM Constitution Recognition API Documentation](references/api_doc.md) <br>
- [Shared Analysis API Documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files] <br>
**Output Format:** [Markdown report text with structured JSON content and optional saved output file] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include cloud report export links and historical report lists returned by the Life Emergence service.] <br>

## Skill Version(s): <br>
1.0.4 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
