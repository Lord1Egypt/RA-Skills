## Description:

Command-line tool for managing Wiki.js pages, assets, templates, backups, search, synchronization, and content analysis through the Wiki.js GraphQL API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hopyky](https://clawhub.ai/user/hopyky)

### License/Terms of Use:

MIT

## Use Case:

Developers, documentation maintainers, and site administrators use this skill to manage Wiki.js content from an agent-assisted command-line workflow, including page CRUD, backup and restore, bulk operations, validation, and analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill handles Wiki.js API tokens and stores configuration under the user home directory.

Mitigation: Use HTTPS Wiki.js URLs, create least-privilege API tokens, and protect ~/.config/wikijs.json.

Risk: The skill can perform destructive or broad wiki changes, including delete, restore, replace, bulk update, and forced operations.

Mitigation: Review exact targets, prefer dry-run or confirmation flows, and keep a fresh backup before running high-impact commands.

Risk: The inspected artifact declares a CLI executable path that is missing from the package contents.

Mitigation: Verify package contents and executable availability before installing or relying on the release.

## Reference(s):

- [ClawHub Wiki.js CLI skill page](https://clawhub.ai/hopyky/skills/wikijs)
- [Wiki.js](https://js.wiki/)
- [Commander.js](https://github.com/tj/commander.js/)
- [Ora](https://github.com/sindresorhus/ora)
- [Chalk](https://github.com/chalk/chalk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands, configuration snippets, and CLI output instructions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Wiki.js API operations, filesystem backup or sync actions, and JSON or table CLI output depending on command options.]

## Skill Version(s):

1.4.0 (source: evidence release metadata, package.json, CHANGELOG released 2026-02-04)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
