## Description: <br>
Summarize condenses long AI coding sessions into structured progress summaries while tracking errors, lessons learned, and layered memory updates. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[gtbwpkwjnb-alt](https://clawhub.ai/user/gtbwpkwjnb-alt) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users invoke this skill with the standalone summarize trigger to produce concise session reports, progress status, next steps, error summaries, and memory updates for supported coding agents. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can persist session context, summaries, and error history on disk. <br>
Mitigation: Review storage paths before use and avoid running it in projects where session content should not be retained. <br>
Risk: The skill may write to project or global agent memory and rule files. <br>
Mitigation: Inspect proposed memory and rule updates before accepting them, and disable or remove flows that update shared agent configuration. <br>
Risk: One-line remote installation can obscure what the installer changes. <br>
Mitigation: Use manual installation or inspect the installer scripts before execution. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/gtbwpkwjnb-alt/skills/session-summarize) <br>
- [Archive model](references/archive-model.md) <br>
- [Installation](references/installation.md) <br>
- [Skill analytics](references/skill-analytics.md) <br>
- [Trigger examples](references/trigger-examples.md) <br>
- [Changelog](references/CHANGELOG.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown session summary with structured progress, risk, and memory sections] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write session summaries, error history, pending decisions, and memory updates to local agent/project files.] <br>

## Skill Version(s): <br>
6.6.3 (source: server release, skill frontmatter, VERSION) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
