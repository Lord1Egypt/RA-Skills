## Description: <br>
Build automated pipelines with reusable components, data flow between nodes, and state management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation-oriented users use this skill to design, create, test, update, and maintain workspace workflow pipelines with reusable components, shell runners, configuration files, state, logs, and data handoff between nodes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Webhook examples could be adapted into a remotely triggerable local workflow runner without complete validation. <br>
Mitigation: Add strict workflow-name allowlisting, resolved-path checks, signature and timestamp verification, and explicit user approval before any selected workflow is executed. <br>
Risk: Generated run.sh files and automation snippets may perform network calls, write state, update schedules, or remove files when copied into a workspace. <br>
Mitigation: Review generated scripts before execution, run dry-run mode first, use least-privilege credentials, and replace broad cron, removal, or deletion examples with scoped reversible procedures. <br>
Risk: Workflow state, logs, and intermediate data can become stale, corrupted, or expose sensitive operational details. <br>
Mitigation: Define retention and recovery procedures, keep secrets in the configured credential store rather than logs or data files, and validate state before reruns or recovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/workflow) <br>
- [Publisher profile](https://clawhub.ai/user/ivangdavila) <br>
- [Directory Structure](artifact/structure.md) <br>
- [Data Flow Between Nodes](artifact/data-flow.md) <br>
- [State Management](artifact/state.md) <br>
- [Error Handling](artifact/errors.md) <br>
- [Components](artifact/components.md) <br>
- [Workflow Lifecycle](artifact/lifecycle.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands, YAML examples, JSON examples, and workflow file templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires jq, yq, curl, uuidgen, and flock on Linux or macOS; examples may create workflow files, state, data, and logs in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
