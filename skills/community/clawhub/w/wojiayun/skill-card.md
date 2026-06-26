## Description: <br>
Provides Wojiayun equipment management and work-order API access for device lookup, repair, inspection, maintenance, file upload, project switching, and multi-project work-order reporting. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[mumuxilele](https://clawhub.ai/user/mumuxilele) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and operations teams with a scoped Wojiayun API key use this skill to query equipment, create and manage work orders, inspect maintenance data, switch projects, upload files, and aggregate multi-project work-order statistics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill requires OAuth-style token handling and sensitive Wojiayun credentials. <br>
Mitigation: Install only if the publisher is trusted, use a scoped API key, and treat local key, token, and config files as sensitive business data. <br>
Risk: A bundled default-key helper is present in the artifact. <br>
Mitigation: Do not use the default-key helper; provision and rotate a user-controlled scoped API key instead. <br>
Risk: The skill can create work orders, upload files, switch projects, export inventory data, and change the API base URL. <br>
Mitigation: Review these actions before execution, avoid changing the base URL, and protect generated SQL exports as sensitive operational data. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/mumuxilele/wojiayun) <br>
- [Artifact skill instructions](artifact/SKILL.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with Python code examples and API response data] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires a scoped Wojiayun API key; may read or write local encrypted key, token, config, and SQL export files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
