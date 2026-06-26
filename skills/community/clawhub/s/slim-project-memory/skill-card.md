## Description: <br>
Slim Project Memory restructures or initializes project memory into a compact CLAUDE.md router, a gitignored local environment reference, a topical docs tree, and a housekeeping protocol. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[adelvillar1](https://clawhub.ai/user/adelvillar1) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to reduce project-memory bloat, separate local environment references from shared documentation, and keep project context organized across sessions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Project memory migration can move or rewrite documentation in ways that lose important project context or point agents at the wrong environment. <br>
Mitigation: Review the proposed section-to-destination map before edits and verify all CLAUDE.md docs pointers resolve after migration. <br>
Risk: Local environment reference files may accidentally include credential values if users paste real secrets into markdown. <br>
Mitigation: Keep CLAUDE.local.md gitignored, record only environment variable names and non-secret URLs, and store real credentials in environment managers or ignored .env files. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/adelvillar1/slim-project-memory) <br>
- [CLAUDE Template](artifact/references/CLAUDE-template.md) <br>
- [Local Environment Reference Template](artifact/references/CLAUDE-local-template.md) <br>
- [Housekeeping Protocol](artifact/references/housekeeping-protocol.md) <br>
- [Case Study: Cruise Intelligence Migration](artifact/references/cruise-intelligence-case-study.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands and file-edit instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or reorganize CLAUDE.md, CLAUDE.local.md, docs files, and .gitignore entries in the target project.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
