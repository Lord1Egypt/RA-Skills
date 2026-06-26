## Description: <br>
Provides a JavaScript evaluation helper for RAG quality, reasoning quality, and hallucination detection with single-case and batch evaluation APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yuyonghao-123](https://clawhub.ai/user/yuyonghao-123) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to score RAG outputs, inspect reasoning steps, detect possible hallucinations, and generate batch evaluation summaries for AI-generated content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Evaluation scores are simple heuristic checks rather than authoritative safety judgments. <br>
Mitigation: Use the outputs as review aids and pair them with human review or task-specific validation before deployment decisions. <br>
Risk: Some documentation examples use parameter names that do not exactly match the implementation. <br>
Mitigation: Confirm request parameters against the JavaScript source APIs before wiring the skill into automated workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yuyonghao-123/yuyonghao-evaluation-suite) <br>
- [Skill Documentation](artifact/SKILL.md) <br>
- [Package Manifest](artifact/package.json) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Code, Configuration, Guidance] <br>
**Output Format:** [JavaScript objects with scores, pass/fail flags, indicators, and aggregate report data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs are heuristic evaluation results and should be reviewed before they are used as authoritative quality or safety judgments.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
