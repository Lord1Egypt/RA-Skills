## Description:

Perform authorized security tests to detect, exploit, and validate defenses against SQL injection vulnerabilities in web applications.

This skill is ready for commercial/non-commercial use.

## Publisher:

[brandonwise](https://clawhub.ai/user/brandonwise)

### License/Terms of Use:


## Use Case:

Security testers, penetration testers, and application security engineers use this skill during authorized assessments to identify SQL injection behavior, validate exploitability, and check whether defenses are effective.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill includes SQL injection payloads that can extract credentials or database metadata if used outside an authorized assessment.

Mitigation: Use only with written authorization, defined scope, and non-production or approved test data; stop testing if real user data appears.

Risk: Out-of-band callback payloads can exfiltrate database details to external infrastructure.

Mitigation: Use only organization-controlled callback infrastructure and only when OOB testing is explicitly permitted by the engagement scope.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/brandonwise/skills/sql-injection-testing)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, guidance]

**Output Format:** [Markdown with SQL payload examples, testing checklists, and defensive validation guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs may include exploit payloads and should be used only within written authorization and defined engagement scope.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
