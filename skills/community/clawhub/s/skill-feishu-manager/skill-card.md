## Description:

Comprehensive Feishu (Feishu) management toolkit for documents, knowledge bases, bitables, and cloud storage.

This skill is ready for commercial/non-commercial use.

## Publisher:

[limoxt](https://clawhub.ai/user/limoxt)

### License/Terms of Use:

MIT

## Use Case:

Developers and workspace operators use this skill to let an agent read, create, and update Feishu documents, wiki pages, bitable records, and drive folders.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Feishu app secrets could expose workspace access if mishandled.

Mitigation: Protect the app_secret and configure the Feishu app with least-privilege permissions where possible.

Risk: Create or write actions can modify documents, wiki pages, bitables, or drive folders.

Mitigation: Confirm intended changes before allowing document, wiki, bitable, or drive create/write actions.

## Reference(s):

- [Feishu Open Platform](https://open.feishu.cn)

## Skill Output:

**Output Type(s):** [API Calls, Markdown, Configuration instructions, Shell commands, Guidance]

**Output Format:** [Markdown with Feishu tool-call examples and YAML configuration]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May propose Feishu document, wiki, bitable, or drive create/write actions that require user confirmation.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
