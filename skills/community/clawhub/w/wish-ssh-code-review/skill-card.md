## Description:

Reviews Wish SSH server code for proper middleware, session handling, and security patterns.

This skill is ready for commercial/non-commercial use.

## Publisher:

[anderskev](https://clawhub.ai/user/anderskev)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and engineers use this skill to review Charmbracelet Wish SSH server implementations for middleware order, host key handling, graceful shutdown, session handling, Bubble Tea integration, and security patterns.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: SSH key and password examples could be copied into production without adaptation.

Mitigation: Treat examples as review patterns, prefer public-key authentication, and verify secure host-key storage before applying guidance.

Risk: Code review findings may overstate issues if source evidence is incomplete.

Mitigation: Follow the skill's review gates and cite concrete file and line evidence before reporting a defect.

## Reference(s):

- [Server Setup](references/server.md)
- [Sessions & Security](references/sessions.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, guidance]

**Output Format:** [Markdown code review findings with file and line citations]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Findings are sequenced by review gates and tied to the included reference material.]

## Skill Version(s):

2.3.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
