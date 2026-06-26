## Description: <br>
Query and sync YApi interface documentation. Use when user mentions "yapi 接口文档", YAPI docs, asks for request/response details, or needs docs sync. Also triggers when user pastes a YApi URL that matches the configured base_url. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[leeguooooo](https://clawhub.ai/user/leeguooooo) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and engineers use this skill to query YApi interface documentation, summarize request and response details, and synchronize documentation with YApi projects. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The fallback command runs an npm package during agent work. <br>
Mitigation: Review the package source before installation or execution, and prefer a trusted installed yapi command when available. <br>
Risk: Docs sync commands can modify local project metadata and documentation mappings. <br>
Mitigation: Run the documented dry-run first and perform the real sync only when the workspace changes are intended. <br>
Risk: YApi authentication data is read from local config and auth cache files. <br>
Mitigation: Keep YApi tokens scoped to the intended projects and protect the local YApi config and auth cache. <br>


## Reference(s): <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with inline shell commands and API request summaries] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include YApi lookup commands, docs-sync dry-run guidance, and configuration path references.] <br>

## Skill Version(s): <br>
1.0.1 (source: ClawHub release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
