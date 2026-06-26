## Description: <br>
A personal to-do management skill that helps an agent create, update, query, complete, and delete workspace-local tasks across pending, in-progress, and completed states. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tangruilin](https://clawhub.ai/user/tangruilin) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Individuals and developers use this skill to maintain a lightweight personal task list inside an agent workspace, including task status changes, optional GitHub issue links, and related file paths. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Todo state is persisted in local workspace JSON files. <br>
Mitigation: Install only when local workspace persistence is acceptable, and review the generated todo files if task contents may be sensitive. <br>
Risk: Broad triggers and fuzzy matching can select the wrong todo for status changes or deletion. <br>
Mitigation: Use explicit item numbers or exact task names, and ask the agent to confirm before deleting or changing fuzzy-matched todos. <br>


## Reference(s): <br>
- [Data Schema](references/data-schema.md) <br>
- [Usage Examples](references/examples.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON files, Guidance] <br>
**Output Format:** [Conversational Markdown responses with workspace-local JSON todo files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains separate JSON files for pending, in-progress, completed, and metadata state.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
