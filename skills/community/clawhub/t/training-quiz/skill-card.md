## Description: <br>
Interactive product knowledge training and quiz system for retail staff that tests product specs, store policies, sales techniques, and FAQs while tracking completion and scores per employee. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fangwei-frank](https://clawhub.ai/user/fangwei-frank) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Retail staff use this skill to practice product knowledge, store policy, FAQ, and sales scenario questions through flashcards, multiple choice quizzes, and role-play prompts. Managers may request concise progress reports based on stored employee quiz history. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Employee quiz results and progress reports may expose staff performance data. <br>
Mitigation: Define who may start tracked sessions, who may request manager reports, what notice or consent is required, and how long quiz history is retained before deployment. <br>
Risk: Accidental triggers could start tracking or save training results unexpectedly. <br>
Mitigation: Use narrow trigger phrases and require confirmation before saving a learner's quiz results. <br>
Risk: Generated questions depend on the accuracy of products, policies, and FAQs in the knowledge base. <br>
Mitigation: Review the knowledge base and sample generated quizzes before using the skill for staff training. <br>


## Reference(s): <br>
- [Question Bank Templates](references/question-bank.md) <br>
- [Training Quiz on ClawHub](https://clawhub.ai/fangwei-frank/training-quiz) <br>
- [Publisher profile](https://clawhub.ai/user/fangwei-frank) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, json, guidance] <br>
**Output Format:** [Conversational Markdown for quiz sessions and progress summaries; JSON arrays when using the question-generation script.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May store per-employee quiz progress in agent memory and summarize that progress for managers on request.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
