## Description:

Create free SSH tunnels to expose local ports to the internet using tinyfi.sh.

This skill is ready for commercial/non-commercial use.

## Publisher:

[simantak-dabhade](https://clawhub.ai/user/simantak-dabhade)

### License/Terms of Use:


## Use Case:

Developers and engineers use this skill to expose a local web app or service through a temporary public HTTPS URL for webhook testing, prototype demos, or short-term sharing.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The tunnel can make a local service publicly reachable on the internet.

Mitigation: Use it only for non-sensitive local apps that are safe to publish, and avoid databases, admin consoles, debug ports, or services containing secrets.

Risk: A public tunnel can remain available longer than intended while the SSH session is alive.

Mitigation: Stop the SSH process as soon as sharing or testing is finished.

Risk: Unauthenticated local services may be accessed by unintended users through the public URL.

Mitigation: Add authentication or access restrictions around anything exposed through the tunnel.

## Reference(s):

- [Tunneling skill page](https://clawhub.ai/simantak-dabhade/skills/tunneling)

## Skill Output:

**Output Type(s):** [Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown with inline bash code blocks]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes SSH tunnel commands, port-selection guidance, public URL reporting guidance, common local ports, and TinyFish service limits.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
