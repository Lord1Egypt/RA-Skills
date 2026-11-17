## Description:

Turn a public PDF URL into a short summary video using Revid's article-to-video workflow.

This skill is ready for commercial/non-commercial use.

## Publisher:

[api00](https://clawhub.ai/user/api00)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use this skill to create 30-90 second narrated summary videos from public whitepapers, research papers, slide exports, ebook chapters, and similar PDF documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local or login-protected PDFs may become accessible to a third-party video service without adequate consent, access control, or cleanup.

Mitigation: Use only PDFs that are allowed to be shared externally; for local or private PDFs, get explicit user approval, use short-lived private or presigned URLs, revoke or delete access after processing, and review Revid's data handling and retention terms.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/api00/skills/revid-pdf-to-video)
- [Revid Render API Endpoint](https://www.revid.ai/api/public/v3/render)
- [Revid Status API Endpoint](https://www.revid.ai/api/public/v3/status)

## Skill Output:

**Output Type(s):** [Guidance, API Calls, JSON, Shell commands, Configuration instructions]

**Output Format:** [Markdown instructions with JSON payload examples and shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires REVID_API_KEY and a PDF URL reachable without authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
