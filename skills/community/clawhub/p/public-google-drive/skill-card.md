## Description:

Create public Google Docs and Google Sheets in Memyard's workspace without requiring Google OAuth.

This skill is ready for commercial/non-commercial use.

## Publisher:

[memyard](https://clawhub.ai/user/memyard)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to create, update, and list public Google Docs or Sheets through Memyard without a Google sign-in flow.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Documents created through this skill are public to anyone with the share link.

Mitigation: Use it only for content where public link-based viewing is acceptable, and avoid private, regulated, or confidential material unless that sharing model is approved.

Risk: Document content is sent to Memyard for creation and updates.

Mitigation: Review content sensitivity before using the skill and avoid sending data that should not be processed by Memyard.

Risk: The skill stores a local agent key for future requests.

Mitigation: Protect the per-user config file and delete the stored key if the skill is no longer used.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/memyard/skills/public-google-drive)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with JSON API payloads, shell command examples, and public share URLs.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Creates documents with anyone-with-link viewer access and stores an agent key in a per-user local config file.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
