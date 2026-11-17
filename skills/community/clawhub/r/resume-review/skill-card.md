## Description:

Reviews fall recruiting resumes with humorous, grounded feedback and generates a JOJO-style stand stat panel image.

This skill is ready for commercial/non-commercial use.

## Publisher:

[padepa](https://clawhub.ai/user/padepa)

### License/Terms of Use:

MIT

## Use Case:

External job seekers and agents use this skill to extract resume text, anonymize sensitive details, score six resume dimensions, generate humorous but grounded feedback, and render a shareable PNG panel.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Resume processing can expose unredacted personal, contact, identifier, company, or school details to the agent or to an external LLM provider.

Mitigation: Redact names, contact details, identifiers, company names, and school names locally before sending text to any model, then review the generated JSON and PNG for leaks.

Risk: The normal workflow uses mutable install or runtime dependencies.

Mitigation: Prefer pinned dependencies or an isolated environment without sensitive credentials.

## Reference(s):

- [resume-review ClawHub page](https://clawhub.ai/padepa/skills/resume-review)
- [Humor Style and Scoring Guide](references/humor-style.md)
- [Panel Data Generation Prompt](references/roast-prompt.md)
- [Intro Video Script](docs/intro-video-script.md)

## Skill Output:

**Output Type(s):** [text, json, shell commands, files, guidance]

**Output Format:** [Resume review guidance, panel JSON, shell commands, and a rendered PNG image]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires local anonymization before model use and review of the generated JSON and PNG for sensitive-data leaks.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 2.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
