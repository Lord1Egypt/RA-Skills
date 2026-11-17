## Description:

Use TabTab to run AI-powered tasks in a sandboxed multi-agent environment for writing, research, data analysis, web scraping, chart and slide generation, database Q&A, and web or HTML generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bjwswang](https://clawhub.ai/user/bjwswang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to submit prompts and files to TabTab's remote multi-agent API, monitor task progress, retrieve event logs, and download generated outputs for research, analysis, data collection, charts, slides, database Q&A, and HTML generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts, selected files, task metadata, event logs, and downloaded outputs may pass through the configured remote TabTab API.

Mitigation: Install only when the TabTab service is trusted, and avoid uploading confidential or regulated data without explicit approval.

Risk: A configurable TABTAB_BASE_URL can receive the user's API key and uploaded data.

Mitigation: Keep TABTAB_BASE_URL unset or fixed to the official HTTPS origin unless intentionally using a trusted private instance.

Risk: The skill can load credentials from scripts/env.

Mitigation: Protect scripts/env like a secret, restrict file permissions, and do not commit it to version control.

## Reference(s):

- [TabTab Skill on ClawHub](https://clawhub.ai/bjwswang/skills/tabtab)
- [TabTab API Key Settings](https://tabtabai.com/api-key)
- [TabTab Service](https://tabtabai.com)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance, Files]

**Output Format:** [Markdown guidance with bash commands, JSON API responses, saved event-log JSON files, and downloadable ZIP task outputs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires TABTAB_API_KEY; TABTAB_BASE_URL is optional and defaults to the TabTab HTTPS service.]

## Skill Version(s):

1.0.4 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
