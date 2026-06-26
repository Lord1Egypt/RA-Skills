## Description: <br>
Socrates helps agents run a concise Socratic self-Q&A before planning, coding, refactoring, or delegation to clarify goals, assumptions, risks, approach, and next actions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Hongyi3](https://clawhub.ai/user/Hongyi3) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, agents, and reviewers use Socrates to pressure-test non-trivial plans, coding changes, refactors, and delegation boundaries before execution while keeping the reasoning brief and action-oriented. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Use in sensitive maintenance or production-adjacent workflows could authorize actions that need human review. <br>
Mitigation: Review commands and proposed actions before allowing moderation, publishing, production Convex, or full-access autoreview steps, and use documented opt-outs or confirmation steps in sensitive environments. <br>


## Reference(s): <br>
- [Socrates Protocol](references/protocol.md) <br>
- [Socrates Examples](references/examples.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/Hongyi3/socrates) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown sections with concise bullet points and numbered action plans] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include a Delegation Contract only when sub-agents are involved.] <br>

## Skill Version(s): <br>
0.1.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
