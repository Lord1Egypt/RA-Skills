## Description: <br>
Private mesh networking and public IP exposure via Telnyx WireGuard infrastructure. Connect nodes securely or expose services to the internet. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[teamtelnyx](https://clawhub.ai/user/teamtelnyx) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and infrastructure operators use this skill to create Telnyx-backed WireGuard mesh networks, join nodes, discover peers, and optionally expose selected services through a public IP. <br>

### Deployment Geography for Use: <br>
Global, subject to Telnyx regional gateway availability. <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent lasting privileged control over WireGuard through passwordless sudoers configuration. <br>
Mitigation: Use setup-sudoers only when unattended WireGuard control is required, and remove the exact /etc/sudoers.d/wireguard-<user> file when finished. <br>
Risk: The skill can expose local services to the internet through a public IP and opened ports. <br>
Mitigation: Expose only authenticated services, avoid high-risk ports unless explicitly reviewed, and confirm firewall state before use. <br>
Risk: Generated WireGuard configuration files and Telnyx API credentials can grant access to network resources. <br>
Mitigation: Use a scoped Telnyx API key, protect generated wg-*.conf files as secrets, and avoid committing local configuration or credential files. <br>
Risk: Scripts may load environment variables from a local .env file in the skill directory. <br>
Mitigation: Run the scripts only from trusted directories and inspect local .env files before execution. <br>


## Reference(s): <br>
- [Telnyx Network skill page](https://clawhub.ai/teamtelnyx/telnyx-network) <br>
- [Telnyx API keys](https://portal.telnyx.com/#/app/api-keys) <br>
- [Telnyx API v2](https://api.telnyx.com/v2) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with bash command examples and generated local configuration files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The scripts can create or update local network state such as config.json and WireGuard configuration files when run.] <br>

## Skill Version(s): <br>
1.0.0 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
