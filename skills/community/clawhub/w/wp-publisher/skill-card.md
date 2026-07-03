## Description: <br>
Publish WordPress posts via REST API from any OpenClaw channel (WeChat/QQ/DingTalk/etc). AI writes in Markdown, auto-converts to HTML, posts to your blog, and returns the link. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[foxihaohao](https://clawhub.ai/user/foxihaohao) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site operators, and content teams use this skill to draft Markdown content, convert it to HTML, and publish or manage WordPress posts through the WordPress REST API from OpenClaw channels. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill gives an agent authenticated WordPress content-management access, including update and permanent delete operations. <br>
Mitigation: Use a dedicated low-privilege WordPress application password and require explicit human confirmation before update or delete actions. <br>
Risk: WordPress credentials could be exposed if secrets are pasted directly into reusable commands or shared logs. <br>
Mitigation: Provide credentials through environment variables or a secure secret mechanism, and avoid embedding secrets directly in commands. <br>
Risk: Disabling TLS certificate checks can weaken transport security for WordPress API requests. <br>
Mitigation: Require HTTPS with valid certificate verification and avoid disabling certificate checks in production use. <br>


## Reference(s): <br>
- [WP Publisher on ClawHub](https://clawhub.ai/foxihaohao/wp-publisher) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline bash and Python code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces WordPress REST API calls and a published article link when posting succeeds. Requires WordPress API base URL, username, and application password supplied by the user.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
