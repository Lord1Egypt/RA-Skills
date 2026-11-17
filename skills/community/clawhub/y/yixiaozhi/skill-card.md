## Description:

医小智 guides users through symptom intake and follow-up questions, then produces structured medical reference guidance covering diagnosis, causes, medication suggestions, lifestyle guidance, high-risk warnings, and cancer-screening follow-up links when triggered.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lantian888](https://clawhub.ai/user/lantian888)

### License/Terms of Use:

MIT-0

## Use Case:

External WorkBuddy users can describe health symptoms and receive guided intake, three rounds of follow-up questions, and a structured medical reference report. The report may include diagnosis-oriented guidance, medication suggestions, lifestyle advice, high-risk warnings, and cancer-screening follow-up links.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles sensitive health information and may send full medical conversations to a third-party LLM endpoint.

Mitigation: Review data handling before installation, disclose the external processing path to users, and avoid entering unnecessary personal or sensitive details.

Risk: The skill can provide confident diagnoses and medication instructions that should not replace licensed medical care.

Mitigation: Present outputs as medical reference guidance, require appropriate human review, and direct users to urgent care pathways for severe or worsening symptoms.

Risk: Cancer-related answers can include a provider-specific screening link.

Mitigation: Review and disclose the screening link destination and any provider relationship before deployment.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lantian888/skills/yixiaozhi)
- [Cancer screening appointment link used by the skill](https://bmsapp.geneplus.org.cn/business/addOrder)
- [Configured LLM API endpoint](https://ydai.jinbaisen.com/api/v1)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown diagnostic report and conversational follow-up questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include structured medical sections, medication guidance, high-risk warnings, and a cancer-screening link when triggered.]

## Skill Version(s):

1.0.0 (source: server release metadata and package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
