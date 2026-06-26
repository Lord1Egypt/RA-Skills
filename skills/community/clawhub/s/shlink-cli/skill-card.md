## Description: <br>
Use this skill when the user wants to install, configure, or troubleshoot the Shlink CLI from GitHub and manage short URLs, tags, visits, domains, and health checks through Shlink REST API v3. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ParinLL](https://clawhub.ai/user/ParinLL) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install and configure the Shlink CLI, then manage short URLs, tags, visits, domains, and health checks for a Shlink instance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses SHLINK_API_KEY to manage a Shlink instance. <br>
Mitigation: Keep the API key private and prefer a least-privileged key where possible. <br>
Risk: Update or delete commands can change short URLs and related Shlink data. <br>
Mitigation: Review commands before running them, especially operations that modify or remove resources. <br>
Risk: Optional global installation uses sudo and installs a locally built binary. <br>
Mitigation: Use sudo install only after trusting the source or pinning a known commit. <br>


## Reference(s): <br>
- [Shlink CLI GitHub repository](https://github.com/ParinLL/shlink-cli) <br>
- [ClawHub skill page](https://clawhub.ai/ParinLL/shlink-cli) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with bash command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHLINK_BASE_URL and SHLINK_API_KEY for Shlink access; building from source also requires Go.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
