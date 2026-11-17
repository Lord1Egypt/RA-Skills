## Description:

真实的人类 helps agents identify, analyze, and model individual users for personalized interaction.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wasinc](https://clawhub.ai/user/wasinc)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers use this skill to help an agent build, update, query, and validate user models for personalized responses.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can lead agents to create persistent user profiles that include sensitive personal or psychological inferences.

Mitigation: Use it only after clear user opt-in, allow users to inspect and delete all profile copies, and avoid storing sensitive inferences unless explicitly authorized.

Risk: Automatic profiling can overstate uncertain behavioral or personality conclusions.

Mitigation: Keep confidence and source notes with model entries, periodically ask users to confirm or correct the model, and remove stale or disputed information.

## Reference(s):

- [信息提取方法](references/extraction-methods.md)
- [人类建模理论框架](references/modeling-framework.md)

## Skill Output:

**Output Type(s):** [Text, Markdown, Configuration, Guidance]

**Output Format:** [Markdown and structured profile guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May guide creation of user profile files and relationship data in the agent workspace.]

## Skill Version(s):

1.0.0 (source: server release evidence, package.json, _meta.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
