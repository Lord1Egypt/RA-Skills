## Description: <br>
Builds and updates a local user profile from conversation insights, then uses that profile to personalize responses and recommend future conversation topics. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chasezxs](https://clawhub.ai/user/chasezxs) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users and agent operators use this skill to maintain a persistent local profile of user interests, preferences, communication style, and conversation history so future conversations can be personalized and topic suggestions can be generated. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill persistently profiles the user from conversations, including interests, preferences, habits, and communication style. <br>
Mitigation: Install only when persistent personalization is intended, and regularly review, delete, or reset the local profile files under ~/.openclaw/workspace/memory. <br>
Risk: The skill includes proactive topic exploration and engagement-probing behavior that may feel intrusive if enabled unintentionally. <br>
Mitigation: Use proactive or scheduled exploration only with explicit opt-in, and honor user requests to stop collecting information, forget topics, disable proactive outreach, or reset the profile. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/chasezxs/user-insight) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, JSON, Files, Shell commands] <br>
**Output Format:** [Markdown guidance and JSON profile or topic recommendation data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses local profile and topic exploration files under ~/.openclaw/workspace/memory when the helper scripts are run.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
