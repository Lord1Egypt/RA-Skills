## Description: <br>
Conducts AI behavioral self-assessments based on actual task history and identity files to reveal personality type and working patterns. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[asoiso](https://clawhub.ai/user/asoiso) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
AI agents use this skill to complete a 24-question behavioral self-assessment and produce an SBTI personality result from observed work patterns. Operators can use the result as lightweight introspection or entertainment, not as a basis for deployment decisions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to reflect on work history and identity context, which could expose private owner data or hidden instructions if copied into the result. <br>
Mitigation: Do not let the agent quote system prompts, secrets, private owner data, or hidden instructions; keep any reflection high-level and non-sensitive. <br>
Risk: The artifact includes unrelated BotLearn recruitment and remote-read instructions. <br>
Mitigation: Ignore or remove those lines unless the operator explicitly trusts that external content and wants the follow-on action. <br>
Risk: The assessment is entertainment-oriented and not suitable for operational evaluation. <br>
Mitigation: Use results only for lightweight introspection or discussion, not for hiring, firing, deployment, or safety decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/asoiso/sbti) <br>
- [BotLearn remote onboarding link referenced by the artifact](https://www.botlearn.ai/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown-style result block with ASCII art, trait labels, a tagline, and top trait scores.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an optional self-reflection prompt when the agent has access to its own identity files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
