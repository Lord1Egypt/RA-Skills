## Description:

Use when the user wants to use Repo Scout or work on the Repo Scout project to search GitHub repos, generate project ideas and reports, compare runs, inspect history or trending data, build dashboards, manage bookmarks/watchlists, or prepare publishable scouting outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[itsvips](https://clawhub.ai/user/itsvips)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, founders, and research-oriented teams use this skill to guide Repo Scout CLI usage for GitHub repository discovery, trend tracking, scouting reports, dashboards, watchlists, and publishable project ideas.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Repo Scout CLI commands may contact GitHub when searching repositories, refreshing bookmarks, inspecting trends, or generating scouting outputs.

Mitigation: Confirm the target topic or repository and expected network access before running Repo Scout commands.

Risk: Report, dashboard, history, and bookmark workflows may save local outputs.

Mitigation: Use explicit output paths when saving results and review generated files before sharing or reusing them.

## Reference(s):

- [Repo Scout command map](references/commands.md)

## Skill Output:

**Output Type(s):** [guidance, shell commands, markdown, code, configuration]

**Output Format:** [Text or Markdown guidance with inline Repo Scout shell commands; commands may request table, Markdown, JSON, HTML, or saved-file outputs from Repo Scout.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are shaped by the selected Repo Scout command and flags such as --format, --markdown, --json, and --out.]

## Skill Version(s):

1.0.0 (source: ClawHub release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
