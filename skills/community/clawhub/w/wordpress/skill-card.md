## Description: <br>
OpenClaw skill that provides a WordPress REST API CLI for posts, pages, categories, tags, users, and custom requests using plain HTTP. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[codedao12](https://clawhub.ai/user/codedao12) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and site operators use this skill to automate WordPress post, page, taxonomy, user-read, and custom REST API workflows through a Node.js CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can create, update, publish, or delete WordPress site content when configured with powerful credentials. <br>
Mitigation: Use a dedicated low-privilege WordPress account and require explicit approval before write, delete, publish, or raw request commands. <br>
Risk: WordPress credentials or tokens could be exposed if logged, committed, or passed through unsafe workflows. <br>
Mitigation: Store credentials in environment variables, avoid logging secrets, and use HTTPS for the configured WP_BASE_URL. <br>
Risk: The @file input convention can send local file contents to the configured WordPress site. <br>
Mitigation: Avoid passing sensitive local files with @file and review file paths before execution. <br>


## Reference(s): <br>
- [WordPress REST API Guide](assets/wordpress-rest-api-guide.md) <br>
- [WordPress REST API credentials example](env_example.md) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, Shell commands, Configuration, Guidance] <br>
**Output Format:** [JSON to stdout with CLI help text and stderr errors] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Non-zero exit codes on errors; credentials are supplied through environment variables.] <br>

## Skill Version(s): <br>
1.0.0 (source: package.json and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
