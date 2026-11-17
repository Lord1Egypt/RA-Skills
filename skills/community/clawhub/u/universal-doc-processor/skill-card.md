## Description:

Universal Doc Processor helps agents receive, parse, and manage user-supplied documents across common formats, then wait for explicit instructions before analyzing, modifying, extracting, translating, or converting content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cyril-ruidong](https://clawhub.ai/user/cyril-ruidong)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to stage uploaded documents, request analysis or transformation tasks, and receive clarifying questions when the requested document operation is underspecified.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill trusts supplied file paths and could read files outside the intended upload area.

Mitigation: Run it only in a sandbox or constrain uploads to a trusted directory, and avoid granting access to directories containing credentials, private workspace files, or other users' documents.

Risk: The release has a suspicious security verdict and low trust tier in the provided server evidence.

Mitigation: Review the skill before installing and require publisher fixes for path validation, size limits, and retention controls before broader use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/cyril-ruidong/skills/universal-doc-processor)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown or plain text responses with optional processed document files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Maintains per-session file state for multi-turn document tasks.]

## Skill Version(s):

2.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
