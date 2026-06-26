## Description: <br>
Tunelo exposes local services and files through a public HTTPS URL so agents can share previews, dev servers, demos, or temporary localhost access. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[claw-bot](https://clawhub.ai/user/claw-bot) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent operators use this skill when a user needs remote access to local files, a local dev server, a demo service, or localhost content from another device or network. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can make local files or services reachable from the internet. <br>
Mitigation: Use it only for paths and ports intended for sharing, prefer --private or --local when appropriate, avoid broad folders such as home or Documents, and stop the tunnel when finished. <br>
Risk: Installation uses a remote shell script from tunelo.net. <br>
Mitigation: Install only when tunelo.net is trusted and the operator is comfortable with the remote installer. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/claw-bot/tunelo) <br>
- [Tunelo install script](https://tunelo.net/install.sh) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, shell commands, configuration] <br>
**Output Format:** [Markdown with inline shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include public HTTPS tunnel URLs, local preview URLs, access codes, and relay or host options.] <br>

## Skill Version(s): <br>
0.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
