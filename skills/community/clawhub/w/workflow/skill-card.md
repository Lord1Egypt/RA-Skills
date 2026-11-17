## Description:

Build automated pipelines with reusable components, data flow between nodes, and state management.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ivangdavila](https://clawhub.ai/user/ivangdavila)

### License/Terms of Use:


## Use Case:

Developers and automation engineers use this skill to design, document, test, and maintain reusable workflow pipelines with components, triggers, state, logs, and error handling.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Webhook, file-watcher, or cron triggers could cause workflows to run from untrusted events or paths.

Mitigation: Review workflows before installation, require webhook signature verification and workflow allowlists, and avoid watching untrusted directories.

Risk: Generated workflows may store or use API credentials and service tokens.

Mitigation: Use platform secret storage, keep secrets out of workflow files and logs, and restrict credentials to the minimum required scope.

Risk: Cleanup and state-recovery commands can remove local workflow state or intermediate data.

Mitigation: Review cleanup paths before execution, keep recovery steps scoped to the intended workflow directory, and test with dry-run mode where available.

## Reference(s):

- [ClawHub Workflow skill page](https://clawhub.ai/ivangdavila/skills/workflow)
- [Directory Structure](artifact/structure.md)
- [Components](artifact/components.md)
- [Data Flow Between Nodes](artifact/data-flow.md)
- [State Management](artifact/state.md)
- [Error Handling](artifact/errors.md)
- [Workflow Lifecycle](artifact/lifecycle.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell, YAML, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce workflow files, component templates, run scripts, state conventions, and operational guidance for jq, yq, curl, uuidgen, and flock on Linux or macOS.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
