## Description: <br>
中医养生健康顾问，用于中医辨证、体质辨识、食疗建议、节气养生、穴位保健、中药科普和回访总结等咨询场景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tix007](https://clawhub.ai/user/tix007) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users can use this skill for traditional Chinese medicine wellness guidance, including symptom-oriented pattern analysis, lifestyle and dietary suggestions, acupoint self-care, and follow-up summaries. It is wellness and education oriented and does not replace diagnosis or treatment by licensed clinicians. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can keep persistent local health records and reuse them across later consultations. <br>
Mitigation: Use it only after confirming the memory location and establishing a process to review, disable, or delete stored profiles, consultation blocks, reflection reports, and evolution logs. <br>
Risk: Health and wellness guidance may be mistaken for clinical diagnosis or treatment. <br>
Mitigation: Keep outputs framed as wellness education and route urgent, severe, or persistent symptoms to qualified medical care. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tix007/tcm-wellness) <br>
- [Publisher profile](https://clawhub.ai/user/tix007) <br>
- [Acupoints reference](references/acupoints.md) <br>
- [Classic prescriptions reference](references/classic_prescriptions.md) <br>
- [Memory system reference](references/memory_system.md) <br>
- [Seasonal diet reference](references/seasonal_diet.md) <br>
- [Syndrome differentiation reference](references/syndrome_differ.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown wellness guidance with optional shell commands for local memory utilities] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local memory files for health profiles, consultation blocks, reflections, and evolution logs.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
