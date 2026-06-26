## Description: <br>
This skill analyzes pet grooming video URLs or local video files through server-side APIs to identify stress behaviors such as struggling, panting, and tail tucking, then returns stress-level grading and behavior observations for groomers, veterinary clinics, and pet care services. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[18072937735](https://clawhub.ai/user/18072937735) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External pet groomers, veterinary clinic staff, pet care service teams, and agent developers use this skill to submit grooming-session videos for structured stress-behavior analysis and report lookup. The skill is intended to support behavioral observation and timely grooming workflow intervention, not veterinary diagnosis or behavior-correction advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may upload grooming videos to external services. <br>
Mitigation: Review the skill before installing and use it only when the user is comfortable with that data handling. <br>
Risk: The skill may query cloud report history and create or reuse an identity. <br>
Mitigation: Use a dedicated open-id rather than a personal phone number or shared workspace secret. <br>
Risk: The skill handles remote login or registration and local token storage in ways users are not clearly told about. <br>
Mitigation: Confirm account and token handling expectations before deployment and limit use to appropriate test or operational identities. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/18072937735/skills/smyx-pet-grooming-stress-behavior-analysis) <br>
- [API interface documentation](references/api_doc.md) <br>
- [Analysis API documentation](skills/smyx_analysis/references/api_doc.md) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, JSON, Files, Shell commands, Configuration instructions] <br>
**Output Format:** [Markdown and JSON-like structured text, with optional saved output files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include stress-behavior observations, stress-level grading, history report lists, and report export links.] <br>

## Skill Version(s): <br>
1.0.2 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
