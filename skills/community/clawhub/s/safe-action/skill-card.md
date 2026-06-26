## Description: <br>
Before any destructive or irreversible action, run a safety pre-flight to check risks, reversibility, and timing. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[CutTheMustard](https://clawhub.ai/user/CutTheMustard) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agents use this skill before destructive, irreversible, high-stakes, or production-impacting actions to synthesize safety, reversibility, and timing checks into a proceed-or-pause recommendation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends brief action descriptions, platform names, and timezone information to external AgentUtil services. <br>
Mitigation: Keep descriptions minimal and omit secrets, credentials, customer data, private document contents, and detailed internal identifiers. <br>
Risk: A full pre-flight may incur small x402 charges for paid checks. <br>
Mitigation: Use free discovery endpoints when exploring and confirm cost acceptance before running paid checks. <br>
Risk: The skill can recommend pausing or proceeding, but the underlying action may still be destructive or irreversible. <br>
Mitigation: Require explicit user approval before high-risk, irreversible, or time-sensitive actions and prefer safer alternatives when available. <br>


## Reference(s): <br>
- [Safe Action on ClawHub](https://clawhub.ai/CutTheMustard/safe-action) <br>
- [AgentUtil](https://agentutil.net) <br>
- [AgentUtil Think check endpoint](https://think.agentutil.net/v1/check) <br>
- [AgentUtil Undo check endpoint](https://undo.agentutil.net/v1/check) <br>
- [AgentUtil Context check endpoint](https://context.agentutil.net/v1/check) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, shell commands] <br>
**Output Format:** [Markdown guidance with risk summaries, recommendations, and optional inline API call examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include risk levels, reversibility status, timing context, safer alternatives, and explicit-confirmation prompts.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata; artifact frontmatter is 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
