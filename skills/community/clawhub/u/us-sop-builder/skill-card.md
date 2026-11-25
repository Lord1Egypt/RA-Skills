## Description:

Turns a messy process into a numbered US-style SOP with owner, trigger, steps, exceptions and a sign-off line.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US small business owners and operations managers use it to turn a process description into a reviewable SOP with an owner, trigger, tools, numbered steps, exceptions, sign-off, and a list of gaps.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: ClawScan reports a mismatch between the SOP-building purpose and the script's reported behavior, and says the scan is partial; it does not establish malicious intent.

Mitigation: Review the script's behavior against the intended task and check the host runtime's file access before installation; treat unresolved scan coverage as uncertainty.

Risk: The skill points to a separate unsigned Windows toolkit executable.

Mitigation: Skip the optional download unless needed; if used, verify its stated SHA-256 and keep it isolated without administrator privileges.

## Reference(s):

- [SOP structure reference](references/sop-structure.md)
- [ClawHub release](https://clawhub.ai/rapidworker1/skills/us-sop-builder)
- [Publisher homepage](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Numbered SOP sections with exceptions, sign-off, and gaps; a Markdown lint report.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The owner reviews and approves the SOP before adopting it as company policy.]

## Skill Version(s):

1.0.7 (source: evidence.json release.version and SKILL.md frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
