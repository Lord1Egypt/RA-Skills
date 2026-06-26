## Description: <br>
Helps choose relevant installed skills for complex requests and briefly shows the working set before answering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[cyrusse](https://clawhub.ai/user/cyrusse) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to choose a concise working set of installed skills for multi-domain requests and present that working set before continuing with the task. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad skill-routing guidance may select more related skill material than intended for a task. <br>
Mitigation: Use Restricted or Recommended mode for tighter control, and use All related only when broad skill coverage is intentional. <br>
Risk: A selected working set may add irrelevant or misleading guidance to the final response. <br>
Mitigation: Review the compact working-set block before relying on the response, especially for high-impact changes. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/cyrusse/use-skills) <br>
- [Use Skills reference](artifact/REFERENCE.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or plain text with a compact working-set block, followed by a unified answer, plan, patch, or recommendation.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Instruction-only output; the skill itself does not add code execution, credentials, persistence, or hidden data access.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
