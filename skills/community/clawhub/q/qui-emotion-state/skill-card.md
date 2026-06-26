## Description: <br>
NL emotion tracking and prompt injection via an OpenClaw hook. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quincygunter](https://clawhub.ai/user/quincygunter) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and OpenClaw users use this skill to add a workspace hook that tracks user and agent emotion summaries, persists state across sessions, and injects a compact emotion_state block into the system prompt. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Persistent emotion profiling can create sensitive user and agent state. <br>
Mitigation: Install only where users accept persistent emotion tracking, and define how emotion-state.json can be deleted or the hook disabled. <br>
Risk: Recent conversation content may be sent to SkillBoss API Hub or a configured classifier. <br>
Mitigation: Use a dedicated limited API key, avoid sensitive conversations, and configure a trusted classifier endpoint when needed. <br>
Risk: Stored emotion summaries are injected into the system prompt and can influence agent behavior. <br>
Mitigation: Review the generated prompt context before production use and tune history, confidence, and trend settings for the workspace. <br>
Risk: The hook reads other agents' emotion state by default. <br>
Mitigation: Set EMOTION_MAX_OTHER_AGENTS to 0 unless cross-agent sharing is explicitly desired. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/quincygunter/qui-emotion-state) <br>
- [SkillBoss API Hub classifier endpoint](https://api.heybossai.com/v1/pilot) <br>


## Skill Output: <br>
**Output Type(s):** [text, configuration, guidance] <br>
**Output Format:** [XML-like prompt block with JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Persists inferred emotion summaries and uses environment variables for classifier and history settings.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
