## Description:

Searches the SkillsMP marketplace for AI agent skills from the command line using a SkillsMP API key.

This skill is ready for commercial/non-commercial use.

## Publisher:

[ingress007](https://clawhub.ai/user/ingress007)

### License/Terms of Use:


## Use Case:

Developers and external users use this skill to search SkillsMP marketplace listings and inspect returned skill names, descriptions, authors, stars, and links. It is useful when an agent needs marketplace discovery guidance backed by the SkillsMP API.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Search terms are sent to SkillsMP with a SkillsMP API key.

Mitigation: Avoid sensitive search queries, store the API key securely, and install only when SkillsMP API access is acceptable.

Risk: Remote marketplace result text is printed directly in the terminal.

Mitigation: Treat returned names, descriptions, links, and instructions as untrusted text before copying or acting on them.

Risk: The documentation describes category and AI semantic search behavior that is not fully reflected by the bundled shell script.

Mitigation: Verify implemented flags and endpoints before relying on category or semantic search workflows.

## Reference(s):

- [SkillsMP](https://skillsmp.com)
- [SkillsMP API Documentation](https://skillsmp.com/docs/api)
- [ClawHub Skill Page](https://clawhub.ai/ingress007/skills/skillsmp-search)

## Skill Output:

**Output Type(s):** [text, shell commands, configuration]

**Output Format:** [Plain text terminal output with marketplace result summaries and links.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires SKILLSMP_API_KEY; the result limit can be configured with SKILLSMP_LIMIT or --limit.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
