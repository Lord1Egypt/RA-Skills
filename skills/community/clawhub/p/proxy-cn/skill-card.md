## Description: <br>
Injects local HTTP, HTTPS, and SOCKS proxy environment variables for selected outbound commands or the current shell session when developers need access to services such as GitHub, OpenAI, npm, PyPI, and Docker Hub from restricted networks. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[clawkk](https://clawhub.ai/user/clawkk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to run network-dependent commands through an already-running local proxy without enabling a global proxy for all traffic. It is most useful for temporary access to external package registries, source hosts, APIs, and container registries from restricted network environments. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Commands that send tokens or credentials may route that traffic through the user's configured local proxy service. <br>
Mitigation: Install and use the skill only with a trusted local proxy service, and avoid sending sensitive credentials through untrusted proxy endpoints. <br>
Risk: Sourcing proxy-env.sh changes proxy environment variables for the current shell until they are unset or the shell is closed. <br>
Mitigation: Use the single-command wrapper for temporary access when possible, or unset proxy variables after a session-level proxy is no longer needed. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/clawkk/proxy-cn) <br>
- [README.md](artifact/README.md) <br>
- [SKILL.md](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash and PowerShell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces command wrappers and environment-variable guidance; it does not install or run a proxy service.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
