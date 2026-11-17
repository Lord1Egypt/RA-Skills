## Description:

中国传媒大学瑜伽精品课（赵晓琳老师）瑜伽体式知识库，帮助用户查询瑜伽体式名称、动作步骤、练习要点、目标肌肉、考试提示和文化背景。

This skill is ready for commercial/non-commercial use.

## Publisher:

[hoovaycn](https://clawhub.ai/user/hoovaycn)

### License/Terms of Use:

MIT-0

## Use Case:

External users and students use this skill to ask about the CUC yoga course pose catalog, including pose matching, step-by-step practice guidance, exam-relevant cues, Sanskrit names, and origin stories.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The package includes and uses a plaintext shared NocoDB token with unclear privileges.

Mitigation: Rotate the exposed token, remove it from the artifact, and require a user-provided or restricted read-only credential before deployment.

Risk: The skill provides yoga pose guidance without explicit safety qualifications or injury-screening guidance.

Mitigation: Add basic safety language advising users to avoid painful movements, account for injuries or medical conditions, and consult a qualified instructor or clinician when appropriate.

Risk: The skill contacts an external NocoDB service during normal use.

Mitigation: Review the external service endpoint, data access scope, credential handling, and network policy before installing in restricted environments.

## Reference(s):

- [Skill reference: poses.md](artifact/references/poses.md)
- [ClawHub skill page](https://clawhub.ai/hoovaycn/skills/yoga-pose-cuc)
- [Publisher profile](https://clawhub.ai/user/hoovaycn)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, guidance]

**Output Format:** [Markdown text with optional shell command execution for data retrieval]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Responses are generated from an 11-pose yoga knowledge base and may include pose steps, key points, target muscles, exam tips, Sanskrit names, origin stories, and image-link notes.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
