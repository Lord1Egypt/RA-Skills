## Description:

Orchestrate a multi-agent virtual academic reading group for analyzing papers, challenging interpretations, and synthesizing integrated summaries with traceable citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[isonaei](https://clawhub.ai/user/isonaei)

### License/Terms of Use:


## Use Case:

External users, developers, and researchers use this skill to run structured virtual reading groups over academic papers, producing expert notes, discussion questions, responses, and a final thematic synthesis. It is intended for literature analysis where every substantive claim should remain tied to source documents.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill reads user-provided papers and creates multiple markdown outputs, which may expose sensitive research material if shared folders are reused.

Mitigation: Use a new dedicated output directory for each run and avoid placing sensitive papers in shared folders.

Risk: Large paper sets and high-end model choices can increase cost.

Mitigation: Confirm expected cost before using high-end models or processing large paper collections.

Risk: Generated literature notes or synthesis may contain incorrect or unsupported claims if source passages are unavailable.

Mitigation: Follow the skill's no-source policy: leave unsupported fields blank and require citations to exact paper sections or pages for substantive claims.

## Reference(s):

- [Virtual Reading Group ClawHub Page](https://clawhub.ai/isonaei/skills/virtual-reading-group)
- [Workflow Specification](references/workflow.md)
- [Default Personas](references/default-personas.md)
- [Paper Notes Template](references/paper-notes-template.md)
- [Synthesis Template](assets/synthesis-template.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown files and concise completion guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces multiple reading-group artifacts, including paper notes, expert summaries, junior discussion, expert responses, and an integrated discussion summary.]

## Skill Version(s):

1.1.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
