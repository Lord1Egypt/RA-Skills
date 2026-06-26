## Description: <br>
Track rules, guidelines, and constraints for triggering, compliance, and violations, then generate compliance reports after tasks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[renyuan000](https://clawhub.ai/user/renyuan000) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, learners, and agent users can use this skill to review how well an agent follows task rules, coding guidelines, and safety constraints, then identify frequent violations and improvement opportunities. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks the agent to maintain local memory and may generate reports automatically at task completion, heartbeat, or user-requested trigger points. <br>
Mitigation: Install it only when ongoing local tracking is wanted, restrict writable files, approve autonomous behavior explicitly, and review stored memory for sensitive information. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown reports with rule tables, compliance metrics, diagnosis notes, and local memory file guidance.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local daily memory files named memory/rules-tracker-{YYYY-MM-DD}.json.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
