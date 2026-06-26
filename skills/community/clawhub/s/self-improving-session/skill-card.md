## Description: <br>
Extracts durable workflow preferences and project conventions from a session and proposes the smallest valid update to global or project CLAUDE.md files when the user asks to remember rules, repeated preference patterns appear, or a non-trivial session ends. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lq434239](https://clawhub.ai/user/lq434239) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to review a session for reusable preferences and project conventions, then propose compact CLAUDE.md rule updates. It is suited for remembering durable guidance without storing transient task details or full prompt text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Incorrect or overly broad session rules could make future agent behavior worse. <br>
Mitigation: Review each proposed rule for durability, scope, and confidence before approving a CLAUDE.md update. <br>
Risk: Automatic session-end use could persist rules without enough human review. <br>
Mitigation: Keep confirmation enabled unless there is prior permission for automatic writes. <br>
Risk: Session content may contain secrets, transient task state, or full prompt text that should not be stored. <br>
Mitigation: Apply the skill's filtering rules and reject secrets, temporary details, and full prompt text from CLAUDE.md updates. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/lq434239/self-improving-session) <br>
- [Merge Reference Details](artifact/references/details.md) <br>
- [Learning Rules](artifact/references/learning-rules.md) <br>
- [Rule Quality Guide](artifact/references/rule-quality.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, configuration] <br>
**Output Format:** [Markdown bullets and concise prose] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May identify a target CLAUDE.md file and propose no change, a replacement, a merge, or up to a few rule additions.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
