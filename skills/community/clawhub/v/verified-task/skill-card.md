## Description: <br>
Enforce correctness before execution. Verify any task output and only proceed if it passes--override requires explicit operator approval. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[nutstrut](https://clawhub.ai/user/nutstrut) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents, operators, and workflow developers use this skill to add a PASS, FAIL, or INDETERMINATE verification gate before high-impact actions such as payments, content publishing, message sending, or autonomous workflow continuation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The verification gate can stop or delay workflows when outputs fail review or the result is indeterminate. <br>
Mitigation: Define acceptance criteria before generation and require an explicit human operator override before continuing after a non-PASS verdict. <br>
Risk: Optional external verification can expose sensitive task details if unnecessary data is sent outside the local workflow. <br>
Mitigation: Keep local verification as the primary decision layer, send only minimum structured data, and avoid secrets or sensitive content in any optional external verification step. <br>


## Reference(s): <br>
- [OpenClaw Integration Notes](references/openclaw-integration.md) <br>
- [Decision Template](assets/DECISION-TEMPLATE.md) <br>
- [Use Case Examples](assets/USE-CASE-EXAMPLES.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown guidance and JSON-compatible verification records] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces verdict-oriented review guidance with PASS, FAIL, or INDETERMINATE outcomes.] <br>

## Skill Version(s): <br>
1.0.7 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
