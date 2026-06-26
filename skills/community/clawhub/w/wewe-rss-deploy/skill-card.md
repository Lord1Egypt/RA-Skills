## Description: <br>
Deploys a WeWe RSS service that uses WeChat Read to fetch WeChat public-account articles and publish RSS-style feeds. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[agasding](https://clawhub.ai/user/agasding) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operators use this skill to install, configure, run, and remove a local WeWe RSS service backed by SQLite, with PM2 as an optional process manager. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The service is configured to bind to all interfaces and listen on port 4000, which can expose an account-linked RSS service to untrusted networks. <br>
Mitigation: Bind to 127.0.0.1 unless remote access is intentionally required, restrict firewall access to port 4000, and use a strong AUTH_CODE. <br>
Risk: The deployment uses a public WeChat Read relay through PLATFORM_URL, which may expose account-linked traffic to a third party. <br>
Mitigation: Use a trusted or self-hosted relay and scan the WeChat Read login QR code only when the upstream project and relay are trusted. <br>
Risk: Uninstall commands remove the project directory and local configuration, which may delete the SQLite database and feed state. <br>
Mitigation: Back up the database before uninstalling or replacing the deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/agasding/wewe-rss-deploy) <br>
- [Publisher profile](https://clawhub.ai/user/agasding) <br>
- [Referenced upstream WeWe RSS project](https://github.com/cooderl/wewe-rss) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with shell and environment-variable examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces deployment, verification, usage, troubleshooting, and uninstall steps for an agent to execute or relay.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
