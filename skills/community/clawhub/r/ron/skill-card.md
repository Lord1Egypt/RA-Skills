## Description: <br>
Ron is a skeptical reviewer who finds issues in code, reasoning, diagnoses, analysis, and decisions, then returns the problems without fixing them. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nicolasgrasset](https://clawhub.ai/user/nicolasgrasset) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, operators, and decision-makers use Ron for a second-opinion review before shipping code, accepting analysis, resolving incidents, or relying on strategic recommendations. It focuses on finding unsupported claims, missed scope, weak evidence, and overconfident conclusions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can retain short cross-session memory from broad reviews, which may capture sensitive or confidential context if used on private work. <br>
Mitigation: Use it only where persistent memory is acceptable, or disable, restrict, or review memory behavior before use on secrets, customer data, production incidents, private financial plans, or confidential strategy. <br>
Risk: The skill relies on the agent's available read access and may be unable to independently verify source material in restricted sessions. <br>
Mitigation: Require the review to state which sources were directly checked and treat unverified findings as limited-context review output. <br>


## Reference(s): <br>
- [Ron ClawHub release page](https://clawhub.ai/nicolasgrasset/ron) <br>
- [Deploy Checklist](artifact/references/deploy-checklist.md) <br>
- [Ron's Memory](artifact/memory.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, files] <br>
**Output Format:** [Markdown review findings, CLEAR statements, and short memory entries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Review output is limited to issues found or a CLEAR verdict; the skill may append a brief persistent memory entry after each session.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
