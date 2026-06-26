## Description: <br>
Merge overlapping local skills into one canonical skill and republish the canonical skill to ClawHub. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[G-Hanasq](https://clawhub.ai/user/G-Hanasq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to consolidate duplicated or overlapping local skills, preserve unique guidance, and publish the canonical skill as the updated ClawHub release. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can remove a redundant local skill folder during cleanup. <br>
Mitigation: Before removal, show the exact skill folder, require explicit approval, and back it up or move it to an archive instead of deleting it immediately. <br>
Risk: Republishing the canonical skill can update the public ClawHub release with an incomplete or incorrect merge. <br>
Mitigation: Verify the merged SKILL.md, version bump, publish result, and remote status before reporting completion. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/G-Hanasq/skill-merge-and-republish) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown report with command summaries and release verification details] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May describe local skill changes, a commit, version bump, publish result, and remote status verification.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
