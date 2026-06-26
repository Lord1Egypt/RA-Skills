## Description: <br>
Package and publish OpenClaw skills to the ClawHub registry. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tonakic](https://clawhub.ai/user/tonakic) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and skill maintainers use this skill to prepare, sanitize, version, and publish OpenClaw skills to ClawHub. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens can be exposed during login, publishing, or local configuration. <br>
Mitigation: Use placeholders in published artifacts, keep real tokens in protected local config or environment variables, and avoid putting real keys on command lines. <br>
Risk: A skill package can accidentally include secrets or private endpoints before release. <br>
Mitigation: Run the included sensitive-data scan and manually review the skill folder before publishing. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/tonakic/up-skill-to-clawhub) <br>
- [Configuration template](references/config.template.json) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON configuration snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Bilingual English and Chinese workflow guidance with a sensitive-data review checklist.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
