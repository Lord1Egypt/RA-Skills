## Description:

CLI for YC Startup School, a16z Speedrun, SPC, and startup program discovery - weekly updates, dashboard, applications, accelerator deadlines.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lucasygu](https://clawhub.ai/user/lucasygu)

### License/Terms of Use:

MIT

## Use Case:

Developers and startup founders use this agent skill to install and run the yc CLI for Startup School dashboard checks and weekly updates, a16z Speedrun and SPC applications, and startup program discovery.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can use browser session cookies for YC Startup School access.

Mitigation: Use it only when the user intentionally grants access to the relevant browser session, and review requested dashboard reads or weekly update submissions before running them.

Risk: The skill can submit YC updates, a16z Speedrun applications, or SPC application data on the user's behalf.

Mitigation: Use dry-run or headed preview modes when available, and require user review before final submission.

Risk: Installation can modify ~/.claude/skills by creating or replacing the yc-cli skill path.

Mitigation: Inspect any existing ~/.claude/skills/yc-cli path before installation, and back it up or remove it deliberately before proceeding.

Risk: macOS Keychain prompts may request persistent browser cookie access.

Mitigation: Avoid persistent Keychain approval where possible and grant only the access needed for the current task.

## Reference(s):

- [ClawHub yc skill page](https://clawhub.ai/lucasygu/skills/yc)
- [YC CLI homepage](https://github.com/lucasygu/yc-cli)
- [Startup School](https://www.startupschool.org/)
- [Playwright](https://playwright.dev/)
- [sweet-cookie](https://github.com/steipete/sweet-cookie)

## Skill Output:

**Output Type(s):** [Shell commands, JSON, Markdown, Guidance]

**Output Format:** [Markdown with CLI commands and JSON templates]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May run local CLI workflows that read browser cookies or submit updates and applications when requested.]

## Skill Version(s):

0.3.2 (source: frontmatter, package.json, release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
