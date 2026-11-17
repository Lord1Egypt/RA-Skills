## Description: <br>
A multi-agent workflow for MBA and academic thesis writing that supports dual-version drafting, review, integration, finalization, and Word document output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hehe973781230](https://clawhub.ai/user/hehe973781230) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Students, academic writers, and agents use this skill to coordinate long-form MBA or academic thesis drafting, review, integration, and final document generation. It is intended for workflows that need staged human confirmation, academic format checks, and multi-version review before final output. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The security review reports persistent automated workflow behavior, including agent spawning, state maintenance, and possible scheduled execution. <br>
Mitigation: Review the workflow before installing, run it in an isolated environment, and enable scheduled execution only after confirming the state files and workflow behavior. <br>
Risk: The security review reports email fields even though the documented workflow does not include an email or contact flow. <br>
Mitigation: Avoid entering email or contact details unless they are actually required, and remove unused contact fields from local workflow inputs. <br>
Risk: The workflow includes an optional AI-humanization or AI-removal phase that may conflict with academic integrity rules. <br>
Mitigation: Check institutional policy before using that phase and skip it when policy does not allow AI-humanized thesis text. <br>


## Reference(s): <br>
- [Academic Standards Checklist](references/checklist.md) <br>
- [Loop Design Principles](references/loop-design.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/hehe973781230/thesis-workflow) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown drafts and review reports, shell commands, state/configuration JSON, and optional DOCX files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Outputs may include thesis drafts, review reports, task state files, and Word documents in the user's workspace.] <br>

## Skill Version(s): <br>
1.7.3 (source: frontmatter, release metadata, CHANGELOG released 2026-06-19) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
