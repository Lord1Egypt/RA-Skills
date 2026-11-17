## Description:

AI-assisted tool for building WeChat Mini Programs with templates, generated pages and components, cloud function templates, and deployment guidance.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yang1002378395-cmyk](https://clawhub.ai/user/yang1002378395-cmyk)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and small-business teams use this skill to scaffold WeChat Mini Program projects, generate page code from prompts, create common cloud function templates, and follow deployment guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Prompts may be shared with a remote AI service.

Mitigation: Do not enter secrets, confidential requirements, private customer data, or unreleased business plans in prompts.

Risk: The skill can write generated project, page, and cloud function files into the local workspace.

Mitigation: Run it only in a dedicated workspace, avoid path-like names, and review generated files before merging or deploying them.

Risk: Generated cloud function packages may use unpinned npm dependencies.

Mitigation: Pin and review npm dependencies before installing or deploying generated cloud functions.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yang1002378395-cmyk/skills/wechat-mini-program-builder)
- [Publisher profile](https://clawhub.ai/user/yang1002378395-cmyk)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown with generated WXML, WXSS, JavaScript, JSON, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May write generated project files, page markdown, and cloud function templates in the working directory.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact documentation)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
