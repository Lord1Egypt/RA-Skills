## Description: <br>
Provides task planning, validation, approval, dry-run, and execution utilities for AI agents using pure Python. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cerbug45](https://clawhub.ai/user/cerbug45) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to define, validate, approve, dry-run, persist, and execute ordered task plans through custom Python executor functions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The server security summary says the skill overstates safety while allowing auto-approved execution through arbitrary user-provided executors. <br>
Mitigation: Keep auto_approve disabled for sensitive workflows, require manual review before execution, and connect only tightly allowlisted executor functions. <br>
Risk: Plans loaded from disk or produced by another agent can drive real executor behavior if approved. <br>
Mitigation: Review every loaded plan, use dry runs before live execution, and treat the built-in validator and rollback support as aids rather than security boundaries. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cerbug45/task-panner-validator) <br>
- [README](artifact/README.md) <br>
- [Quickstart](artifact/QUICKSTART.md) <br>
- [API reference](artifact/API.md) <br>
- [Changelog](artifact/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and shell commands; runtime APIs produce Python objects, JSON plan files, logs, and execution summaries.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses the Python standard library and supports dry-run execution, manual approval, plan persistence, and execution summaries.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
