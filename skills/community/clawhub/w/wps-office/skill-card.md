## Description:

Automates WPS Office document creation, opening, listing, format conversion, batch processing, and optional WPS 365 form, document, sheet, flowchart, and mind-map workflows.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and office automation users can use this skill to create, open, list, and convert WPS Office documents from an agent workflow. Teams that configure WPS Open Platform credentials can also use it for WPS 365 forms, online documents, sheets, flowcharts, and mind maps.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local automation can type into the active window and may affect the wrong application or document.

Mitigation: Test in an isolated desktop session first, keep focus controlled while commands run, and review each automated action before using it with important documents.

Risk: Document creation and batch conversion can create or modify files outside the intended folder.

Mitigation: Use a trusted test directory, avoid broad batch-conversion targets, and confirm input and output paths before execution.

Risk: WPS 365 features require API credentials that could expose cloud resources if mishandled.

Mitigation: Leave credentials blank unless needed, use least-privilege WPS app credentials, avoid shared machines, and rotate secrets regularly.

Risk: Converting untrusted Markdown may produce unsafe or misleading document output.

Mitigation: Convert only trusted Markdown and inspect generated RTF, HTML, or document files before sharing or opening them in sensitive environments.

## Reference(s):

- [ClawHub skill listing](https://clawhub.ai/lilei0311/skills/wps-office)
- [WPS Open Platform documentation](https://open.wps.cn/docs)
- [WPS Open Platform](https://open.wps.cn)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with inline shell commands, JSON configuration examples, and text or JSON command results]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May launch local WPS Office, write or convert files, and call WPS 365 APIs when credentials are configured.]

## Skill Version(s):

1.0.1 (source: server release metadata and artifact skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
