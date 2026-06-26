## Description: <br>
中国传媒大学瑜伽精品课（赵晓琳老师）瑜伽体式知识库，帮助用户查询瑜伽体式名称、步骤、要点、目标肌肉、考试提示和文化背景。 <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[hoovaycn](https://clawhub.ai/user/hoovaycn) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and students use this skill to ask about CUC yoga course poses, including pose lookup, difficulty, movement steps, practice points, target muscles, exam tips, Sanskrit names, and origin stories. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires a remote NocoDB query to answer pose questions. <br>
Mitigation: Disclose the external service before installation and allow deployment only where outbound access to that service is approved. <br>
Risk: The artifact includes an embedded reusable database token. <br>
Mitigation: Remove or rotate the bundled token and require operators to provide a scoped token through NOCODB_XC_TOKEN. <br>
Risk: The query retrieves up to 100 records from the configured table and view. <br>
Mitigation: Narrow the table, view, token permissions, and query scope to only the pose records needed for the skill. <br>


## Reference(s): <br>
- [瑜伽体式知识参考（CUC赵晓琳老师瑜伽精品课）](references/poses.md) <br>
- [ClawHub skill page](https://clawhub.ai/hoovaycn/yoga-pose-cuc) <br>
- [External NocoDB API endpoint used by the skill](https://nocodb.dixchain.com/api/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, API Calls, Shell commands, Guidance] <br>
**Output Format:** [Markdown prose backed by JSON records returned from a shell query] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses may include pose names, Sanskrit names, classifications, steps, key points, target muscles, exam tips, origin stories, and image-link notices when present in the source data.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
