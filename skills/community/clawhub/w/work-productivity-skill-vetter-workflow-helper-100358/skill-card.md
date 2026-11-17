## Description:

Helps agent users and skill authors create practical workflows, checklists, analyses, and implementation support for vetting skills, fixing bugs, hardening setups, and improving reliability.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Agent users, skill authors, maintainers, and teams use this skill to turn skill-vetting, bug-fixing, setup-hardening, and reliability-improvement needs into concrete workflows, artifacts, checklists, analysis, code changes, or decision support.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad trigger wording and implicit invocation can cause the skill to appear in unrelated security, GitHub, or workflow conversations.

Mitigation: Narrow trigger terms or disable implicit invocation when predictable activation matters.

Risk: Workflow guidance may be incomplete if the user omits constraints, inputs, or success criteria.

Mitigation: Restate assumptions, ask only material clarifying questions, and validate the output against the stated success criteria.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Vetter demand signal](https://clawhub.ai/skills/skill-vetter)
- [ClawHub Github skill demand signal](https://clawhub.ai/skills/github)
- [ClawHub SkillScan demand signal](https://clawhub.ai/skills/skillscan)
- [Hacker News LG ThinQ Terms of Use discussion](https://news.ycombinator.com/item?id=48958273)
- [Hacker News GPT-5.6 Sol Max discussion](https://news.ycombinator.com/item?id=48947713)
- [V2EX Codex usage panel discussion](https://www.v2ex.com/t/1228371)
- [GitHub kana-dojo good first issue](https://github.com/lingdojo/kana-dojo/issues/25174)
- [GitHub Continue tool calling redesign issue](https://github.com/continuedev/continue/issues/13000)
- [GitHub Chrome DevTools MCP daemon defaults issue](https://github.com/ChromeDevTools/chrome-devtools-mcp/issues/2388)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code, shell command, checklist, workflow, analysis, or configuration snippets]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs are tailored to available user inputs and should make assumptions, limits, and validation notes visible.]

## Skill Version(s):

0.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
