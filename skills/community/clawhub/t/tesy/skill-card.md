## Description: <br>
Conducts adversarial red-team analysis by decomposing claims, using parallel expert perspectives, and producing steelman arguments, counterarguments, or synthesized recommendations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kipasdinding6969-alt](https://clawhub.ai/user/kipasdinding6969-alt) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers, architects, reviewers, and decision makers use this skill to stress-test arguments, feature plans, architecture choices, code review options, and other high-stakes proposals before acting on them. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may read local customization files before running workflows. <br>
Mitigation: Keep the customization directory trusted and avoid placing secrets or sensitive private data in customization content. <br>
Risk: The skill sends a localhost notification when workflows run. <br>
Mitigation: Install only in environments where localhost notification behavior is acceptable. <br>
Risk: Multi-agent analysis can copy user-provided context into subagent prompts. <br>
Mitigation: Avoid giving the workflow secrets or private data that should not be shared across analysis prompts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kipasdinding6969-alt/tesy) <br>
- [RedTeam skill overview](artifact/SKILL.md) <br>
- [Parallel analysis workflow](artifact/Workflows/ParallelAnalysis.md) <br>
- [Adversarial validation workflow](artifact/Workflows/AdversarialValidation.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown with structured numbered analysis and recommendations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs commonly include steelman arguments, counterarguments, critique summaries, convergence findings, and synthesized recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
