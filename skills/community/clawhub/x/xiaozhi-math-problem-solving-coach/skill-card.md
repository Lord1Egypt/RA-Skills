## Description: <br>
A Chinese-language math coaching skill that guides students through problem solving, error analysis, concept questions, exam review, and similar practice without directly giving complete answers. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[qizhitang](https://clawhub.ai/user/qizhitang) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students and learning assistants use this skill for math problem coaching, wrong-answer analysis, concept clarification, pre-exam review, and guided generation of similar practice questions. It is designed to ask diagnostic questions and validate understanding rather than provide direct complete solutions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed to store or reuse problem history, weak points, and exam-related study context through learning DNA and math error DNA dependencies. <br>
Mitigation: Review the dependent personalization skills and their data handling expectations before deployment. <br>
Risk: The photo-based workflow depends on multimodal vision or OCR support that may misread math problem images. <br>
Mitigation: Ask the learner to confirm recognized problem text and conditions before coaching begins. <br>
Risk: A tutoring workflow can accidentally reveal complete answers instead of coaching the learner. <br>
Mitigation: Keep the skill's no-direct-answer rule and require guided questions, student reasoning, and similar-problem verification. <br>


## Reference(s): <br>
- [CLAW Template Extensions](references/claw-templates-extended.md) <br>
- [Math Socratic Guide](references/math-socrates-guide.md) <br>
- [Four-Step Photo Method State Machine](references/photo-4step-statemachine.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/qizhitang/xiaozhi-math-problem-solving-coach) <br>
- [ClawHub Publisher Profile](https://clawhub.ai/user/qizhitang) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown conversational guidance, question prompts, study summaries, and practice problems] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Chinese-language tutoring workflow; may use multimodal/OCR support for problem images when the host agent provides it.] <br>

## Skill Version(s): <br>
1.0.0 (source: SKILL.md frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
