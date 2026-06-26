## Description: <br>
Audit another Codex skill for structural compliance, trigger quality, instruction clarity, reuse of scripts or references, and overall maintainability. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aidenchangzy](https://clawhub.ai/user/aidenchangzy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to audit a Codex skill folder for structural compliance, trigger quality, workflow clarity, resource use, and maintainability before release or revision. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The auditor reads files in the target skill folder and may expose unintended content if pointed at unrelated private directories. <br>
Mitigation: Run it only against the intended skill directory and confirm the target path before execution. <br>
Risk: Quality verdicts may be conservative or incomplete for unusual skill designs. <br>
Mitigation: Use the verdict as review support and confirm release-impacting decisions with human review. <br>


## Reference(s): <br>
- [Skill Audit Rubric](artifact/references/rubric.md) <br>
- [ClawHub skill page](https://clawhub.ai/aidenchangzy/skill-quality-auditor-new) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Guidance] <br>
**Output Format:** [Markdown assessment with optional JSON audit output from the bundled script] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes a verdict, score summary, strengths, weaknesses, critical blockers, and recommended fixes.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
