## Description:

Classify documents into user-defined categories using Upstage Document Classification API, with optional document splitting for multi-document PDFs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[upstage-deployment](https://clawhub.ai/user/upstage-deployment)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and document-processing teams use this skill to classify files into user-defined categories, route documents by type, and split mixed PDFs into separate document groups.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents or document URLs submitted for classification are sent to Upstage's remote API under the user's Upstage account.

Mitigation: Use the skill only with documents approved for that service, and avoid highly sensitive, regulated, or confidential content unless organizational policy allows it.

Risk: Classification and split results may persist on disk at the resolved output path.

Mitigation: Review output locations before use and clean up generated files according to local data-handling requirements.

Risk: Low-confidence classifications can route documents incorrectly.

Mitigation: Use returned confidence scores to flag uncertain results for manual review.

## Reference(s):

- [Upstage Document Classification API](https://console.upstage.ai/api/document-classification)
- [Document Split - Multi-Document Separation](references/document-split.md)
- [ClawHub Skill Page](https://clawhub.ai/upstage-deployment/skills/upstage-document-classification)
- [Publisher Profile](https://clawhub.ai/user/upstage-deployment)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands, configuration, json, files]

**Output Format:** [Markdown guidance with Python and curl examples, JSON response structures, and resolved output file paths]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce classified JSON files or split-document output files when the agent applies the workflow.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
