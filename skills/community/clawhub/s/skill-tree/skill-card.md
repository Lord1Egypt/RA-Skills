## Description: <br>
Track learning across topics like an RPG skill tree with prerequisites, milestones, suggested next steps, and gamified learning paths. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[TheShadowRose](https://clawhub.ai/user/TheShadowRose) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
External learners and developers use this skill to track study progress across prerequisite-based skill trees, mark completed topics, and ask the agent for suggested next skills. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Local progress data remains on disk and may include personal learning details. <br>
Mitigation: Keep the progress file in a trusted workspace, avoid storing sensitive personal details in skill names or notes, and remove the file when it is no longer needed. <br>
Risk: Progress data can be lost or corrupted through local filesystem issues or user error. <br>
Mitigation: Maintain independent backups of important learning progress data before relying on the tracker as a long-term record. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/TheShadowRose/skill-tree) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance, files] <br>
**Output Format:** [Plain text or Markdown progress summaries backed by local JSON progress data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update a local skill-tree.json progress file in the workspace.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
