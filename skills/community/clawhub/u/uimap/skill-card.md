## Description:

Provides accurate URLs and step-by-step click paths for completing tasks on websites.

This skill is ready for commercial/non-commercial use.

## Publisher:

[delai](https://clawhub.ai/user/delai)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and agents use Uimap to find website URLs and step-by-step click paths before performing tasks in web applications.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Setup instructions include an unverified remote installer path and an unpinned global CLI install.

Mitigation: Review the installer before use, prefer a pinned and verifiable npm package version in an isolated environment, and avoid the CDN curl-to-shell path.

Risk: Using the service may send website-task queries to UIMap during authenticated search workflows.

Mitigation: Only log in and submit queries when the task and target website details are acceptable to share with the UIMap service.

## Reference(s):

- [@refore-ai/uimap on npm](https://www.npmjs.com/package/@refore-ai/uimap)
- [Uimap ClawHub skill page](https://clawhub.ai/delai/skills/uimap)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands]

**Output Format:** [Text or Markdown with shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include website URLs, ordered click instructions, and optional domain-scoped search commands.]

## Skill Version(s):

0.1.9 (source: artifact/SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
