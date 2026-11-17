## Description:

Drive an existing runnable web application through a real browser to find and evidence functional, interaction, and UI defects and, only when requested, repair them, validate changes, deploy to an authorized environment, and run post-deployment regression.

This skill is ready for commercial/non-commercial use.

## Publisher:

[liubai00](https://clawhub.ai/user/liubai00)

### License/Terms of Use:

MIT No Attribution

## Use Case:

Developers and QA engineers use this skill to run evidence-backed browser smoke, regression, repair, and release verification loops for existing runnable web applications. It helps an agent preserve QA state, respect authorization boundaries, and report covered scenarios, defects, verification results, deployment outcomes, and residual risk.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The workflow can drive a real browser and may interact with live application state.

Mitigation: Use it only against an authorized target, keep high-side-effect actions scoped to the current task, and require explicit authorization for production, credentials, deployment, rollback, Git delivery, and external notifications.

Risk: Repair and release modes can modify source, run verification, deploy, or record rollback and delivery outcomes when authorized.

Mitigation: Select the least-permissive mode that satisfies the request, keep repair, deployment, rollback, and delivery permissions separate, and verify changes with the declared checks and browser scenarios before reporting success.

Risk: QA ledgers and evidence references could accidentally capture sensitive details.

Mitigation: Store sanitized evidence references only and do not store secrets, raw personal data, cookies, tokens, passwords, or unrelated user data in ledger entries.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/liubai00/skills/webapp-qa-loop)
- [Project Homepage](https://github.com/liubai00/webapp-qa-loop)
- [Scope and Scenario Selection](references/scope-and-selection.md)
- [Browser Playbook](references/browser-playbook.md)
- [Issue Ledger](references/issue-ledger.md)
- [Repair and Reuse Gate](references/repair-and-reuse.md)
- [Release and Rollback Gate](references/release-and-rollback.md)
- [Automation Promotion](references/automation-promotion.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown reports with inline commands, code/configuration changes when authorized, and ledger-backed evidence summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are bounded by the authorized QA mode and should avoid secrets, raw personal data, and claims of exhaustive defect freedom.]

## Skill Version(s):

1.0.1 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
