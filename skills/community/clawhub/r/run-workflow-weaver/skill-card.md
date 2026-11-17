## Description:

API documentation generator and diagram creator that uses Workflow Weaver to turn OpenAPI specs, API endpoints, and code snippets into visual workflows, process diagrams, and step-by-step guides.

This skill is ready for commercial/non-commercial use.

## Publisher:

[britrik](https://clawhub.ai/user/britrik)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and technical writers use this skill to generate API documentation, diagrams, process guides, and exportable workflow artifacts from API specs, endpoints, and code snippets.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Installation may run mutable npm packages, including examples that use latest package tags.

Mitigation: Prefer pinned Workflow Weaver package versions and review package provenance before installation.

Risk: Workflow Weaver refresh tokens and MCP credentials can be exposed through shell history, logs, project-local config files, or agent transcripts.

Mitigation: Use environment variables or protected user-level config, avoid printing tokens, keep credentials out of project files, and rotate tokens if exposure is suspected.

Risk: Generated public share links may expose source material or derived API documentation.

Mitigation: Review source inputs and generated outputs before creating or distributing public share links.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/britrik/skills/run-workflow-weaver)
- [Workflow Weaver app](https://weaver.vibingfun.com)
- [workflow-weaver npm package](https://www.npmjs.com/package/workflow-weaver)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with bash, JSON, and MCP configuration examples; generated Workflow Weaver exports may be Markdown, SVG, PNG, PDF, or JSON.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires Node.js 20 or newer, Workflow Weaver CLI or MCP tools, and user-provided Workflow Weaver credentials for live generation.]

## Skill Version(s):

0.1.2 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
