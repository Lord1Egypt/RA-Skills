## Description: <br>
Soul Decision Engine Free helps agents structure decisions with domain/type memory, confidence labels, and review loops that learn user risk and framework preferences. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thcjp](https://clawhub.ai/user/thcjp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and agent operators use this skill to turn choice-heavy discussions into structured decision analyses, record outcomes in local Markdown memory, and review decisions to refine preferences over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores decision history and inferred preferences under ~/soul-decision, which can expose sensitive work or life decisions on shared machines. <br>
Mitigation: Review the local memory directory before use, avoid sensitive decision logs on shared systems, and delete or restrict access to records that should not persist. <br>
Risk: The skill can update or reuse a user preference profile from broad conversational cues without strong consent boundaries. <br>
Mitigation: Require explicit confirmation before memory writes and periodically review or remove learned preferences that should no longer influence advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thcjp/skills/soul-decision-engine-free) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and decision-record templates] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create or update local Markdown files under ~/soul-decision when the agent follows the skill.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
