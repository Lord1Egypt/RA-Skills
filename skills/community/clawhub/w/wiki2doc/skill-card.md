## Description:

Automatically logs into an internal Confluence wiki, extracts page content into Word documents, analyzes requirement quality, and generates structured test cases with Markdown, JSON, and Excel outputs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[yontlly](https://clawhub.ai/user/yontlly)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, QA engineers, and product teams use this skill to convert Confluence requirement pages into editable documents, identify missing or ambiguous requirement details, and produce structured test cases for review or test management workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The release includes embedded/default wiki credentials.

Mitigation: Replace them with user-provided secrets, rotate any exposed password, and avoid committing credentials in skill files.

Risk: The skill authenticates to Confluence and fetches page content and images that may contain internal information.

Mitigation: Validate the Confluence origin, require HTTPS where available, and restrict use to approved pages and accounts.

Risk: Generated Word, Markdown, JSON, Excel, and debug files may persist sensitive wiki content.

Mitigation: Protect the output directory, disable persistent debug artifacts by default, and clean up generated files according to data handling policy.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/yontlly/skills/wiki2doc)
- [README](artifact/README.md)
- [Usage examples](artifact/examples.md)
- [Skill instructions](artifact/skill.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files]

**Output Format:** [Markdown/text guidance plus generated .docx, .md, .json, and .xlsx files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Generated files are written to a demand output directory and may contain internal Confluence content.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
