## Description: <br>
Auto-triggers Context Engineering compliance and Lobster enforcement when proposing, creating, or formalizing rules, policies, processes, or behavioral constraints. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[levineam](https://clawhub.ai/user/levineam) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent operators use this skill to turn newly stated rules, policies, workflows, or behavioral constraints into persistent governance documentation and, when available, Lobster enforcement workflows. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can automatically modify persistent governance files. <br>
Mitigation: Use a review-first workflow, keep backups, and restrict writes to known governance files. <br>
Risk: The skill can generate executable Lobster workflows from unreviewed rule text. <br>
Mitigation: Inspect generated Lobster workflow files before enabling or running them. <br>
Risk: An uncontrolled TARGET_FILE value could direct writes outside the intended governance documents. <br>
Mitigation: Remove or tightly control TARGET_FILE and allow only approved governance paths. <br>


## Reference(s): <br>
- [ClawHub Rule Creation skill page](https://clawhub.ai/levineam/rule-creation) <br>
- [Context Engineering reference](https://x.com/koylanai/status/2025286163641118915) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown summaries, JSON script results, generated workflow files, governance document entries, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write persistent governance files and generate Lobster workflow files when invoked by an agent.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
