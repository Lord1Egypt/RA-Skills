## Description:

Extract and validate URLs from text, presenting results in a clear format with brief descriptions and image previews.

This skill is ready for commercial/non-commercial use.

## Publisher:

[openlark](https://clawhub.ai/user/openlark)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and external users use this skill to extract web addresses from pasted text, validate accessibility, and receive a concise table with status, titles, and image-preview markers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Validating extracted URLs may cause the agent runtime to contact external, internal, localhost, cloud metadata, or private-network addresses found in user-provided text.

Mitigation: Use this skill only in runtimes that block unsafe destinations, or avoid validation for untrusted text containing internal or private-network URLs.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/openlark/skills/url-extractor)

## Skill Output:

**Output Type(s):** [Markdown, Text, Guidance]

**Output Format:** [Markdown table with counts, URL statuses, title or description text, and optional image preview notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [For large URL sets, validates the first 20 URLs and lists the rest as pending.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
