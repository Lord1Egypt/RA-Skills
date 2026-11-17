## Description:

X/Twitter CLI for reading, searching, and posting via cookies or Sweetistics.

This skill is ready for commercial/non-commercial use.

## Publisher:

[soanai](https://clawhub.ai/user/soanai)

### License/Terms of Use:


## Use Case:

External users and developers use this skill to guide an agent in reading, searching, and posting on X/Twitter through the bird CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bird executable may receive access to X/Twitter authentication material and posting authority.

Mitigation: Use a dedicated, revocable API key or isolated browser profile, run `bird check` before use, and review account actions before posting.

Risk: The external CLI provenance is not resolved by the server evidence.

Mitigation: Review the upstream CLI source and install path before authorizing account access.

## Reference(s):

- [bird homepage](https://bird.fast)
- [ClawHub skill page](https://clawhub.ai/soanai/skills/xbio)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Guidance may reference the bird executable, browser cookies, and SWEETISTICS_API_KEY authentication.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
