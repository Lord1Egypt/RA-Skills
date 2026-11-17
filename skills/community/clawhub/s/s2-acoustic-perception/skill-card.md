## Description:

Captures a short microphone sample, sends it to a local edge service for acoustic event classification, and returns semantic event data with optional local linkage suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[spacesq](https://clawhub.ai/user/spacesq)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents can use this skill, with explicit user consent, to sample environmental audio and receive structured acoustic labels such as speech, music, pet sounds, glass breakage, or ambient noise. It is intended for local edge-service workflows where microphone access and follow-on smart-home or security actions are carefully controlled.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill captures microphone audio and can expose sensitive environmental or human-speech context.

Mitigation: Run it only after explicit user consent, limit use to intended zones, and avoid recording or retaining raw audio outside the local workflow.

Risk: Audio is sent to an edge service over unauthenticated HTTP.

Mitigation: Use only a trusted local service on a controlled network, add authentication or transport protection where possible, and do not route requests to public or untrusted hosts.

Risk: The skill's output may suggest camera, alarm, smart-home, or memory actions.

Mitigation: Require human review or explicit policy gates before agents trigger downstream devices, alarms, logging, or memory updates.

Risk: The source text makes strong LAN-only and memory-erasure claims that should not be treated as guarantees.

Mitigation: Review the deployment and runtime behavior directly, and document residual privacy limits before operational use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/spacesq/skills/s2-acoustic-perception)
- [S2-SP-OS homepage](https://space2.world/s2-sp-os)

## Skill Output:

**Output Type(s):** [JSON, Shell commands, Guidance]

**Output Format:** [JSON emitted by a Python command-line client]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3 with sounddevice and numpy, microphone access, explicit consent, and a local edge service IP.]

## Skill Version(s):

1.0.5 (source: server release metadata and frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
