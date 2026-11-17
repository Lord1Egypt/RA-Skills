## Description:

Manage agent trust scores with Bayesian updates, domain-specific trust, revocation, forgetting curves, challenge-response verification, and a local dashboard.

This skill is ready for commercial/non-commercial use.

## Publisher:

[felmonon](https://clawhub.ai/user/felmonon)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to maintain local trust graphs for agent identities, capabilities, interactions, and domain-specific reputation. It helps inspect trust status, record interactions, revoke or restore trust, and view trust data in a dashboard.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Confirmed command-injection flaws in shell=True command construction can allow unsafe command execution.

Mitigation: Do not install or run until the publisher removes shell=True command construction or uses argument lists with validated inputs.

Risk: The skillsign dependency is unpinned and can change behavior over time.

Mitigation: Pin, vendor, or otherwise verify the skillsign dependency before use.

Risk: The skill stores local trust and identity metadata under ~/.atp.

Mitigation: Treat ~/.atp as sensitive agent trust data; restrict access and avoid sharing it.

Risk: Moltbook identifiers may be accepted into trust mappings without adequate validation.

Mitigation: Validate Moltbook identifiers before linking, scoring, or scanning users and posts.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/felmonon/skills/trust-protocol)
- [skillsign integration](https://github.com/FELMONON/skillsign)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with CLI command examples and JSON trust graph data]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create or read local ~/.atp trust, interaction, challenge, and Moltbook bridge files; dashboard commands expose local trust data through localhost JSON endpoints.]

## Skill Version(s):

2.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
