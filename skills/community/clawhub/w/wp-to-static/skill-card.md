## Description: <br>
Convert a WordPress website to a static site and deploy to Cloudflare Pages. Mirrors the rendered HTML via SSH, extracts only referenced assets, fixes URLs, self-hosts fonts, strips WordPress cruft, and deploys. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[abhibavishi](https://clawhub.ai/user/abhibavishi) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to migrate a WordPress site into static assets and deploy it to Cloudflare Pages. It is intended for controlled migrations where the user has SSH access to the WordPress host and authenticated GitHub and Cloudflare CLIs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires SSH access to the WordPress server and authenticated GitHub and Cloudflare CLIs. <br>
Mitigation: Install only when the agent should access the target server and use the authenticated CLIs; keep the repository private unless intentionally changed. <br>
Risk: A migration could expose WordPress server-side files or secrets if sensitive files are copied or committed. <br>
Mitigation: Use the documented rsync exclusions, scrub ./build before git operations, and verify ./public contains no PHP, wp-config, .env, SQL dumps, or other secrets before deployment. <br>
Risk: SSH host verification failures could indicate an untrusted or unexpected server. <br>
Mitigation: Require the server host key to be verified in known_hosts and do not bypass host key checking. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/abhibavishi/wp-to-static) <br>
- [ClawHub publisher profile](https://clawhub.ai/user/abhibavishi) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and file-generation instructions] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May create local static-site artifacts under ./build and ./public before deployment.] <br>

## Skill Version(s): <br>
1.2.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
