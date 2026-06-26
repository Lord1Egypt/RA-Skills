## Description: <br>
Telegram Web platform skill for SurfAgent, covering chat state, composer flows, send verification, and when to use the Telegram Web adapter over raw browser control. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[surfagentapp](https://clawhub.ai/user/surfagentapp) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to operate Telegram Web through SurfAgent workflows, especially for chat state checks, composer handling, message extraction, draft filling, and proof-aware send verification. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: A message could be sent to the wrong Telegram chat or reported as sent before the UI confirms delivery. <br>
Mitigation: Confirm the account, target chat, intended draft text, composer state change, and visible post-send message before claiming success. <br>
Risk: Raw browser actions against Telegram Web can be brittle because the UI is dynamic and route changes occur inside the app shell. <br>
Mitigation: Prefer Telegram Web adapter state, composer, extraction, and send tools, using targeted browser control only for narrow probes with immediate verification. <br>
Risk: Third-party skills can request access to browser state or credentials during real tasks. <br>
Mitigation: Follow the security evidence guidance: review requested permissions and provide credentials or file access only when clearly needed. <br>


## Reference(s): <br>
- [SurfAgent homepage](https://surfagent.app) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown] <br>
**Output Format:** [Markdown operating guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Provides agent-facing rules for Telegram Web state checks, composer flows, adapter preference, blocker handling, and send verification.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter, skill.json, release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
