## Description: <br>
Assesses semantic consistency between AI-generated clinical notes and expert gold standards using BERTScore and COMET. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aipoch-ai](https://clawhub.ai/user/aipoch-ai) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and clinical AI evaluators use this skill to compare AI-generated clinical notes against expert gold standards while keeping assumptions, inputs, and fallback paths explicit. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Clinical or similarly sensitive text can appear in inputs, JSON output, and console output. <br>
Mitigation: Use only de-identified text, restrict access to generated artifacts, and handle outputs as sensitive data. <br>
Risk: The package framing does not fully disclose medical-text handling, model download, and dependency risks. <br>
Mitigation: Review the skill before installing, run it in an isolated environment, pin and replace dependencies as needed, and verify model sources. <br>
Risk: The security scan guidance reports a syntax error that can block execution. <br>
Mitigation: Fix and re-run validation on the packaged script before using the skill in an agent workflow. <br>


## Reference(s): <br>
- [Audit Reference](references/audit-reference.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/aipoch-ai/semantic-consistency-auditor) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with command examples and JSON evaluation results] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include source clinical text in JSON or console output; model and dependency setup affects execution.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
