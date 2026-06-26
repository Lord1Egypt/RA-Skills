## Description: <br>
Create new skills, modify and improve existing skills, and measure skill performance. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Shimmernight](https://clawhub.ai/user/Shimmernight) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent builders use this skill to draft new skills, update existing skills, run evaluation workflows, compare skill performance, and optimize skill descriptions for better triggering. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can run local Python and shell workflows, spawn evaluation agents, call Claude or Anthropic tooling, and write review artifacts. <br>
Mitigation: Review planned commands before execution and run the skill only in workspaces where those local actions are acceptable. <br>
Risk: The local review viewer can terminate other local processes or conflict with occupied ports. <br>
Mitigation: Use static viewer mode for sensitive reviews, avoid occupied ports, and stop any background viewer after review. <br>
Risk: The CDN-backed viewer can load third-party scripts into pages containing evaluation outputs. <br>
Mitigation: Avoid embedding confidential outputs in the CDN-backed viewer unless that external dependency is acceptable. <br>


## Reference(s): <br>
- [Skill Creator Schema Reference](references/schemas.md) <br>
- [ClawHub skill page](https://clawhub.ai/Shimmernight/skill-creator-latest) <br>
- [Publisher profile](https://clawhub.ai/user/Shimmernight) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with JSON examples, shell commands, and generated skill files or review artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce skill packages, evaluation workspaces, benchmark reports, HTML review pages, and optimized skill descriptions.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
