## Description: <br>
Reactive Resume is a developer guidance skill for setting up, extending, templating, migrating, exporting, and self-hosting the Reactive Resume open-source resume builder. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[pupuking723](https://clawhub.ai/user/pupuking723) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to work on Reactive Resume: local setup, custom template development, database migrations, PDF export configuration, API extension, and self-hosted deployment. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The included database reset helper can delete all data from the configured database and uses shell command execution. <br>
Mitigation: Run it only against a disposable local database after reviewing DATABASE_URL, keep backups, avoid --confirm, and prefer revising the helper to use shell=False with strict local database allowlisting. <br>
Risk: Deployment guidance can start privileged, persistent Docker services and includes example secrets or tokens. <br>
Mitigation: Review Docker commands before execution, replace all example secrets and tokens before deployment, and avoid exposing credentials in logs or shared configuration. <br>


## Reference(s): <br>
- [Reactive Resume ClawHub Release](https://clawhub.ai/pupuking723/reactive-resume) <br>
- [Reactive Resume Getting Started](https://docs.rxresu.me/getting-started) <br>
- [Reactive Resume Self-Hosting](https://docs.rxresu.me/self-hosting/docker) <br>
- [Reactive Resume Development](https://docs.rxresu.me/contributing/development) <br>
- [Reactive Resume Architecture](https://docs.rxresu.me/contributing/architecture) <br>
- [Reactive Resume GitHub Repository](https://github.com/amruthpillai/reactive-resume) <br>
- [Template Development Guide](references/templates-guide.md) <br>
- [Deployment Configuration Reference](references/deployment.md) <br>
- [API Development Reference](references/api-reference.md) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with inline code blocks, shell commands, and configuration examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May reference local helper scripts and template boilerplate files included in the artifact.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
