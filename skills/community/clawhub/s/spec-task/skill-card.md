## Description: <br>
Spec-task enforces a structured task lifecycle for agent work, including configuration, recall, task creation, document generation, status transitions, verification, and archiving. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leonardo-lb](https://clawhub.ai/user/leonardo-lb) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to manage non-trivial agent tasks through a required brief, spec, plan, checklist, execution log, verification flow, and optional archive. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Task summaries, outputs, history, or lessons may contain sensitive project details when written locally or archived. <br>
Mitigation: Review archive settings before use and avoid including secrets or sensitive task details in task documents, outputs, history, or lessons. <br>
Risk: This release is marked deprecated due to unstable factors. <br>
Mitigation: Prefer the plugin release with the same name when available, or validate the workflow on non-sensitive tasks before relying on it. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/leonardo-lb/spec-task) <br>
- [OpenSpec concept mapping](reference/openspec-mapping.md) <br>
- [Status.yaml format reference](reference/status-format.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown task documents with YAML configuration and status fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates local task documents and may create memory history or lessons when archived.] <br>

## Skill Version(s): <br>
1.2.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
