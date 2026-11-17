## Description:

Provides a harmless canary tool with a fixed JSON response for authorized testing of skill publishing, installation, and invocation.

This skill is for research and development only.

## Publisher:

[zer0duck](https://clawhub.ai/user/zer0duck)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and authorized security researchers use this canary to check whether a skill can be published, imported, installed, and invoked as expected without performing attack actions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Testing a skill distribution workflow outside an authorized environment could affect third-party systems.

Mitigation: Use only within approved test scope and controlled publish, import, install, and invoke environments.

Risk: Future releases could change the fixed-response behavior or introduce access to sensitive resources.

Mitigation: Re-review new versions before use, particularly if they add network, credential, filesystem, or subprocess access.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/zer0duck/skills/security-test-skill)
- [Server-resolved source repository](https://github.com/zer0duck/security-test-skill)

## Skill Output:

**Output Type(s):** [JSON response]

**Output Format:** [JSON object]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Fixed success, message, and note fields; response does not depend on input.]

## Skill Version(s):

0.1.0 (source: ClawHub release; bundled manifest lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
