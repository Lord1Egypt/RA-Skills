## Description:

Fetch and summarize latest Singapore Pools TOTO results from official Singapore Pools data files for normal, cascade, hongbao, and special draws.

This skill is ready for commercial/non-commercial use.

## Publisher:

[bluesneed](https://clawhub.ai/user/bluesneed)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agents use this skill to retrieve the latest Singapore Pools TOTO winning numbers, draw details, Group 1 prize, winning shares, and official source URL in text or JSON form.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled Python script makes outbound requests to singaporepools.com.sg for public lottery result data.

Mitigation: Install only in environments where that outbound access is acceptable; prefer domain-scoped network permissions for stronger governance.

Risk: Result parsing depends on Singapore Pools endpoint filenames and HTML classes remaining stable.

Mitigation: If parsing fails, verify the official source URL and update the endpoint mapping or parser selectors before relying on results.

## Reference(s):

- [Singapore Pools Toto Result Sources](references/source-endpoints.md)
- [Singapore Pools TOTO Results Page](https://www.singaporepools.com.sg/en/product/pages/toto_results.aspx)
- [Singapore Pools Lottery Output Archive](https://www.singaporepools.com.sg/DataFileArchive/Lottery/Output/)

## Skill Output:

**Output Type(s):** [text, JSON, shell commands, guidance]

**Output Format:** [Plain text or JSON returned by a Python command]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Includes draw type, source URL, retrieval timestamp, draw date, draw number, winning numbers, additional number, Group 1 prize, single-draw page URL, and winning shares when available.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
