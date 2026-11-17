## Description:

Set up, run, compare, and debug StockValuation.io, a local-first DCF valuation platform, including Docker startup, ticker valuations, LLM provider changes, prompt dumping, and troubleshooting.

This skill is ready for commercial/non-commercial use.

## Publisher:

[softcane](https://clawhub.ai/user/softcane)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and analysts use this skill to set up and operate StockValuation.io locally, run ticker valuation workflows, compare LLM provider settings, inspect prompt dumps, and troubleshoot Docker-based services.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local setup may require API keys and service secrets in a .env file.

Mitigation: Keep secrets out of chat, logs, and commits; configure them only in local environment files or secret managers.

Risk: Prompt dumping can write sensitive prompt contents, ticker context, and retrieved research snippets to disk.

Mitigation: Enable prompt dumping only intentionally, choose a controlled PROMPT_DUMP_DIR, and remove dumps when they are no longer needed.

Risk: Installer scripts and Docker volume deletion can change or remove local state.

Mitigation: Inspect install.sh before running it and use Docker volume deletion only when intentionally resetting local state.

## Reference(s):

- [StockValuation.io GitHub repository](https://github.com/stockvaluation-io/stockvaluation_io)
- [Setup And Run](references/setup-and-run.md)
- [Model And Provider Experiments](references/model-and-provider-experiments.md)
- [Troubleshooting](references/troubleshooting.md)
- [ClawHub skill page](https://clawhub.ai/softcane/skills/stockvaluation-io)

## Skill Output:

**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration]

**Output Format:** [Markdown with inline bash, text, and JSON examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include local setup steps, Docker Compose commands, API examples, environment variable guidance, and troubleshooting checks.]

## Skill Version(s):

1.0.5 (source: ClawHub release metadata; artifact frontmatter says 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
