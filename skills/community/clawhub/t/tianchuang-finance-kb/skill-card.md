## Description: <br>
Provides strict verbatim retrieval from Tianchuang Finance policy documents, returning matching Chinese excerpts or "无" without summaries or reinterpretation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Jizhidemu52](https://clawhub.ai/user/Jizhidemu52) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Employees, agents, and finance-policy users use this skill to answer Tianchuang Finance policy questions by retrieving exact Chinese excerpts from the configured document corpus. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generic finance terms may trigger the skill more often than users expect. <br>
Mitigation: Review retrieved output in context and disable or narrow triggers if broad activation interferes with other finance workflows. <br>
Risk: Returned excerpts may be outdated or unauthorized if the referenced Tianchuang PDF corpus is not current and approved. <br>
Mitigation: Verify the corpus authorization and currency before treating excerpts as official policy. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Jizhidemu52/tianchuang-finance-kb) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>
- [config.json](artifact/config.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text Chinese excerpts or "无"] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Multiple matches are separated by newlines; output should not include summaries, explanations, headers, or rewritten text.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
