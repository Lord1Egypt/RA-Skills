## Description: <br>
Deploys web-novel writing project infrastructure, including hooks, rules, agents, and Claude Code or OpenCode project files, into a user's project directory. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Writers, writing teams, and developers use this skill to set up a structured web-novel project with writing agents, project rules, hooks, reference material, and deployment checks. It is intended for normal ClawHub use in user-owned writing projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent automation, including hooks, an OpenCode plugin, and a git pre-commit block. <br>
Mitigation: Install it only in writing projects where that automation is acceptable, and review the generated hooks, plugin, and pre-commit changes before relying on them. <br>
Risk: The browser/CDP command can interact with pages where the user is already logged in. <br>
Mitigation: Review the browser/CDP command before use and run it only against trusted browser sessions and sites. <br>
Risk: The session update check can perform automatic GitHub release lookups. <br>
Mitigation: Set STORY_NO_UPDATE_CHECK=1 when automatic release lookups are not desired. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/worldwonderer/skills/story-setup) <br>
- [OpenClaw source metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [Upgrade guide](UPGRADING.md) <br>
- [Hook settings template](references/templates/settings-hooks.json) <br>
- [OpenCode plugin](references/opencode/plugin.ts) <br>
- [OpenCode pre-commit block](references/opencode/pre-commit.sh) <br>
- [Writing quality checklist](references/agent-references/quality-checklist.md) <br>
- [Writing craft reference](references/agent-references/writing-craft.md) <br>
- [Dialogue mastery reference](references/agent-references/dialogue-mastery.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance plus generated project files, hook scripts, agent definitions, rules, and configuration JSON] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install persistent hooks, an OpenCode plugin, a git pre-commit block, project-local reference files, and setup markers.] <br>

## Skill Version(s): <br>
1.1.8 (source: ClawHub release metadata; artifact frontmatter reports 1.2.3) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
