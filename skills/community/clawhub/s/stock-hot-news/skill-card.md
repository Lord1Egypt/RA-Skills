## Description:

Crawls mainstream Chinese finance news sites, scores and summarizes hot topics, collects live finance news flashes, and generates text and HTML finance reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[diudiuhuang](https://clawhub.ai/user/diudiuhuang)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and finance analysts use this skill to collect recent market news from supported Chinese finance sites, cluster and score hot topics, gather important live updates, and generate operational news reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The clawscan summary reports automatic recursive cleanup through configurable paths.

Mitigation: Run only in an isolated workspace, set dedicated temp_dir and reports_dir locations, and review path configuration before execution.

Risk: The clawscan summary reports credential reuse and API-key handling.

Mitigation: Use a dedicated low-quota API key for this skill and avoid sharing personal or production credentials with the runtime.

Risk: The clawscan summary reports browser-profile reuse and automatic opening of generated HTML reports.

Mitigation: Use a disposable browser profile and avoid opening generated HTML reports from scraped or model-produced content until escaping and URL validation are fixed.

Risk: The clawscan summary reports shell command execution.

Mitigation: Review configured commands and dependencies, then execute the workflow in a sandboxed environment with limited filesystem and network access.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/diudiuhuang/skills/stock-hot-news)
- [Artifact README](artifact/README.md)
- [Directory migration notes](artifact/DIRECTORY_MIGRATION.md)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Configuration, Files]

**Output Format:** [Markdown guidance with bash commands; runtime outputs include JSON, text, screenshot, and HTML report files.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes intermediate files and reports under configured temp_dir and reports_dir paths.]

## Skill Version(s):

1.0.5 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
