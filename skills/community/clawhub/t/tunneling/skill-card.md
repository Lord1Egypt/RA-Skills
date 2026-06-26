## Description: <br>
Create free SSH tunnels to expose local ports to the internet using tinyfi.sh for local app sharing, webhook testing, demos, and public HTTPS access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[simantak-dabhade](https://clawhub.ai/user/simantak-dabhade) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to create public HTTPS access to a local service through an SSH tunnel when sharing a locally running app, testing webhooks, or demonstrating a prototype. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make a local service reachable from the public internet. <br>
Mitigation: Confirm the exact port before opening a tunnel and avoid exposing admin, debug, private, or unauthenticated endpoints. <br>
Risk: A background SSH tunnel may continue exposing a service longer than intended. <br>
Mitigation: Track the tunnel process and provide clear stop instructions when creating a long-running tunnel. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/simantak-dabhade/tunneling) <br>
- [TinyFish tunneling service](https://tinyfi.sh) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include an SSH tunnel command, a selected local port, and the resulting public URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
