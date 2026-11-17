## Description:

爽文体验馆是一个中文文字冒险游戏入口，为代理提供修仙、武侠、民国和校园四类剧情世界的选择界面、启动引导和独立存档说明。

This skill is ready for commercial/non-commercial use.

## Publisher:

[heaven-ll](https://clawhub.ai/user/heaven-ll)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent operators use this skill to launch and navigate a Chinese-language text adventure hub with separate game worlds and save files. The skill helps the agent present menu options, check/install dependent game skills, and guide world-specific play.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may guide the agent to install additional OpenClaw skills, including through broad or unpinned commands.

Mitigation: Verify package names, publisher handles, versions, and sources before approving installation, and avoid global unpinned npx commands.

Risk: Saved game text may persist user choices and story state beyond a single session.

Mitigation: Use dedicated save files for each game world and avoid relying on shared agent memory for game state.

Risk: Install and save behavior is broader and less clearly bounded than users may expect.

Mitigation: Review the launcher behavior and security evidence before deployment, then scan dependent skills separately.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/heaven-ll/skills/shuangwen-tiyanguan)
- [Core logic](references/core_logic.md)
- [Save system](references/save_system.md)
- [UI templates](references/ui_templates.md)
- [Welcome launcher](references/welcome.py)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Chinese-language interactive text with markdown-style menus and command snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May refer to independent save files for each game world and installation commands for dependent OpenClaw skills.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
