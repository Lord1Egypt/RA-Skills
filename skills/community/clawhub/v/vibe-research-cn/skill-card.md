## Description:

Conduct AI-led research with autonomous literature review, hypothesis generation, analysis, and synthesis while human provides vision.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jirboy](https://clawhub.ai/user/jirboy)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, analysts, and teams use this skill to turn a research question into a structured AI-led workflow for literature review, gap identification, hypothesis generation, analysis design, execution, and synthesis. The human provides scope and validation while the agent gathers sources, drafts research artifacts, cites claims, and flags uncertainty.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics may be searched online and fetched from external sources, which can expose sensitive or proprietary details if included in the prompt.

Mitigation: Approve the research plan carefully and remove secrets, confidential data, or regulated information before allowing web research.

Risk: The artifact describes offline or no-cloud operation while also documenting web_search and web_fetch research workflows.

Mitigation: Treat the skill as capable of networked research unless the runtime explicitly disables web tools.

Risk: AI-led synthesis can produce incorrect, biased, or weakly supported conclusions.

Mitigation: Require citations, cross-check important claims across multiple sources, review methodology, and keep human validation before relying on final findings.

## Reference(s):

- [Vibe Research ClawHub Skill Page](https://clawhub.ai/jirboy/skills/vibe-research-cn)
- [Research Pipeline](artifact/pipeline.md)
- [Deep Research Quick Reference](artifact/quickref.md)
- [Risk Mitigation](artifact/risks.md)
- [Deep Research Example Workflow](artifact/example.md)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown research plans, analyses, reports, citations, confidence annotations, and reproducibility notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses human checkpoints before scope confirmation, research execution, and final report review.]

## Skill Version(s):

1.0.0 (source: frontmatter and server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
