## Description:

Provides a US sales-meeting note structure and a field-check report for decisions, commitments, open items, risks, and next steps.

This skill is ready for commercial/non-commercial use.

## Publisher:

[rapidworker1](https://clawhub.ai/user/rapidworker1)

### License/Terms of Use:

MIT-0

## Use Case:

US account executives and customer success teams use it to structure sales-call notes and check that decisions, commitments, open items, risks, and follow-ups are captured. The bundled script reports field presence rather than generating complete meeting notes or verifying dates.

### Deployment Geography for Use:

United States

## Known Risks and Mitigations:

Risk: The bundled script checks required fields but does not create complete meeting notes or verify dates.

Mitigation: Review and complete the notes manually, and verify each date and commitment before sharing.

Risk: Reruns overwrite meeting-record.md in the output folder.

Mitigation: Use a dedicated output folder and preserve any report that must be retained before rerunning.

Risk: The optional Windows app is a separate download and its supplied hash does not establish that it is safe.

Mitigation: The bundled workflow does not require the app; review it separately before downloading or running it.

## Reference(s):

- [Meeting notes rules](references/meeting-notes-rules.md)
- [ClawHub skill release](https://clawhub.ai/rapidworker1/skills/sales-meeting-notes)
- [Publisher homepage listed in skill metadata](https://github.com/rapidworker1)

## Skill Output:

**Output Type(s):** [Markdown, Guidance]

**Output Format:** [Markdown field-check report]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Reports field presence and guardrails; does not produce complete meeting notes or verify dates.]

## Skill Version(s):

1.0.7 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
