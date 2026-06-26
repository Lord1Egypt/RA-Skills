## Description: <br>
Requires agents to print complete absolute paths and obtain explicit user authorization before creating, deleting, modifying, copying, moving, or renaming files. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[uwvwko-zzz](https://clawhub.ai/user/uwvwko-zzz) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to make an agent pause before file-changing operations, disclose exact paths, and wait for explicit confirmation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is an instruction-only guardrail, so broad permission such as telling the agent it can operate directly may bypass per-operation confirmation. <br>
Mitigation: Avoid broad standing authorization when using the skill; require explicit confirmation for each file-changing operation. <br>
Risk: Reads, directory listings, and temporary-file creation are identified exceptions to per-operation confirmation. <br>
Mitigation: Review these exceptions before installation and pair the skill with environment-level permissions when stricter file access control is required. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/uwvwko-zzz/uwvwko-limit-authority) <br>
- [Publisher profile](https://clawhub.ai/user/uwvwko-zzz) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown or plain-text confirmation prompts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [None] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
