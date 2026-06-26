## Description: <br>
A unified AI Engineering Operating System that guides agents through tacit knowledge extraction, Agent OS file generation, and pre-deployment governance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[danielfoojunwei](https://clawhub.ai/user/danielfoojunwei) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to interview domain experts, turn the results into structured Agent OS files, and audit an agent before deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The extraction interview can collect sensitive business, personal, or regulated details if users overshare. <br>
Mitigation: Ask for only the minimum task context needed and avoid secrets, credentials, regulated data, and unnecessary personal details. <br>
Risk: Proof-of-action checks can be pointed at unintended files if paths are chosen too broadly. <br>
Mitigation: Limit verification paths to files intentionally created or modified for the current project. <br>
Risk: Generated Agent OS files can encode incorrect assumptions if the interview synthesis is not reviewed. <br>
Mitigation: Pause after synthesis and proceed only after the user confirms that the decision rules, edge cases, and preferences are accurate. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/danielfoojunwei/the-tacit-worker) <br>
- [SECI Externalization Interview Framework](artifact/references/extraction_framework.md) <br>
- [Agent OS Architecture Guide](artifact/references/os_architecture_guide.md) <br>
- [Pre-Deployment Governance Checklist](artifact/references/governance_checklist.md) <br>
- [Verify Action Script](artifact/scripts/verify_action.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with templates, inline Python, bash commands, and JSON validation output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces a tacit knowledge profile, Agent OS file templates, audit report structure, and proof-of-action verification guidance.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
