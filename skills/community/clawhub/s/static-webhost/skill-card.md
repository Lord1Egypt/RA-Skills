## Description: <br>
Deploys static web pages and apps through Caddy or Nginx, with auto-detection and guidance for hosting files over HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[serein-213](https://clawhub.ai/user/serein-213) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill when they need an agent to prepare or deploy static HTML, CSS, JavaScript, or app build files through a machine's Caddy or Nginx web server. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may propose administrator-level changes to web-server configuration, service state, or /var/www/html. <br>
Mitigation: Confirm every sudo/root command, back up existing Caddy or Nginx configuration and the web root, and test configuration before reloading services. <br>
Risk: Static deployment can expose unintended private files if the wrong source directory is copied into the public web root. <br>
Mitigation: Review the files selected for deployment and copy only intended public assets. <br>


## Reference(s): <br>
- [Static Webhost on ClawHub](https://clawhub.ai/serein-213/static-webhost) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with shell command and web-server configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include sudo/root commands that require explicit confirmation before execution.] <br>

## Skill Version(s): <br>
1.2.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
