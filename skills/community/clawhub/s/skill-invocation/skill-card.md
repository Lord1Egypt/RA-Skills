## Description: <br>
Choose the best OpenClaw skill by matching trigger keywords to the TOOLS.md index, then applying strict judgment rules (most specific first; if in doubt, use it). <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[xuchang9337-dev](https://clawhub.ai/user/xuchang9337-dev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent orchestrators use this skill to select one or more OpenClaw skills for a user request by matching trigger keywords against a TOOLS.md index and applying the documented specificity rules. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The permissive fallback rule may lead an agent to select an unsuitable skill when the TOOLS.md index is incomplete or ambiguous. <br>
Mitigation: Require clarification or human confirmation before invoking selected skills for high-impact actions such as editing files, publishing content, deploying code, or affecting accounts. <br>
Risk: Skill selection depends on a TOOLS.md index whose trigger mappings may become stale. <br>
Mitigation: Maintain the TOOLS.md index alongside installed skill changes and review selected skills before execution in sensitive workflows. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/xuchang9337-dev/skill-invocation) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with recommended decision fields] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Recommended output includes selected skills, selection reason, and next action.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
