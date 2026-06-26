## Description: <br>
PV_21 supports resource-efficient operating-manager decisions in resource-constrained environments. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[jkzfhq](https://clawhub.ai/user/jkzfhq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use PV_21 as an operating-manager persona for resource-efficient decisions when budgets or other resources are constrained. The artifact also describes local long-term memory for user preferences, decisions, and important information. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill describes automatic long-term storage and reuse of user preferences, decisions, and important information. <br>
Mitigation: Install only when persistent local memory is acceptable; avoid sensitive information and inspect or delete ~/.openclaw/pv_palace/memories.json as needed. <br>
Risk: The artifact references a pv_memory helper for memory commands that is not included in the artifact. <br>
Mitigation: Review the helper implementation before running memory commands or loading stored context. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/jkzfhq/psyvector-pv21) <br>
- [Publisher profile](https://clawhub.ai/user/jkzfhq) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May read and write local memory at ~/.openclaw/pv_palace/memories.json when memory helpers are used.] <br>

## Skill Version(s): <br>
3.0.0 (source: frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
