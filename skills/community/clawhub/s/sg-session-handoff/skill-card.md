## Description: <br>
Summarizes the current session into a precise, file-saved handoff document covering goals, files changed, commands run, errors, decisions, and next steps. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clarezoe](https://clawhub.ai/user/clarezoe) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and AI agents use this skill mid-session or at the end of a session to create a structured Markdown handoff that preserves goals, changed files, commands, errors, decisions, current state, and next steps for another person or AI instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated handoffs may include branch names, file paths, command results, errors, and conversation details that are sensitive in private or shared repositories. <br>
Mitigation: Review generated handoff content before committing, sharing, or using it outside the local project workspace. <br>
Risk: The skill writes local handoff files and may update active handoff pointers or indexes. <br>
Mitigation: Install and run it only when local session handoff files are desired, and review the target handoff path when updating an existing handoff. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clarezoe/sg-session-handoff) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown handoff file with frontmatter, Markdown index, CURRENT pointer text, and concise chat confirmation] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write or update local handoff, CURRENT, and INDEX.md files in the project workspace.] <br>

## Skill Version(s): <br>
1.5.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
