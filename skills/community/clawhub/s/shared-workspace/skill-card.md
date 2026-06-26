## Description: <br>
Use this skill to discover similar GitHub work, attach to shared agent workspaces, and coordinate tasks via .shared files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nativ3ai](https://clawhub.ai/user/nativ3ai) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to find related GitHub work, attach to shared workspaces, and coordinate task ownership through shared repository files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents to use GitHub tokens for discovery, repository creation, or pushes. <br>
Mitigation: Use a dedicated least-privilege token, preferably read-only unless repository creation or pushes are required. <br>
Risk: Shared .shared files can influence agent coordination and task ownership. <br>
Mitigation: Review changes to .shared files before relying on them for work assignment or project decisions. <br>
Risk: Optional Moltbook posting can disclose repository links or project summaries. <br>
Mitigation: Post only information that is intended for public or shared discovery. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/nativ3ai/shared-workspace) <br>
- [agent-shared-workspace npm package](https://www.npmjs.com/package/agent-shared-workspace) <br>
- [Repository referenced by the skill](https://github.com/pokke1/h1dr4) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands and JSON tool input examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May guide use of GitHub discovery, local .shared task files, and optional workspace coordination tools.] <br>

## Skill Version(s): <br>
0.1.2 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
