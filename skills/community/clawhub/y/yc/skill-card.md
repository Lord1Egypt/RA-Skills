## Description: <br>
CLI for YC Startup School, a16z Speedrun, SPC, and startup program discovery - weekly updates, dashboard, applications, accelerator deadlines. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lucasygu](https://clawhub.ai/user/lucasygu) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External startup founders and their agents use this skill to check YC Startup School status, submit weekly updates, prepare accelerator applications, and discover startup programs from the terminal. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can read browser session cookies for YC Startup School. <br>
Mitigation: Use a specific Chrome profile for the intended account and grant browser or Keychain access only when you are comfortable with the agent using that session. <br>
Risk: The skill can submit live weekly updates or accelerator applications. <br>
Mitigation: Run dry-run or headed preview modes first, inspect generated JSON and form data, and only run live submission commands after user review. <br>
Risk: The npm package runs install and uninstall scripts that modify local Claude Code skill links and patch an installed dependency. <br>
Mitigation: Review the package scripts before installation and install in an environment where those local file changes are acceptable. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lucasygu/yc) <br>
- [Project homepage](https://github.com/lucasygu/yc-cli) <br>
- [OpenClaw ClawHub documentation](https://docs.openclaw.ai/tools/clawhub) <br>
- [YC Startup School](https://www.startupschool.org/) <br>
- [Playwright](https://playwright.dev/) <br>
- [sweet-cookie](https://github.com/steipete/sweet-cookie) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON, shell commands, configuration, guidance] <br>
**Output Format:** [Terminal text, Markdown instructions, JSON templates, and shell commands.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May submit live YC Startup School updates or accelerator applications when the user chooses non-dry-run commands.] <br>

## Skill Version(s): <br>
0.3.2 (source: SKILL.md frontmatter, package.json, server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
