## Description:

Compile Typst and LaTeX documents to PDF via API. Send source code, get back a PDF.

This skill is ready for commercial/non-commercial use.

## Publisher:

[gregm711](https://clawhub.ai/user/gregm711)

### License/Terms of Use:


## Use Case:

Developers and agents use this skill to compile Typst and LaTeX source, including multi-file projects and auxiliary assets, into PDF output through the TypeTex public API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Typst or LaTeX source, auxiliary files, and embedded images are sent to the external TypeTex/Modal API for compilation.

Mitigation: Use only with content appropriate for that external service, and avoid secrets, confidential business documents, personal data, or regulated material unless the service's privacy and retention posture has been separately approved.

Risk: Compilation depends on a remote public API, so availability, timeout behavior, and shared-service limits can affect results.

Mitigation: Check the API success field before using PDF output, surface returned error details to users, and keep test compilations minimal when diagnosing issues.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/gregm711/skills/typetex)
- [TypeTex Public Compile API](artifact/openapi.yaml)
- [TypeTex](https://typetex.app)
- [Typst Documentation](https://typst.app/docs/)
- [LaTeX Wikibook](https://en.wikibooks.org/wiki/LaTeX)

## Skill Output:

**Output Type(s):** [Guidance, Code, Shell commands, Files]

**Output Format:** [Markdown with API request examples and PDF file output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Remote API responses include base64-encoded PDF content on success and human-readable errors on failure; LaTeX failures may include compilation logs.]

## Skill Version(s):

1.5.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
