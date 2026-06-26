## Description: <br>
Manage a self-hosted WordPress site via SSH and WP-CLI, with REST API support when direct HTTPS access is available. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eddygk](https://clawhub.ai/user/eddygk) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to administer self-hosted WordPress sites, create or update drafts and posts, manage metadata, and run WP-CLI or REST API workflows on configured hosts. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can administer the configured WordPress site, including content, plugin/theme, database, and file-management actions. <br>
Mitigation: Use a dedicated least-privilege SSH user and WordPress application password, verify WP_HOST and WP_ROOT before use, and require confirmation before publishing, deleting, plugin/theme, database, or file-management actions. <br>
Risk: SSH commands use trust-on-first-use host key handling by default. <br>
Mitigation: Pre-pin SSH host keys when possible and reserve disabled host key checking for isolated, trusted CI-style environments. <br>
Risk: REST API use exposes the WordPress application password in the agent execution context as a shell variable. <br>
Mitigation: Use a dedicated application password, avoid logging command environments, and rotate the credential if exposure is suspected. <br>
Risk: Temporary HTML content files are created locally and copied to the remote host. <br>
Mitigation: Create temporary files with restrictive permissions and clean up local and remote copies after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/eddygk/wordpress-selfhosted) <br>
- [Publisher profile](https://clawhub.ai/user/eddygk) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Commands depend on WP_HOST, WP_SSH_USER, WP_ROOT, SSH/SCP, WP-CLI, curl, jq, and optional 1Password CLI.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
