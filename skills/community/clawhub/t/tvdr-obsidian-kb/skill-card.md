## Description: <br>
通过API与本地Obsidian知识库交互，实现笔记创建、语义搜索及笔记管理功能。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[admirobot](https://clawhub.ai/user/admirobot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to create, search, list, and manage notes through a configured Obsidian knowledge-base API. It supports saving work experience, project documentation, and shared operational knowledge as Markdown notes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends and writes note data to a hardcoded plaintext internal Obsidian service. <br>
Mitigation: Install only when the configured service and network are trusted; avoid secrets, credentials, regulated data, or private operational notes until the endpoint is configurable, authenticated, encrypted, and scoped to approved vault paths. <br>
Risk: Shared knowledge-base writes can persist inaccurate or unintended operational notes. <br>
Mitigation: Review note content and target folders before creating or rebuilding indexed notes, and restrict use to approved folders and workflows. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/admirobot/tvdr-obsidian-kb) <br>
- [Publisher profile](https://clawhub.ai/user/admirobot) <br>
- [Artifact README](artifact/README.md) <br>
- [Artifact SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces API-oriented instructions and helper calls for note creation, semantic search, note listing, statistics, and index rebuild operations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
