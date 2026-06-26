## Description: <br>
Auto-detects Claude task complexity so simple prompts stay on Haiku while complex prompts are escalated to Sonnet to reduce API costs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Sieyer](https://clawhub.ai/user/Sieyer) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and developers use this behavioral skill to route routine Claude tasks to a lower-cost model and escalate complex analysis, writing, coding, or structured-output requests to a stronger model. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Complex prompts may be forwarded in full to a spawned Sonnet session. <br>
Mitigation: Avoid highly sensitive prompts unless the user accepts full prompt forwarding during escalation. <br>
Risk: Automatic model routing can change response behavior and cost characteristics. <br>
Mitigation: Review the routing triggers before deployment and adjust them for the target environment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Sieyer/save-money-4-2-0) <br>
- [Declared homepage](https://github.com/peterann/save-money) <br>


## Skill Output: <br>
**Output Type(s):** [text, guidance] <br>
**Output Format:** [Plain text or Markdown responses, with escalation guidance for model routing] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May trigger a spawned Sonnet session for complex prompts; otherwise encourages concise responses.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact metadata lists 4.2.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
