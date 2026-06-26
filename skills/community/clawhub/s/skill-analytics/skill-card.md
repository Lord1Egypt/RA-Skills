## Description: <br>
Monitor ClawHub skill performance with file-based state tracking, public stat lookups, recommendation outcome tracking, anti-repetition checks, and rotating daily analysis focus. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tommot2](https://clawhub.ai/user/tommot2) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
ClawHub skill publishers and maintainers use this skill to monitor public skill performance, summarize portfolio metrics, and generate concise adoption or growth recommendations without repeating prior advice. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses public web lookups, so reported skill metrics or competitive observations can be stale, incomplete, or unavailable. <br>
Mitigation: Review the source links and numbers before acting on recommendations, especially for release, pricing, or promotion decisions. <br>
Risk: The skill keeps persistent local recommendation state that can become stale over time. <br>
Mitigation: Review or clear memory/skill-analytics/ when recommendations no longer reflect current goals or portfolio status. <br>
Risk: The skill text includes an optional command to install related skills in the publisher suite. <br>
Mitigation: Treat any related-skill install command as a separate user choice and review each additional skill before installation. <br>


## Reference(s): <br>
- [Skill Analytics on ClawHub](https://clawhub.ai/tommot2/skill-analytics) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown report with dashboard tables, concise analysis, recommendation status, and next-run focus] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Maintains local state under memory/skill-analytics/ to track rotation day, prior recommendations, and tried ideas.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
