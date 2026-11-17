## Description:

Analyze Chinese writing style fingerprints by extracting syntax patterns, lexical preferences, and rhetorical features from text or files and saving JSON fingerprints for writing agents.

This skill is ready for commercial/non-commercial use.

## Publisher:

[noah-1106](https://clawhub.ai/user/noah-1106)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, writers, and writing-agent builders use this skill to analyze Chinese writing samples, persist style fingerprints, and export compact guidance for later writing-agent prompts.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Saved fingerprints include a short raw sample of analyzed text.

Mitigation: Use the skill only with text that is acceptable to store locally, and remove generated fingerprints that contain sensitive samples.

Risk: Untrusted fingerprint names or export paths may escape the intended storage or output area.

Mitigation: Avoid untrusted names and output paths until path validation and confinement are added; run the skill in an isolated working directory for review.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/noah-1106/skills/style-fingerprint)
- [Publisher profile](https://clawhub.ai/user/noah-1106)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Terminal text reports, JSON fingerprint files, and exported Markdown-style writing guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires python3; saves fingerprints locally under ./fingerprints/ and can export guidance to a user-specified output path.]

## Skill Version(s):

1.0.0 (source: release evidence and skill.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
