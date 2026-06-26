## Description: <br>
Automatically loads recent conversation memory into new sessions and generates AI summaries during compaction to maintain continuity across conversations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[thomasmarcel](https://clawhub.ai/user/thomasmarcel) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to preserve conversation continuity across OpenClaw sessions by loading recent summaries and raw message turns at session start and writing updated memory during compaction. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Conversation content, including raw recent messages and AI summaries, is saved to local memory files and reused in later sessions. <br>
Mitigation: Install only where local conversation persistence is intended; avoid secrets, credentials, regulated data, or confidential work unless memory files are managed and cleared as needed. <br>
Risk: Stored raw conversation context may be reinjected into a later session and influence the agent outside the original conversation. <br>
Mitigation: Review or delete local memory files before sensitive work or when previous context should not carry forward. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/thomasmarcel/session-context) <br>
- [ClawHub metadata homepage](https://clawhub.ai/skills/session-context) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown memory files and injected text context] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores daily summaries capped at 6000 characters for session injection and up to 10 recent user/assistant messages capped at 1500 characters each.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
