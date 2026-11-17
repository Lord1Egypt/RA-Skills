## Description:

Keeps company and competitor context current by reviewing their public websites and news, then proposing dated updates in a pull request.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cargo-ai](https://clawhub.ai/user/cargo-ai)

### License/Terms of Use:

MIT-0

## Use Case:

Growth, marketing, and revenue operations teams use it to seed and refresh a shared company context repository from public company and competitor pages and news. Weekly findings are evidence-tagged and proposed in a pull request for human review.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: A setup path may download and run an unpinned package without confirmation, and one file was only partially inspected by the security scan.

Mitigation: Review the setup instructions and package source before execution, pin the package version where possible, and inspect the partially covered file.

## Reference(s):

- [Skill documentation](https://github.com/getcargohq/gtm-skills/tree/main/web-capture)
- [Cargo GTM skills project homepage](https://github.com/getcargohq/gtm-skills)
- [ClawHub release](https://clawhub.ai/cargo-ai/skills/web-capture)

## Skill Output:

**Output Type(s):** [Files, Markdown, Pull requests]

**Output Format:** [Markdown files and a pull request]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Weekly, evidence-tagged proposals; the first run seeds the context repository.]

## Skill Version(s):

0.2.0 (source: skill frontmatter, server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
