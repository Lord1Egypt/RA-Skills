## Description: <br>
Tidepool helps agents build and deploy web apps from the command line with support for authentication, payments, admin panels, email, database, file storage, custom domains, markdown, secrets, and real-time SSE. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[greydanus](https://clawhub.ai/user/greydanus) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Tidepool to create, run, and deploy web applications that need a URL and common web-app services such as login, subscriptions, storage, email, and real-time updates. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can guide agents toward production deployment, secret handling, and destructive synchronization workflows. <br>
Mitigation: Review deploy, push, --secret, --replace-db, --sync, and -y commands before execution; prefer test projects and least-privilege secrets until the workflow is trusted. <br>
Risk: Generated changes can affect code, data, files, users, payment settings, and public application content. <br>
Mitigation: Inspect the application code, data changes, secrets, user settings, payment configuration, and public content before deploying or pushing changes. <br>


## Reference(s): <br>
- [Tidepool homepage](https://tidepool.sh) <br>
- [Tidepool API reference](https://tidepool.sh/api) <br>
- [ClawHub listing](https://clawhub.ai/greydanus/tidepool) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance] <br>
**Output Format:** [Markdown guidance with inline code and shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include commands and configuration that deploy or modify live Tidepool applications.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
