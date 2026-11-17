## Description:

Structured field extraction tool that extracts text, table, and paragraph fields from documents according to a user-defined schema.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cf990801-commits](https://clawhub.ai/user/cf990801-commits)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to extract structured text fields, tables, and paragraphs from PDFs, Word documents, Excel files, images, and other supported document formats. It is suited to targeted extraction tasks such as financial report data, contract terms, and form fields when a schema is available or can be constructed from the user's request.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Local or private documents may leave the local machine for DPA processing, including uploads to plaintext HTTP endpoints.

Mitigation: Use the skill only after confirming trusted endpoints, HTTPS/TLS protection, access controls, and retention/deletion practices; avoid sensitive contracts, financial reports, personal data, and confidential files until those controls are verified.

Risk: Custom DPA_BASE_URL or DPA_UPLOAD_URL settings can change where documents and extraction requests are sent.

Mitigation: Verify any custom endpoint values before execution and restrict configuration to approved service URLs.

Risk: Large documents may exceed the default wait time and return a taskId with an in-progress status instead of final extracted data.

Mitigation: Treat task status responses as incomplete until the result endpoint returns final text, table, or paragraph data.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cf990801-commits/skills/test-asdasdasd)
- [Simulation DPA document endpoint](http://imsfz.gjzq.cn:18087/ismp/yx-dpa/document)
- [Simulation DPA upload endpoint](http://imsfz.gjzq.cn:18087/ismp/yx-gw/infras/file/file/v3/upload)
- [Production DPA document endpoint](http://ims.gjzq.cn:18087/ismp/yx-dpa/document)
- [Production DPA upload endpoint](http://ims.gjzq.cn:18087/ismp/yx-gw/infras/file/file/v3/upload)

## Skill Output:

**Output Type(s):** [JSON, Guidance]

**Output Format:** [JSON extraction results containing text, table, and paragraph arrays, plus task identifiers, status messages, source page numbers, and source coordinates when available.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May return a taskId and status instead of final data when asynchronous extraction exceeds the default 60 second wait.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
