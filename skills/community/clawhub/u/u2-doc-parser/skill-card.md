## Description:

Parse documents with the UniDoc API and convert supported files to Markdown or JSON using synchronous or asynchronous processing.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aaiccee](https://clawhub.ai/user/aaiccee)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to convert PDFs, Office documents, text files, and images into Markdown or JSON for downstream analysis or content extraction workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents are uploaded to an external unauthenticated UAT service for processing.

Mitigation: Use only non-sensitive test documents and review data handling requirements before installation or use.

Risk: Endpoint overrides and skipped security checks can route documents to untrusted services or suppress warnings.

Mitigation: Avoid --skip-security-check and do not set UNIDOC_BASE_URL or UNIDOC_API_KEY unless the endpoint is fully trusted.

Risk: The force option can delete directories when an output path already exists as a directory.

Mitigation: Do not use --force with paths that may be directories until the recursive deletion behavior is fixed.

## Reference(s):

- [UniDoc API Documentation](http://unidoc.uat.hivoice.cn)
- [ClawHub Skill Page](https://clawhub.ai/aaiccee/skills/u2-doc-parser)

## Skill Output:

**Output Type(s):** [Text, Markdown, JSON, Files, Shell commands, Guidance]

**Output Format:** [Markdown or JSON content printed to stdout or saved to a specified file, with progress and errors on stderr.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Supports sync and async parsing modes, selectable output format, custom conversion method, optional user ID, and optional output path.]

## Skill Version(s):

1.0.5 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
