## Description: <br>
Migrate N8N/Zapier/Make workflows to production-grade Python or Node.js scripts. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[kevdogg102396-afk](https://clawhub.ai/user/kevdogg102396-afk) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and automation engineers use this skill to convert N8N, Zapier, or Make workflow descriptions or exports into runnable Python or Node.js automation projects with retry, logging, dry-run support, and deployment files. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated workflow failure alerts may use Kevin-specific Telegram settings and send workflow failure details to an unrelated destination. <br>
Mitigation: Replace or remove the Telegram settings before use and provide only an alert destination that the user explicitly approves. <br>
Risk: Generated automation scripts may make API, email, database, or file-system changes when run with real credentials. <br>
Mitigation: Review generated files, test with --dry-run, and use non-production credentials before enabling live execution. <br>
Risk: Recurring generated scripts may continue running after migration if they are not clearly scoped. <br>
Mitigation: Keep recurring scripts in a dedicated directory and document a known stop or disable path before deployment. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/kevdogg102396-afk/workflow-migrate) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with generated Python or Node.js code, dependency manifests, environment examples, optional skill instructions, and run commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Generated projects are intended to be reviewed, tested with dry-run mode, and configured with user-provided credentials before use.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
