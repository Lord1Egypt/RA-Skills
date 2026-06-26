## Description: <br>
Automatically manages OpenClaw sessions by cleaning inactive sessions, preserving configured sessions, reporting session status, and optionally setting up per-user Nginx reverse proxies. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zx0018](https://clawhub.ai/user/zx0018) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
OpenClaw users and administrators use this skill to keep session files manageable through manual or scheduled cleanup, status reporting, and whitelist-based retention. Teams that need multi-user web access can also use its proxy scripts to create per-user ports after reviewing the security implications. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Proxy setup can make sudo changes to system Nginx configuration and reload Nginx. <br>
Mitigation: Use the proxy scripts only on hosts where those changes are expected; review generated configuration and prefer the cleanup-only workflow when proxy access is not needed. <br>
Risk: Proxy configuration can store an access token in Nginx configuration and redirect clients to a URL containing that token. <br>
Mitigation: Avoid passing tokens on the command line, restrict access to generated Nginx files and logs, and use the proxy feature only when token exposure through redirects is acceptable. <br>
Risk: Session cleanup deletes local session files based on age, minimum-count, and whitelist settings. <br>
Mitigation: Run cleanup with dry-run first, confirm retention settings, and keep important session identifiers in the whitelist. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/zx0018/session-manager-zx) <br>
- [Publisher profile](https://clawhub.ai/user/zx0018) <br>
- [OpenClaw homepage](https://github.com/openclaw/openclaw) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Shell commands, Configuration] <br>
**Output Format:** [Markdown with shell commands and JSON configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces operational instructions for local scripts that may read, delete, or summarize session files and may configure Nginx when proxy features are used.] <br>

## Skill Version(s): <br>
1.0.4 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
