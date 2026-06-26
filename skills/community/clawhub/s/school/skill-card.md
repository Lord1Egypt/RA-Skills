## Description: <br>
AI-powered education for K-12 students with parental controls, adaptive learning by age, homework help, exam prep, and progress tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Parents and guardians use this skill to configure age-adapted K-12 tutoring, homework support, exam preparation, curriculum alignment, progress tracking, and safety controls for children ages 3-18. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores child learning progress, session history, and preferences under ~/school/, which can be sensitive even when used for education. <br>
Mitigation: Use minimal child identifiers, avoid full names, school names, addresses, photos, phone numbers, and location details, and periodically review or delete stored records. <br>
Risk: Parents or agents may over-collect or over-share child information while configuring tutoring, progress reports, or curriculum alignment. <br>
Mitigation: Follow the security guidance to keep parent verification private, use the least data needed for the educational task, and confirm platform encryption, access control, and deletion behavior before use. <br>
Risk: K-12 tutoring can produce age-inappropriate or overly direct homework answers if the agent does not follow the skill's safety and tutoring constraints. <br>
Mitigation: Apply the age-specific safety protocols, redirect inappropriate questions, avoid direct answers, and keep parent review focused on progress and safety alerts rather than private conversation text. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/ivangdavila/school) <br>
- [Child Safety Protocols](artifact/safety.md) <br>
- [Parent Dashboard & Controls](artifact/parents.md) <br>
- [Homework Help & Tutoring](artifact/tutoring.md) <br>
- [Curriculum Integration](artifact/curriculum.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Configuration] <br>
**Output Format:** [Markdown guidance and structured workspace notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only skill; no external binaries or API keys are required by the release metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
