## Description: <br>
中医执业医师考试备考助手，用于生成每日复习计划、评估答案和管理错题集。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tom859174-sketch](https://clawhub.ai/user/tom859174-sketch) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External learners preparing for the Chinese medicine practitioner exam use this skill to turn study feedback into daily review plans, evaluate practice-answer results, track weak areas, and maintain a wrong-question review list. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores study history, wrong answers, review timing, preferences, and document-cache metadata locally. <br>
Mitigation: Review or delete the skill memory folder when the data is no longer needed, especially on shared systems. <br>
Risk: The wrong-question export path may not work reliably until the OUTPUT_DIR issue is fixed. <br>
Mitigation: Verify the configured output directory before relying on export results, and keep a fallback copy of important wrong-question records. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tom859174-sketch/tcm-exam-assistant) <br>
- [Publisher profile](https://clawhub.ai/user/tom859174-sketch) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown-style study plans, answer evaluation reports, wrong-question export text, and Node.js command examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local JSON memory files for stage, progress, wrong questions, review scheduling, user preferences, and document-cache metadata.] <br>

## Skill Version(s): <br>
1.0.0 (source: release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
