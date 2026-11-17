## Description:

Provides structured argumentation tools that help language-model agents analyze claims, premises, conclusions, objections, and rebuttals through an external API.

This skill is ready for commercial/non-commercial use.

## Publisher:

[alinklab](https://clawhub.ai/user/alinklab)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers can use this skill to structure complex arguments into claims, premises, conclusions, objections, rebuttals, and synthesis steps. It is suited for analyzing competing perspectives, ethical questions, policy proposals, and scientific hypotheses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requires an API key and stores it in a plaintext local .env file.

Mitigation: Use a scoped or disposable key, keep the workspace private, and rotate the key if it may have been exposed.

Risk: The skill sends requests to the XiaoBenYang service and can be redirected by configuration.

Mitigation: Install only when the service is trusted and review endpoint configuration before use.

Risk: The included tools.py has a syntax error, so the skill may fail as packaged.

Mitigation: Validate and fix the package before relying on the skill in an agent workflow.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/alinklab/skills/structured-argumentation)
- [XiaoBenYang Service](https://xiaobenyang.com)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown summaries derived from JSON API responses]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires an XBY_APIKEY value; raw upstream JSON is summarized for the user.]

## Skill Version(s):

1.0.1 (source: server release metadata; artifact frontmatter lists 1.0.0)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
