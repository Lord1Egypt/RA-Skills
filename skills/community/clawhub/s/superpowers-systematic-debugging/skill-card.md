## Description: <br>
Enforces a four-phase debugging process for bugs, test failures, and unexpected behavior: root cause investigation, pattern analysis, hypothesis testing, and evidence-based fix verification. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[axelhu](https://clawhub.ai/user/axelhu) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineering agents use this skill to debug software issues methodically before proposing or applying fixes. It guides investigation, comparison with working patterns, hypothesis testing, and verification so fixes address root causes rather than symptoms. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide an agent toward repo-maintenance, Convex workflow, moderation, deployment, or nested review commands that may have high impact if executed without review. <br>
Mitigation: Review commands before execution, use documented opt-outs or confirmation steps when appropriate, and verify fixes with tests or other concrete evidence. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [guidance, text, markdown] <br>
**Output Format:** [Markdown guidance with checklists and process steps] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May lead the agent to propose tests, code changes, shell commands, or configuration checks during debugging.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
