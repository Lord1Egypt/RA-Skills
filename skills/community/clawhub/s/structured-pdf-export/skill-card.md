## Description:

Structured PDF Export converts structured content such as tables, comparison lists, and data visualizations into styled local PDF files for delivery through OpenClaw.

This skill is ready for commercial/non-commercial use.

## Publisher:

[huchiyv](https://clawhub.ai/user/huchiyv)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and OpenClaw users use this skill when they need to present structured information as a polished PDF instead of a plain markdown table. It is intended for single-user or fully trusted environments where local browser rendering, local file handling, and manual sensitive-data review are acceptable.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A local HTTP server can expose generated files beyond localhost.

Mitigation: Bind the server to 127.0.0.1 and use a unique per-run temporary directory with restrictive permissions.

Risk: Generated PDFs may include confidential or sensitive data because automatic sensitive-data scanning is unavailable.

Mitigation: Manually review source content, the rendered HTML, and the final PDF before sending the file.

Risk: HTML title and subtitle fields may include unescaped content.

Mitigation: Escape user-provided HTML fields before rendering and avoid inserting untrusted markup.

Risk: Port 8888 conflicts can interrupt unrelated work on shared or multi-user systems.

Mitigation: Use a user-specific or random port and manually verify process ownership before stopping any process.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/huchiyv/skills/structured-pdf-export)
- [Publisher Profile](https://clawhub.ai/user/huchiyv)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown instructions with bash and Python-assisted local file generation]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces local HTML/PDF workflow guidance and files; final PDF delivery depends on OpenClaw browser and message tools.]

## Skill Version(s):

1.2.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
