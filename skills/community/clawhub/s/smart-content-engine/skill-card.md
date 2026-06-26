## Description: <br>
Content Engine helps agents create, adapt, manage, and distribute content across Twitter/X, LinkedIn, WeChat Official Accounts, blogs, Medium, and Obsidian workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hanjing5024064](https://clawhub.ai/user/hanjing5024064) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Content creators, marketers, and content operations teams use this skill to manage drafts, adapt content to platform-specific formats, plan publishing calendars, collect performance metrics, and generate AI image prompts. It is intended for agent-assisted content workflows that may include local storage, Obsidian import/export, and optional platform publishing. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Obsidian and export paths can read or overwrite local files outside the intended content area. <br>
Mitigation: Use a dedicated vault or publishable-drafts folder, pass only known paths, and review target paths before import, export, or sync actions. <br>
Risk: Publishing tokens may allow access to external content platforms. <br>
Mitigation: Store tokens outside source control, use the minimum permissions available, and rotate or revoke tokens when no longer needed. <br>
Risk: Automated publishing can distribute incomplete, incorrect, or unintended content. <br>
Mitigation: Preview adapted content and require explicit confirmation before every publish or scheduled publish action. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/hanjing5024064/smart-content-engine) <br>
- [Platform Specifications](artifact/references/platform-specs.md) <br>
- [WeChat Guide](artifact/references/wechat-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Chinese conversational guidance, Markdown drafts and previews, JSON CLI inputs, and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local content records, calendar exports, adapted platform drafts, reports, and AI image prompts.] <br>

## Skill Version(s): <br>
1.1.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
