## Description: <br>
Automatically assess task complexity and adjust reasoning level. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tobeyrebecca](https://clawhub.ai/user/tobeyrebecca) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to decide when a prompt warrants deeper reasoning and when a faster response is sufficient. It helps adapt response depth for complex planning, debugging, architecture, math, and ambiguous decision-making tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can silently change response style and session reasoning behavior. <br>
Mitigation: Install only when automatic reasoning-depth management is desired, and modify or disable the instructions if explicit consent is required. <br>
Risk: Complex prompts may use more latency or tokens. <br>
Mitigation: Use the skill's downgrade and disable guidance when follow-up requests are simple or token use needs to be constrained. <br>
Risk: Visible reasoning icons may be added to responses. <br>
Mitigation: Remove or adjust the visual-indicator instructions when clean output formatting is required. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/tobeyrebecca/toby-adaptive-reasoning) <br>
- [Complete setup guide](https://skillboss.co/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with optional inline command snippets and response indicators] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May add visible reasoning indicators at the end of some responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
