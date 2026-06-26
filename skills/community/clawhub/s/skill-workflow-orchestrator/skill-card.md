## Description: <br>
Multi-skill workflow orchestrator that chains skills into automated pipelines from a single phrase, with support for sequential execution, conditional branching, and error handling. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[openlark](https://clawhub.ai/user/openlark) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to plan and coordinate multi-step workflows that chain specialized skills, apply conditional branches, and handle step failures. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Automated workflow chaining can trigger powerful local review commands or tests in sequence. <br>
Mitigation: Install only when automated local review is intended, and use normal approval controls or the documented no-yolo option when sandbox bypass is not acceptable. <br>
Risk: Multi-step workflows can propagate incorrect intermediate outputs into later actions. <br>
Mitigation: Review generated workflow plans and require confirmation before sensitive actions such as sending messages, emails, or notifications. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/openlark/skill-workflow-orchestrator) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, configuration, guidance] <br>
**Output Format:** [Markdown with JSON and pseudocode examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe workflow steps, retry settings, fallback behavior, and final output formats such as JSON, Markdown, or text.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
