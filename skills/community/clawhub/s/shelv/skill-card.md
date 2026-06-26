## Description: <br>
Convert PDFs into structured Markdown filesystems and hydrate them into your workspace for exploration with standard Unix tools. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[JoshuaOHanlon](https://clawhub.ai/user/JoshuaOHanlon) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to upload selected PDFs to Shelv, wait for processing, and hydrate the resulting Markdown filesystem into an OpenClaw workspace for inspection with standard Unix tools. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Selected PDFs are sent to shelv.dev for processing. <br>
Mitigation: Use a revocable Shelv API key, and avoid regulated or confidential documents unless approved by your organization. <br>
Risk: Hydrating with --force can replace an existing local shelf directory. <br>
Mitigation: Use --force only when you intend to replace the existing hydrated shelf. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/JoshuaOHanlon/shelv) <br>
- [Shelv homepage](https://shelv.dev) <br>
- [Shelv documentation](https://docs.shelv.dev) <br>
- [API Reference](references/api-reference.md) <br>
- [Shelf Lifecycle](references/shelf-lifecycle.md) <br>
- [Error Handling](references/error-handling.md) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, Files, Shell commands, Guidance] <br>
**Output Format:** [Markdown guidance with inline shell commands and hydrated Markdown filesystem output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires SHELV_API_KEY and local curl, tar, jq, and checksum tooling on macOS or Linux.] <br>

## Skill Version(s): <br>
1.0.3 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
