## Description:

Analyzes seed-tray images or videos to count emerged seedlings and estimate germination rate against the number of seeds sown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[18072937735](https://clawhub.ai/user/18072937735)

### License/Terms of Use:

MIT-0

## Use Case:

Growers, seed companies, and nursery operators use this skill to assess seedling emergence from tray images or videos, estimate germination rates, and review past analysis reports.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Images, videos, URLs, and report metadata are sent to the lifeemergence cloud service.

Mitigation: Review the material and service privacy terms before using the skill; avoid submitting sensitive content.

Risk: The skill silently creates or reuses an identity and can retrieve reports linked to it.

Mitigation: Use a dedicated identity or isolated workspace and review account-linked report access.

Risk: A local SQLite database and stored service tokens may persist in shared workspaces.

Mitigation: Restrict workspace access and manage the database and tokens before sharing or disposing of the workspace.

## Reference(s):

- [Skill API reference](references/api_doc.md)
- [Skill demonstration](https://lifeemergence.com/sample.html)
- [ClawHub skill listing](https://clawhub.ai/18072937735/skills/smyx-seed-germination-rate-prediction-analysis)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Structured analysis report or JSON; historical reports as a Markdown table]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include germination counts and rates, report links, and an optionally saved output file.]

## Skill Version(s):

1.0.17 (source: ClawHub release; skill frontmatter lists 1.0.12)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
