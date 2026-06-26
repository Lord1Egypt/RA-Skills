## Description: <br>
Generates USMLE Step 1 and Step 2 CK style clinical cases with patient history, physical findings, diagnostics, multiple-choice questions, and answer explanations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Medical educators, learners, and exam-preparation authors use this skill to generate structured USMLE-style practice vignettes, answer choices, explanations, and learning objectives for educational review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated medical education content may contain clinical inaccuracies or outdated guidance. <br>
Mitigation: Review generated cases against authoritative medical sources and do not use them for diagnosis or treatment. <br>
Risk: Setup instructions include an unexplained dependency entry named main. <br>
Mitigation: Verify or remove the dependency before running pip install -r requirements.txt. <br>
Risk: The skill executes local Python code to generate cases. <br>
Mitigation: Run the script in a controlled workspace and review output files before relying on them. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/aipoch-ai/usmle-case-generator) <br>
- [Guidelines](references/guidelines.md) <br>
- [USMLE patterns](references/usmle_patterns.md) <br>
- [Medical specialty topics](references/topics.json) <br>
- [Case templates](references/case_templates.json) <br>
- [Sample input](references/sample_input.json) <br>
- [Sample output](references/sample_output.json) <br>
- [Runtime requirements](references/requirements.txt) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, guidance] <br>
**Output Format:** [Plain text, Markdown, or JSON clinical case scenarios with multiple-choice questions and explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs can vary by USMLE step, specialty topic, condition, difficulty, count, format, and answer-key inclusion.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
