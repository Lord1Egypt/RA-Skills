## Description:

scellrun helps agents run and explain report-first single-cell analysis for .h5ad, 10x mtx, Cell Ranger, loom, or tabular expression matrix inputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[drstrangerujn](https://clawhub.ai/user/drstrangerujn)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use scellrun to run single-cell analysis workflows, choose appropriate CLI commands, inspect generated reports and decision logs, and explain results to clinicians or bench scientists in plain language.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned package installation guidance can introduce supply-chain or reproducibility risk on sensitive data hosts.

Mitigation: Review operational risks before install and prefer pinned or internally mirrored scellrun packages.

Risk: Remote execution against clinical or lab data can affect sensitive input and output directories.

Mitigation: Confirm the SSH target before running and use a dedicated least-privilege account with access only to needed directories.

Risk: Optional AI-assisted runs can expose credentials or data if API keys are handled unsafely or external calls are not authorized.

Mitigation: Use --no-ai unless the user explicitly authorizes external AI calls; if AI is needed, inject credentials through a secrets manager or ephemeral environment and avoid placing API keys in commands, chat, logs, history, or persistent plaintext files.

## Reference(s):

- [ClawHub scellrun skill page](https://clawhub.ai/drstrangerujn/skills/scellrun)
- [scellrun repository listed in artifact](https://github.com/drstrangerujn/scellrun)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with inline shell commands, configuration snippets, and concise analysis summaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May reference scellrun reports, decision logs, generated files, and optional external AI calls when explicitly authorized.]

## Skill Version(s):

1.3.3 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
