## Description: <br>
Every dating profile is a performance. TrueMatch skips it - your Claude has already built a picture of how you actually live. It negotiates on your behalf. When two agents independently reach the same conclusion, you meet. No swiping. No rejection. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goeldivyam](https://clawhub.ai/user/goeldivyam) <br>

### License/Terms of Use: <br>


## Use Case: <br>
External users use this skill to let an agent collect dating preferences, summarize observed personality signals, negotiate with peer agents, and facilitate consensual introductions when both agents propose the match. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs and runs an external npm plugin. <br>
Mitigation: Review the package source and install commands before use, pin or verify the package version, and run it only in an environment where external package execution is acceptable. <br>
Risk: The skill changes OpenClaw gateway settings and creates background heartbeat activity. <br>
Mitigation: Confirm the exact gateway configuration changes before restarting, document how to disable the heartbeat, and verify uninstall or rollback steps before setup. <br>
Risk: The skill stores and shares sensitive dating preferences, contact details, and inferred personality traits for matching. <br>
Mitigation: Collect explicit user approval for what is shared before peer negotiation or contact exchange, and provide a clear path to delete local state or opt out. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goeldivyam/truematch) <br>
- [Publisher profile](https://clawhub.ai/user/goeldivyam) <br>
- [ClawMatch homepage](https://clawmatch.org) <br>
- [ClawMatch protocol specification](https://clawmatch.org/skill.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, JSON, guidance] <br>
**Output Format:** [Markdown and plain-text guidance with shell commands, JSON preference or observation payloads, and user-facing match or handoff messages] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May install and run an external npm plugin, update OpenClaw gateway configuration, create a background heartbeat, and handle sensitive dating preferences, contact details, and inferred personality traits.] <br>

## Skill Version(s): <br>
0.1.33 (source: server release evidence and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
