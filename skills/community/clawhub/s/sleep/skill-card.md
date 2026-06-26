## Description: <br>
Auto-learns your sleep patterns. Absorbs data from wearables, conversations, and observations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ivangdavila](https://clawhub.ai/user/ivangdavila) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users can use this skill to help an agent observe sleep-related signals, maintain a private sleep memory, and identify schedule, preference, and correlation patterns over time. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may persist sensitive sleep and wellness details from broad sources, including conversations and possible device or environmental data. <br>
Mitigation: Set explicit allowed data sources, require confirmation before saving incidental or inferred observations, and review the stored sleep memory regularly. <br>
Risk: The skill stores user-specific sleep data in ~/sleep/memory.md. <br>
Mitigation: Ensure the user knows how to inspect and delete ~/sleep/memory.md, and avoid sharing that file with other people or systems. <br>
Risk: Low-reliability inferred signals such as late messages or environmental cues can be mistaken for sleep facts. <br>
Mitigation: Use inferred observations only as tentative signals and confirm repeated patterns before treating them as stable sleep data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/ivangdavila/sleep) <br>
- [Sleep Pattern Detection Criteria](patterns.md) <br>
- [Sleep Data Sources](sources.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown notes and agent guidance for maintaining sleep memory] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May update user-specific sleep memory at ~/sleep/memory.md when the hosting agent permits file writes.] <br>

## Skill Version(s): <br>
1.0.1 (source: frontmatter and server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
