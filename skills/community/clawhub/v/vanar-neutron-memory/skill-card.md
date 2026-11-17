## Description:

Save and recall agent memory with semantic search. Context that persists across every session.

This skill is ready for commercial/non-commercial use.

## Publisher:

[naeemmaliki036](https://clawhub.ai/user/naeemmaliki036)

### License/Terms of Use:


## Use Case:

Developers and agent users use this skill to save selected conversation context to the Neutron service and recall semantically relevant memories across sessions. Optional hooks can automatically capture conversation turns and inject recalled context when explicitly enabled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved text, search queries, and opt-in conversation turns may be sent to and stored by the remote Neutron service.

Mitigation: Use the skill only for projects where remote memory storage is acceptable, avoid sensitive content, and leave VANAR_AUTO_CAPTURE and VANAR_AUTO_RECALL disabled for sensitive work.

Risk: Recalled remote memories can be injected into the agent context with limited safeguards.

Mitigation: Review recalled memory content before relying on it for important decisions or actions.

Risk: Plaintext credentials files and an untrusted NEUTRON_API_BASE can expose API keys or redirect memory traffic.

Mitigation: Prefer a service-specific NEUTRON_API_KEY environment variable, lock down any credentials file permissions, and keep NEUTRON_API_BASE unset unless the endpoint is trusted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/naeemmaliki036/skills/vanar-neutron-memory)
- [Publisher profile](https://clawhub.ai/user/naeemmaliki036)
- [OpenClaw dashboard and API keys](https://openclaw.vanarchain.com/)
- [Setup Guide](artifact/SETUP.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with inline shell commands and JSON API responses from the CLI]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Manual save/search commands require curl, jq, and an API key; opt-in hooks may print recalled memory text into agent context.]

## Skill Version(s):

1.3.2 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
