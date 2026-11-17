## Description:

Monitor and analyze Weights & Biases training runs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[chrisvoncsefalvay](https://clawhub.ai/user/chrisvoncsefalvay)

### License/Terms of Use:


## Use Case:

Developers and ML engineers use this skill to check W&B training run health, inspect loss, gradient, and evaluation trends, compare experiments, and monitor active or recently completed jobs.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can read W&B run metadata, configs, summaries, and histories available to the user's configured credentials.

Mitigation: Install and run it only with intended W&B credentials and specify the target entity, project, and run IDs explicitly.

Risk: watch_runs.py can query built-in default scopes when invoked without explicit entity and project selections.

Mitigation: Pass the intended entity and --projects or --all-projects deliberately, especially for shared or sensitive W&B accounts.

Risk: Health verdicts are threshold-based monitoring heuristics and can miss or misclassify training issues.

Mitigation: Treat alerts as guidance and confirm important decisions against W&B dashboards, logs, and project-specific expectations.

## Reference(s):


## Skill Output:

**Output Type(s):** [text, markdown, JSON, shell commands, guidance]

**Output Format:** [Markdown summaries with shell commands and optional JSON from helper scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses configured W&B credentials to read selected entity, project, and run data.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
