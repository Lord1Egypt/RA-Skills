## Description: <br>
故事接龙 supports collaborative story writing, local story management, style selection, and template-based story continuation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[yansocool](https://clawhub.ai/user/yansocool) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and writers use this CLI skill to start, continue, view, switch, complete, and delete locally stored collaborative stories across several Chinese-language story styles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The delete command can permanently remove local story files without sufficient safeguards. <br>
Mitigation: Keep separate backups, verify the exact story ID before deleting, and prefer a release that validates IDs and uses confirmation or soft-delete. <br>
Risk: Important or sensitive drafts may be stored locally in the OpenClaw workspace. <br>
Mitigation: Review storage location and access controls before use, and avoid storing sensitive drafts unless the local environment is appropriate. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/yansocool/story-relay) <br>
- [Project Homepage](https://github.com/openclaw/story-relay) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration] <br>
**Output Format:** [Console text and locally persisted JSON story files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores story state under the local OpenClaw workspace.] <br>

## Skill Version(s): <br>
2.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
