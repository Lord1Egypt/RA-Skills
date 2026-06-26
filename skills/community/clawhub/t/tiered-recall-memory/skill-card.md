## Description: <br>
Tiered Recall loads core memory, recent logs, active project context, and a compact memory index so an agent can resume work across sessions and perform deeper recall on request. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[davidme6](https://clawhub.ai/user/davidme6) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve project continuity by loading local long-term notes, recent daily logs, active project metadata, and indexed memory snippets into a new or ongoing session. It is also used for manual deep recall by project, topic, date range, or keyword. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can surface private notes and project context from local memory files into later agent sessions. <br>
Mitigation: Review MEMORY.md, memory/, and .tiered-recall before use, and keep credentials, tokens, regulated personal data, and client-confidential data out of those files. <br>
Risk: Automatic recall can expose local context during shared-screen, shared-account, or otherwise sensitive work. <br>
Mitigation: Disable or avoid automatic recall in sensitive collaboration settings and use targeted manual recall only when the context is appropriate to share. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/davidme6/tiered-recall-memory) <br>
- [ClawHub Homepage Metadata](https://clawhub.com/skill/tiered-recall) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown and JSON-oriented text with shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Default recall targets about 20k tokens; deep recall can load larger batches up to the configured budget.] <br>

## Skill Version(s): <br>
1.1.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
