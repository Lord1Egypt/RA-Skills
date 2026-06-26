## Description: <br>
AI product-management coaching agent that uses guided dialogue to help PMs move from pain-point analysis through AI suitability, capability boundaries, confidence handling, hallucination planning, and PRD output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fbz1234](https://clawhub.ai/user/fbz1234) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Product managers and AI product teams use this skill to structure early AI product design conversations, evaluate whether AI is appropriate, define human decision points, and produce PRD-style summaries for review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad trigger phrases such as AI product, product design, PRD, capability boundary, confidence, hallucination, or continue may invoke the skill during ordinary product-management discussions. <br>
Mitigation: Use explicit invocation context and disable or avoid the skill when the conversation should not enter AI product-design coaching. <br>
Risk: Product plans, customer data, credentials, or regulated business details may be sensitive if pasted into the coaching conversation. <br>
Mitigation: Do not provide confidential or regulated information unless the workspace policy allows that data to be used with the agent. <br>
Risk: Coaching outputs and generated PRD sections may be treated as final decisions even though the skill is designed to guide user judgment. <br>
Mitigation: Have the product owner review and confirm assumptions, risk thresholds, responsibility boundaries, and PRD content before implementation. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/fbz1234/xxjdjdnene) <br>
- [AI PM Coach README](artifact/README.md) <br>
- [AI PM Coach architecture](artifact/ARCHITECTURE.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Analysis, Guidance] <br>
**Output Format:** [Conversational text and Markdown PRD-style summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires user confirmation at decision checkpoints; does not execute commands or access external systems.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
