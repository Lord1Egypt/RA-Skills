## Description:

Discover hidden APIs behind web pages and replace expensive browser snapshots with lightweight API calls.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ianzlm](https://clawhub.ai/user/ianzlm)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and automation engineers use this skill to find read-oriented APIs behind web pages and replace large browser snapshots with focused API calls for structured data extraction.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can inspect and sample authenticated API data from pages opened while logged in.

Mitigation: Use only on user-approved sites and avoid sensitive account, billing, profile, admin, or authentication endpoints.

Risk: Discovered API paths and response details may expose sensitive implementation or data-access information if saved broadly.

Mitigation: Review discovered API details before adding them to another skill, persistent notes, or shared documentation.

Risk: Direct API calls can become brittle when undocumented endpoints, parameters, or environments change.

Mitigation: Test each environment separately, verify returned field counts, and keep browser snapshot behavior as a fallback.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/ianzlm/skills/snapshot-to-api)
- [Publisher Profile](https://clawhub.ai/user/ianzlm)
- [Snapshot vs API: Detailed Comparison](references/comparison.md)

## Skill Output:

**Output Type(s):** [guidance, code, shell commands]

**Output Format:** [Markdown with inline JavaScript and browser command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May produce API endpoint notes, response-shape summaries, extraction snippets, and fallback guidance.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
