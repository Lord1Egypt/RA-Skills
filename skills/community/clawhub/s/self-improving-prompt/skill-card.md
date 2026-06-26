## Description: <br>
Refines ambiguous or high-risk user requests before execution. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lq434239](https://clawhub.ai/user/lq434239) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, operators, and agent users use this skill to decide when ambiguous or high-risk requests should be refined, compared with the original, clarified, or executed directly. It helps reduce rework by adding clearer scope, output expectations, and acceptance criteria only when refinement materially improves execution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may add clarification or compare-first prompts when a request is vague or high risk. <br>
Mitigation: Apply the documented trigger threshold and substantial-value test so clear single-step or already well-scoped tasks execute directly. <br>
Risk: When paired with a session-learning skill, workflow preference signals could be over-collected or too specific. <br>
Mitigation: Record only abstract event labels such as choice outcomes, never full prompt text or task-specific details. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lq434239/self-improving-prompt) <br>
- [Decision Matrix](references/decision-matrix.md) <br>
- [Reference Details](references/details.md) <br>
- [Non-Examples](references/non-examples.md) <br>
- [Prompt Refinement Patterns](references/prompt-patterns.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance] <br>
**Output Format:** [Markdown or concise chat text] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May produce a refined prompt, direct execution guidance, a compare-first choice, or a minimal abstract preference event label.] <br>

## Skill Version(s): <br>
1.0.3 (source: server-resolved release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
