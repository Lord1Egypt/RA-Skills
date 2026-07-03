## Description: <br>
Deploys story-writing project infrastructure, including hooks, rules, agents, CLAUDE.md, AGENTS.md, and Codex/OpenCode/OpenClaw configuration. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[worldwonderer](https://clawhub.ai/user/worldwonderer) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External developers and writers use this skill to set up or refresh a structured web-novel writing workspace across Claude Code, OpenCode, Codex, and OpenClaw. It installs project rules, agent definitions, writing references, hooks, and configuration while preserving user-managed files through merge behavior. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs persistent hooks and project-file changes that can affect future writing, commit, and session workflows. <br>
Mitigation: Review the generated deployment plan and target paths before installation, use version control, and install only in writing projects where persistent hooks and project modifications are acceptable. <br>
Risk: Optional browser-based research workflows may reuse an authenticated browser session. <br>
Mitigation: Avoid enabling browser-CDP workflows unless that browser session is appropriate for the project, or use an isolated browser profile. <br>
Risk: The deployed setup can perform automatic GitHub update checks. <br>
Mitigation: Set STORY_NO_UPDATE_CHECK=1 when automatic GitHub requests are not acceptable. <br>
Risk: Security evidence marks the release suspicious because of persistent hooks and browser/session automation pathways. <br>
Mitigation: Treat the security summary as authoritative, review hooks and generated configuration before trusting them, and disable or remove components that are not needed. <br>


## Reference(s): <br>
- [Story Setup ClawHub Page](https://clawhub.ai/worldwonderer/skills/story-setup) <br>
- [OpenClaw Source Metadata](https://github.com/worldwonderer/oh-story-claudecode) <br>
- [SKILL.md](SKILL.md) <br>
- [UPGRADING.md](UPGRADING.md) <br>
- [Agent Reference Bundle](references/agent-references/) <br>
- [Codex Hook Adapter](references/codex/hooks/story_codex_hook.py) <br>
- [OpenCode Model Source](https://models.dev/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown instructions with file edits, shell commands, configuration snippets, and generated project files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install persistent hooks, agent definitions, writing rules, reference files, and CLI-specific configuration into the user's project.] <br>

## Skill Version(s): <br>
1.1.11 (source: server release metadata; artifact frontmatter reports 1.2.5) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
