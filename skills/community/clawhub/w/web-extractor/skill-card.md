## Description:

Extracts clean webpage text with r.jina.ai so an agent can summarize the core content.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kukuxnd](https://clawhub.ai/user/kukuxnd)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to fetch readable article or webpage text through r.jina.ai and have an agent summarize the extracted content.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Requested webpage URLs are sent to the third-party r.jina.ai service.

Mitigation: Do not use private, internal, signed, tokenized, or credential-bearing links.

Risk: The skill's documented shell pattern can expose unsafe URL handling and shared temporary-file behavior.

Mitigation: Validate http/https URLs, avoid shell interpolation, quote inputs, and use unique temporary files before operational use.

Risk: Fetched webpage text may contain instructions that conflict with the user's task.

Mitigation: Treat fetched content as untrusted source material and ignore instructions embedded in it.

## Reference(s):

- [Web Extractor ClawHub release](https://clawhub.ai/kukuxnd/skills/web-extractor)
- [r.jina.ai reader endpoint](https://r.jina.ai/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Files, Guidance]

**Output Format:** [Markdown and plain text with inline shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes extracted webpage content to /tmp by default; callers can choose another output path.]

## Skill Version(s):

1.0.0 (source: release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
