## Description: <br>
Vibecoding Pro guides agents through a Generator-Evaluator workflow for AI-assisted coding, using independent browser, API, or content evaluation with scoring rubrics and iteration loops to improve artifacts against a spec. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zmy1006-sudo](https://clawhub.ai/user/zmy1006-sudo) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering teams use this skill to structure AI-assisted software work around a separate generator and evaluator, especially for interactive UI, API, and content workflows that need repeatable acceptance checks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluator or browser automation can interact with real systems if pointed at live URLs or production accounts. <br>
Mitigation: Only evaluate systems intended for testing, use scoped test credentials, and review generated actions before allowing agents to change code or data. <br>
Risk: Evaluator feedback can be misleading when the spec, rubric, or calibration examples are incomplete. <br>
Mitigation: Keep the spec as the evaluator source of truth, calibrate scoring before use, and add human review for production-critical or brand-sensitive work. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zmy1006-sudo/vibecoding-pro) <br>
- [VibeCoding Pro architecture reference](artifact/references/architecture.md) <br>
- [Evaluator prompt templates](artifact/references/evaluator-prompts.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with prompt templates, JSON evaluation schemas, Python scripts, and CLI examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes scoring rubrics, evaluator calibration guidance, and iteration-loop implementation templates.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
