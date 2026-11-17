## Description:

Write GCP-compliant Standard Operating Procedures for labs and clinical sites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[aipoch-ai](https://clawhub.ai/user/aipoch-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Lab and clinical site teams use this skill to draft Standard Operating Procedures for sample processing, equipment calibration, safety procedures, and GCP compliance workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The SOP output path can overwrite any file the running process is allowed to write.

Mitigation: Run the skill in a controlled workspace, use trusted output filenames, avoid absolute paths and ../ traversal, and restrict output to a dedicated directory.

Risk: Generated SOPs may omit site-specific controls or contain placeholders that are not ready for regulated use.

Mitigation: Have qualified staff review and complete the generated SOP before operational or compliance use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/aipoch-ai/skills/sop-writer-aipoch)
- [Publisher profile](https://clawhub.ai/user/aipoch-ai)

## Skill Output:

**Output Type(s):** [text, markdown, files]

**Output Format:** [Plain text SOP document with structured sections]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes the generated SOP to a user-selected output path.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
