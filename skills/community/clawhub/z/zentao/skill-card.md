## Description: <br>
Use the zentao CLI to login and query ZenTao products and bugs. ZENTAO_URL usually includes /zentao. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external users use this skill to install and run the zentao CLI for ZenTao login, product lookup, bug listing, bug detail lookup, and personal bug queries. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill installs a global npm CLI package. <br>
Mitigation: Install only if you trust the @leeguoo/zentao-mcp package and your npm package source. <br>
Risk: ZenTao credentials are stored in a local config file after login. <br>
Mitigation: Use a least-privileged ZenTao account, protect the config file, and remove or rotate credentials when no longer needed. <br>


## Reference(s): <br>
- [@leeguoo/zentao-mcp npm package](https://www.npmjs.com/package/@leeguoo/zentao-mcp) <br>
- [ClawHub skill page](https://clawhub.ai/leeguooooo/zentao) <br>


## Skill Output: <br>
**Output Type(s):** [Shell commands, Configuration instructions, Guidance] <br>
**Output Format:** [Markdown with inline bash commands and optional JSON CLI output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [CLI commands may produce simple text or JSON when --json is requested.] <br>

## Skill Version(s): <br>
1.0.1 (source: release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
