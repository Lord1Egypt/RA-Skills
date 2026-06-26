## Description: <br>
ZEDEDA edge management API client covering 473 endpoints across edge nodes, applications, clusters, storage, networking, Kubernetes, diagnostics, jobs, and user management. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[krisclarkdev](https://clawhub.ai/user/krisclarkdev) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and operators use this skill to let an agent query and administer ZEDEDA edge management resources through authenticated CLI-style commands and Python service classes. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: An agent can perform disruptive ZEDEDA infrastructure or IAM actions without built-in confirmations. <br>
Mitigation: Review agent plans before allowing delete, reboot, offboard, deactivate, bulk job, secret-listing, or user-management commands. <br>
Risk: The ZEDEDA_API_TOKEN can authorize broad administrative access to ZEDEDA resources. <br>
Mitigation: Use a least-privilege token and avoid production-wide permissions where possible. <br>


## Reference(s): <br>
- [ClawHub ZEDEDA Release](https://clawhub.ai/krisclarkdev/zededa) <br>
- [ZEDEDA API Endpoint](https://zedcontrol.zededa.net/api) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Code, API Calls, Configuration, Guidance] <br>
**Output Format:** [Markdown with inline shell commands, Python code examples, and JSON request bodies] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses ZEDEDA_API_TOKEN and optional ZEDEDA_BASE_URL and ZEDEDA_LOG_LEVEL environment variables.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release metadata; artifact frontmatter reports 1.0.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
