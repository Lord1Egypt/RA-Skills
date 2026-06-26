## Description: <br>
Automates a local WeChat Official Account publishing workflow from environment setup and source gathering through article drafting, image preparation, draft submission, optional final publication, result archiving, scheduling, and alerting while keeping real secrets outside the package. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[16miku](https://clawhub.ai/user/16miku) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External operators, developers, and content teams use this skill to standardize and run a reproducible local WeChat Official Account article workflow, including draft-first production operation and optional scheduled automation. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow can publish live content to a WeChat Official Account when configured with valid account credentials. <br>
Mitigation: Use draft-only mode as the production default, require an explicit final-publish decision, and test first with a non-production or tightly controlled account. <br>
Risk: The included fallback publish script logs part of the WeChat access token. <br>
Mitigation: Remove the access_token log line before operational use and keep real secrets only in a protected local .env file. <br>
Risk: Scheduled automation can repeatedly submit drafts or publications if cron entries are enabled without review. <br>
Mitigation: Review cron entries before enabling them and isolate each account in its own working directory, .env file, title history, and log path. <br>
Risk: API-based freepublish success may not match manual WeChat backend publication behavior or homepage visibility. <br>
Mitigation: Treat technical API success separately from platform and operational success, and manually verify draft or publication visibility in the WeChat backend. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/16miku/wechat-auto-publishing) <br>
- [README](README.md) <br>
- [Runbook](runbook.md) <br>
- [Environment and Configuration](references/environment-and-config.md) <br>
- [Source Gathering](references/source-gathering.md) <br>
- [Writing Style](references/writing-style.md) <br>
- [Image Strategy](references/image-strategy.md) <br>
- [Publishing](references/publishing.md) <br>
- [Scheduling and Alerting](references/scheduling-and-alerting.md) <br>
- [Security Boundary](references/security-boundary.md) <br>
- [Fallback publish script template](templates/publish.mjs) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands, configuration templates, JavaScript script templates, and JSON result artifacts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Produces local workflow scaffolding and operator-facing instructions; publishing actions require separately supplied WeChat credentials and local execution.] <br>

## Skill Version(s): <br>
3.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
