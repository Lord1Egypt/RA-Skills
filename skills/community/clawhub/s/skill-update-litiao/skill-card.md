## Description: <br>
Safely update skills with preview, migration support, and user validation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[litiao1224](https://clawhub.ai/user/litiao1224) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill to check for skill updates, preview diffs and impact, back up existing skill state, and guide migrations or rollbacks with explicit approval. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Updating a skill without previewing changes can break workflows or lose user state. <br>
Mitigation: Present a clear diff and impact summary, flag breaking changes, and proceed only after explicit user approval. <br>
Risk: Migrations, deletions, or failed updates can leave skill data in an inconsistent state. <br>
Mitigation: Create a timestamped backup, apply migration steps only after approval, verify the result, and offer rollback if needed. <br>
Risk: Release metadata may not match the displayed skill identity. <br>
Mitigation: Verify the publisher and target skill before installing when identity or provenance matters. <br>


## Reference(s): <br>
- [Skill Update Litiao on ClawHub](https://clawhub.ai/litiao1224/skill-update-litiao) <br>
- [Preview Changes](artifact/preview.md) <br>
- [Migration Strategies](artifact/migrate.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with shell command examples and approval prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires explicit user approval before updates, migrations, deletions, or rollback actions.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
