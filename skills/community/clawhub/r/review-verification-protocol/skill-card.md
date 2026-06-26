## Description: <br>
Mandatory verification steps for all code reviews to reduce false positives. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[anderskev](https://clawhub.ai/user/anderskev) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and code review agents use this skill to verify review findings against current source artifacts before reporting them, reducing false positives and improving severity calibration. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill asks agents to quote exact source lines or diff hunks when validating findings, which can expose sensitive private code in shared conversations. <br>
Mitigation: Use normal care when applying the protocol to private repositories, and avoid sharing quoted proprietary code outside approved review channels. <br>
Risk: Review findings can still be incorrect if the agent skips the required read, reference, mitigation, or claim gates. <br>
Mitigation: Require same-turn artifact echoes and concrete file-line anchors before accepting actionable review findings. <br>


## Reference(s): <br>
- [Review Verification Protocol on ClawHub](https://clawhub.ai/anderskev/review-verification-protocol) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown] <br>
**Output Format:** [Markdown instructions and review checklist guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [No tool execution, external API calls, credential use, or generated files are described by the skill artifact.] <br>

## Skill Version(s): <br>
1.0.20 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
