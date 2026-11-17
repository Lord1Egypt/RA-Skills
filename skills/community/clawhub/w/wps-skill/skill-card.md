## Description:

WPS Office automation skill supporting document creation, Markdown conversion, and image-text layout.

This skill is ready for commercial/non-commercial use.

## Publisher:

[lilei0311](https://clawhub.ai/user/lilei0311)

### License/Terms of Use:

MIT

## Use Case:

Developers and office automation users use this skill to create, open, convert, and batch-process WPS Office documents, including Word, Excel, PPT, Markdown, and image-text layouts. It also supports optional WPS 365 cloud operations when credentials are configured.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can launch WPS, simulate desktop typing, and modify local Office files.

Mitigation: Use it in a trusted desktop session, review requested actions before execution, and keep backups or separate output paths for conversions and batch edits.

Risk: Optional WPS 365 features require app_id and app_secret credentials.

Mitigation: Leave cloud credentials blank unless the cloud features are needed, keep credentials out of shared project files, and rotate them if exposed.

Risk: Document and Markdown conversion paths may be unsafe for untrusted input files.

Mitigation: Avoid processing untrusted Markdown or Office files, and test new workflows in a sandbox or virtual machine before routine use.

## Reference(s):

- [WPS Open Platform](https://open.wps.cn)
- [WPS Open Platform API Documentation](https://open.wps.cn/docs)
- [WPS Open Platform Auth Documentation](https://open.wps.cn/docs/auth)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, files]

**Output Format:** [Markdown guidance, command-line invocations, JSON status output, and generated Office or Markdown files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create, open, modify, or convert local WPS Office documents; WPS 365 functions require optional app_id and app_secret configuration.]

## Skill Version(s):

1.3.0 (source: server release metadata and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
