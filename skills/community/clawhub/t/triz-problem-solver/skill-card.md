## Description:

Generate reviewable TRIZ innovation or TRIZ/DFMA cost-reduction concepts and expand a selected concept into a detailed solution by calling the PatSnap Solution Engine MCP endpoint over plain HTTP.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wwt1995](https://clawhub.ai/user/wwt1995)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and engineers use this skill to analyze product innovation, engineering contradiction, design improvement, manufacturing simplification, assembly optimization, and cost-reduction requests through TRIZ and DFMA workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill sends user-provided problem descriptions and product details to PatSnap/Eureka RD.

Mitigation: Disclose the external call before use and redact or avoid trade secrets, personal data, NDA-protected material, and export-controlled content unless policy permits submission.

Risk: Generated TRIZ or DFMA concepts may be incomplete, unsuitable, or misleading for a specific engineering context.

Mitigation: Treat outputs as reviewable concepts and require qualified engineering review before design, manufacturing, or procurement decisions.

Risk: Long-running service calls or transport failures can create ambiguity about whether a task is still processing.

Mitigation: Reuse the returned job identifier for stream and detail calls, and avoid starting a replacement task when delivery is ambiguous unless the user confirms.

## Reference(s):

- [ClawHub Skill Listing](https://clawhub.ai/wwt1995/skills/triz-problem-solver)
- [Eureka RD](https://eureka.patsnap.com/rd/#/agentic?type=triz&start_from=hub&utm_source=clawhub&utm_medium=skill_listing&utm_campaign=triz_innovation)

## Skill Output:

**Output Type(s):** [Text, Markdown, Guidance]

**Output Format:** [Markdown with structured TRIZ or DFMA analysis, candidate concepts, job and idea identifiers, and selected solution details when available]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include patent-backed concepts, implementation guidance, evaluations, scores, images, and localized Eureka RD follow-up text when returned or allowed by the workflow.]

## Skill Version(s):

1.0.11 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
