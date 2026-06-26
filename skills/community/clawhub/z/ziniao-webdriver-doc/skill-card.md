## Description: <br>
Helps developers understand the Ziniao browser WebDriver automation interface, including its scope, API workflow, startup parameters, framework integration paths, and troubleshooting considerations. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ziniao-open](https://clawhub.ai/user/ziniao-open) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and engineers use this skill to plan and evaluate integrations with Ziniao browser WebDriver APIs, then route to the relevant reference files for request formats, startup parameters, examples, and troubleshooting. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill guides credentialed browser control, which can expose account credentials, store data, or session state if secrets are included in prompts, logs, or source control. <br>
Mitigation: Use a dedicated low-privilege automation account and keep passwords out of prompts, logs, and source control. <br>
Risk: Opening the WebDriver service beyond localhost or running downloaded drivers and demo code without review can increase unauthorized-control or executable-supply-chain risk. <br>
Mitigation: Keep the service bound to localhost unless remote access is deliberately secured, and verify downloaded drivers or demo code before running them. <br>
Risk: Force-killing processes or clearing caches can disrupt active sessions or cause data loss. <br>
Mitigation: Prefer controlled shutdown where possible, confirm target processes, and review the cache-clearing impact before using destructive cleanup steps. <br>


## Reference(s): <br>
- [Ziniao WebDriver Doc Skill](https://clawhub.ai/ziniao-open/ziniao-webdriver-doc) <br>
- [Core Workflow APIs](reference/api-core.md) <br>
- [Auxiliary Management APIs](reference/api-auxiliary.md) <br>
- [Startup Parameters](reference/startup-params.md) <br>
- [Framework Examples](reference/framework-examples.md) <br>
- [Prerequisites and Troubleshooting](reference/prerequisites.md) <br>
- [Ziniao WebDriver Demo Repository](https://github.com/ziniao-open/ziniao_webdriver_demo) <br>
- [Chrome for Testing Downloads](https://googlechromelabs.github.io/chrome-for-testing/) <br>
- [Ziniao WebDriver Permission Guide](https://open.ziniao.com/docSupport?docId=99) <br>
- [Ziniao Official FAQ](https://open.ziniao.com/docSupport?docId=257) <br>


## Skill Output: <br>
**Output Type(s):** [guidance, markdown, code, shell commands, configuration] <br>
**Output Format:** [Markdown guidance with API examples, command snippets, and configuration notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include JSON API payload examples and framework-specific code snippets.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
