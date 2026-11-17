## Description:

Helps student innovation teams search for similar patents, identify potential patentable aspects, choose an invention or utility-model direction, and prepare a disclosure outline.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ip930](https://clawhub.ai/user/ip930)

### License/Terms of Use:

MIT-0

## Use Case:

Student project teams use this skill for an initial patent search and to organize possible patentable points and a disclosure outline before consulting a campus intellectual-property office or patent professional. It is not a formal novelty search or patentability conclusion.

### Deployment Geography for Use:

Global; the described patent coverage includes China, the United States, Europe, Japan, South Korea, and WIPO.

## Known Risks and Mitigations:

Risk: Project details included in search queries may be sent outside the user's computer.

Mitigation: Decide which unpublished project details may leave the computer and avoid including confidential material unless approved.

Risk: Credential handling, request destinations, and redirects need review before use.

Mitigation: Use a limited PatentMax key and verify HTTPS, destination restrictions, and safe redirect handling before installing or running the skill.

Risk: Retrying a timed-out full-patent request may create unexpected charges if billing or retry behavior is unclear.

Mitigation: Check account charges and confirm timeout/retry billing guidance before retrying; review the account balance after the request.

## Reference(s):

- [ClawHub skill release](https://clawhub.ai/ip930/skills/student-project-patent)
- [PatentMax API reference](references/api-reference.md)
- [Patent search workflow](references/search-workflow.md)
- [Query syntax](references/query-syntax.md)
- [PatentMax account and API platform](https://api.ip930.com/features/api-platform)

## Skill Output:

**Output Type(s):** [Analysis, Markdown, CSV, Guidance]

**Output Format:** [Chinese Markdown patent analysis and an Excel-compatible CSV comparison table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Preliminary patent-search results only; the workflow does not cover academic papers, and recent unpublished applications may not be visible.]

## Skill Version(s):

1.0.0 (source: frontmatter)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
