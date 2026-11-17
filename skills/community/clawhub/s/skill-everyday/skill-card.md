## Description:

Skill Everyday fetches trending ClawHub skills, analyzes one not-yet-processed skill per run, and writes a local report.

This skill is ready for commercial/non-commercial use.

## Publisher:

[autoxj](https://clawhub.ai/user/autoxj)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to monitor popular ClawHub skills and generate one Markdown analysis report per run while tracking already analyzed skills locally.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Remote ClawHub data can influence local report content and derived filesystem paths.

Mitigation: Validate skill slugs, enforce path containment under the skill workspace, and escape Markdown/YAML-sensitive content before routine use.

Risk: The runner may inspect neighboring skill directories when matching a fetched skill slug to local source files.

Mitigation: Run it only in workspaces where neighboring skill directory names are acceptable to list, or disable local source lookup.

Risk: Playwright is installed as a runtime dependency without a lockfile in the artifact.

Mitigation: Pin dependency versions with a lockfile and install Chromium from a trusted package workflow.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/autoxj/skills/skill-everyday)
- [ClawHub skills listing](https://clawhub.ai/skills)
- [Playwright installation documentation](https://playwright.dev/docs/intro)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, files]

**Output Format:** [Markdown report files with a terminal text summary]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates data/analyzed.json and data/reports/ locally; also updates data/reports/LATEST.md with the most recent report.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
