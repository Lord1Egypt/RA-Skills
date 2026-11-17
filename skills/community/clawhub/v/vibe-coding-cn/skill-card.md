## Description:

AI team collaboration skill for generating complete projects from natural-language requirements, including SPEC.md, multi-agent voting approval, and requirements traceability in an OpenClaw environment.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gotomanutd-dot](https://clawhub.ai/user/gotomanutd-dot)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill to turn a project request into requirements, architecture, implementation files, tests, and a summary report. It is suited for prototypes, learning projects, internal tools, MVP validation, and UI component generation where generated code will be reviewed before use.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unsafe path handling may allow generated files to be written outside the intended workspace.

Mitigation: Run the skill only in a constrained workspace, avoid untrusted projectId and outputDir values, and inspect generated file paths before approving writes.

Risk: Folder-opening behavior can invoke shell commands from generated or user-influenced paths.

Mitigation: Review path values before allowing folder-opening actions and disable or remove automatic open-folder behavior in stricter environments.

Risk: The optional local monitor introduces dependency and server exposure concerns.

Mitigation: Keep the optional monitor disabled unless its dependencies and network exposure have been reviewed for the deployment environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gotomanutd-dot/skills/vibe-coding-cn)
- [README](artifact/README.md)
- [Quickstart](artifact/QUICKSTART.md)
- [OpenClaw Integration](artifact/OPENCLAW-INTEGRATION.md)
- [Versioning Guide](artifact/VERSIONING-GUIDE.md)
- [Traceability Matrix](artifact/TRACEABILITY-MATRIX.md)
- [SPEC.md Format](artifact/SPEC-MD-FORMAT.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown guidance with generated project files, tests, progress updates, and optional shell commands.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes generated artifacts under an output directory and can emit real-time progress updates through OpenClaw callbacks or an optional local monitor.]

## Skill Version(s):

4.1.0 (source: server release evidence, target metadata, SKILL.md frontmatter, and claw.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
