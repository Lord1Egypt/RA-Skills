## Description: <br>
Enables the agent to create, manage, and publish a full-featured blog autonomously. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[harshraj001](https://clawhub.ai/user/harshraj001) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, creators, and agents use this skill to set up and operate a professional blog, write Markdown posts, upload media, manage themes and settings, view analytics, and deploy the platform to Cloudflare or Vercel. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Agents can perform high-impact blog actions, including publishing, deleting posts, switching production themes, and deploying the platform. <br>
Mitigation: Require explicit human approval before deleting posts, publishing content, switching production themes, or deploying. <br>
Risk: The skill handles deployment and credentials for database, cache, API key, and hosting providers. <br>
Mitigation: Use a dedicated blog project, back up any existing .env.local file before setup, and keep API keys and service credentials out of public-facing code. <br>
Risk: The security summary flags weak safeguards around the web framework and content handling. <br>
Mitigation: Upgrade the web framework and harden content sanitization and SVG handling before production use. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/harshraj001/write-my-blog) <br>
- [Publisher profile](https://clawhub.ai/user/harshraj001) <br>
- [Write My Blog API Reference](references/api-reference.md) <br>
- [Write My Blog Theme Guide](references/theme-guide.md) <br>


## Skill Output: <br>
**Output Type(s):** [markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with API examples, shell commands, and configuration values] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces and manages blog content, media, themes, settings, deployment commands, and REST API requests.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
