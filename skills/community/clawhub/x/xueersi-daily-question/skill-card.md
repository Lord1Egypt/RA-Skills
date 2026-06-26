## Description: <br>
Xueersi Daily Question Generator helps an agent create one grade- and subject-specific K-9 practice question in Chinese, Math, or English, then provide an answer, explanation, key concept, and light progress summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zhouzhi-tal](https://clawhub.ai/user/zhouzhi-tal) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, parents, tutors, and education agents use this skill to generate quick daily practice questions by grade and subject, then give explanations and follow-up practice based on the learner's answer. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic prompts such as "give me a question" may invoke the skill when the user did not intend a Xueersi-style tutoring flow. <br>
Mitigation: Ask for grade and subject, and confirm the tutoring context when the user's intent is ambiguous. <br>
Risk: The skill text claims Xueersi affiliation, but server evidence does not verify that affiliation. <br>
Mitigation: Treat the publisher as zhouzhi-tal and avoid presenting the skill as an official Xueersi release unless the affiliation is independently confirmed. <br>
Risk: Tutoring exchanges may include student details. <br>
Mitigation: Collect only the grade, subject, answer, and problem context needed for the practice flow; avoid unnecessary sensitive student information. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zhouzhi-tal/xueersi-daily-question) <br>
- [Publisher profile](https://clawhub.ai/user/zhouzhi-tal) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown-formatted tutoring response] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a practice question, optional answer choices, answer explanation, key concept, and short progress summary.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
