## Description:

三峰智能 uses the Sufn smart-home open platform to log in, switch homes, sync devices, query device status, control supported switches, lights, curtains, and air conditioners, and run existing scenes.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lingguyuan](https://clawhub.ai/user/lingguyuan)

### License/Terms of Use:

MIT-0

## Use Case:

External smart-home users use this skill to manage supported 三峰 devices through natural-language requests after authenticating with their account. It supports home switching, synchronization, state queries, device control, and execution of existing scenes, but not scene creation or editing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The request helper can send an authentication token to a caller-controlled URL path.

Mitigation: Review before installing and restrict helper calls to the five documented platform paths before using an active account token.

Risk: The skill controls real smart-home devices and can affect the user's physical environment.

Mitigation: Require an authenticated session, uniquely match devices or scenes before acting, and only confirm completion after the platform reports success.

Risk: Smart-home credentials and tokens are sensitive.

Mitigation: Use encrypted local token storage, avoid logging or disclosing credentials or tokens, and require re-login if protected state cannot be decrypted.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/lingguyuan/skills/sufn-smart-home)
- [API reference](artifact/references/api-reference.md)
- [Control mappings](artifact/references/control-mappings.md)
- [Device capabilities](artifact/references/device-capabilities.md)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration, guidance]

**Output Format:** [Natural-language user replies with PowerShell execution guidance and local state configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Controls real smart-home devices and must avoid disclosing tokens, internal identifiers, request details, raw responses, logs, or local state.]

## Skill Version(s):

1.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
