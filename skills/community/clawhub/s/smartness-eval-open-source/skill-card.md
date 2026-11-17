## Description:

Smartness Eval Open Source evaluates an OpenClaw agent across functional tests, system health, and growth signals, producing scores, evidence, risks, recommendations, and trend reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yh22e](https://clawhub.ai/user/yh22e)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agent operators use this skill to run quick, standard, or deep evaluations of OpenClaw workspaces, compare capability changes after upgrades, and generate structured reports for audits or sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill runs local OpenClaw workspace scripts, and the server security summary says its command execution guard is weaker than documented.

Mitigation: Review the configured task suite and tighten command validation to the documented prefix whitelist before using it in sensitive workspaces.

Risk: The optional LLM judge can send evaluation summaries and the selected API credential to a configurable endpoint.

Mitigation: Keep --llm-judge disabled unless the endpoint is trusted, use a dedicated credential, and review the transmitted summary fields before enabling it.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yh22e/skills/smartness-eval-open-source)
- [Architecture](docs/ARCHITECTURE.md)
- [Scoring formulas](docs/SCORING.md)
- [Security model](SECURITY.md)
- [FAQ](docs/FAQ.md)
- [Showcase](docs/SHOWCASE.md)

## Skill Output:

**Output Type(s):** [text, markdown, configuration, guidance]

**Output Format:** [JSON and Markdown reports, with console JSON or Markdown output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes run JSON, dated Markdown reports, and history JSONL under state/smartness-eval/.]

## Skill Version(s):

0.3.3 (source: server release metadata and artifact _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
