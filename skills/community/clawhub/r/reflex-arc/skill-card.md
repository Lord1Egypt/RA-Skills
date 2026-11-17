## Description:

Reflex Arc adds automatic pre-response checks that help AI agents catch contradictions, scope drift, hallucinated specifics, overengineering, tone mismatch, and risky recommendations before replying.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jcools1977](https://clawhub.ai/user/jcools1977)

### License/Terms of Use:


## Use Case:

Developers and agent users install Reflex Arc to apply lightweight self-review to substantive answers, code guidance, option choices, and multi-step workflows before output is delivered.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may change response style and scope across other skills because it applies broad self-review checks to most substantive replies.

Mitigation: Install it only when broad answer-quality review is desired, and disable individual reflexes for sessions where a check conflicts with the task.

Risk: The skill can improve confidence calibration but does not independently verify facts or provide prompt injection protection.

Mitigation: Use source verification for time-sensitive or high-impact claims, and pair it with dedicated security controls when prompt injection defense is required.

## Reference(s):

- [Methodology](references/methodology.md)
- [Openlaw homepage](https://github.com/jcools1977/Openlaw)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text responses with optional shell diagnostic output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [No APIs, credentials, services, or persistent storage are required; the diagnostic script only checks local installation status.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
