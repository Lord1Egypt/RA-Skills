## Description:

Analyzes pet activity videos or video URLs for over-excitement behaviors, scores excitement level, and returns calming guidance, structured results, and report links.

This skill is ready for commercial/non-commercial use.

## Publisher:

[smyx-sunjinhui](https://clawhub.ai/user/smyx-sunjinhui)

### License/Terms of Use:

MIT-0

## Use Case:

External users and agent developers use this skill to process pet-area footage for excitement monitoring, calming guidance, and history report lookup in homes, boarding centers, daycare, or training settings.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Pet-area videos or video URLs may contain sensitive household, facility, or identity-linked information and are sent to LifeEmergence cloud services for analysis.

Mitigation: Use only with informed consent, avoid highly sensitive footage, and confirm the deployment's data handling and retention expectations before installation.

Risk: The skill can create or reuse an internal identity and store service tokens in a local workspace database.

Mitigation: Run it in a controlled workspace, restrict filesystem access to the skill environment, and clear or rotate stored tokens when decommissioning the skill.

Risk: Calming-device actions such as speakers, lights, or pheromone devices are described as part of the workflow, but integrations may not be verified in the release evidence.

Mitigation: Treat device actions as recommendations unless each hardware integration is separately configured, tested, and supervised.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/smyx-sunjinhui/skills/smyx-excitement-calming-guide-analysis)
- [Skill demo](https://lifeemergence.com/sample.html)
- [Pet excitement API documentation](references/api_doc.md)
- [Shared analysis API documentation](skills/smyx_analysis/references/api_doc.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown text with JSON-style structured analysis and report links]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Can save analysis output to a file when the optional output path is used.]

## Skill Version(s):

1.0.8 (source: ClawHub release metadata; artifact SKILL.md frontmatter states 1.0.11)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
