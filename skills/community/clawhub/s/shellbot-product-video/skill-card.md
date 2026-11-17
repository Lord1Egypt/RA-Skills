## Description:

Creates conversion-focused product marketing videos with Remotion and React using the AIDA framework, with optional Freepik-generated supporting assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[cohnen](https://clawhub.ai/user/cohnen)

### License/Terms of Use:


## Use Case:

Developers and marketing teams use this skill to turn product briefs into AIDA scripts, scene plans, Remotion projects, asset manifests, and render commands for launch videos, paid social ads, app promos, SaaS explainers, or product teasers.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Product briefs or generated assets may be shared with external services such as Freepik, ElevenLabs, Kling, AWS, or Google Cloud.

Mitigation: Review inputs and generated assets before sharing them with external services or publishing them.

Risk: Remotion/npm dependencies and generated code can affect CI reproducibility or introduce ordinary supply-chain risk.

Mitigation: Use a normal project sandbox, pin dependencies for CI or sensitive work, and review generated code and commands before execution.

Risk: Marketing videos can contain misleading claims if a brief or generated script overstates product outcomes.

Mitigation: Apply the skill's QA gate to verify the problem, solution, use cases, CTA, incentive, and proof signals before rendering or publication.

## Reference(s):

- [Remotion Product Video Playbook](references/remotion-product-video-playbook.md)
- [Remotion Rules Index](references/remotion-rules-index.md)
- [Freepik Ancillary Assets](references/freepik-ancillary-assets.md)
- [Template Showcase](references/template-showcase.md)
- [ShellBot Team](https://getshell.ai)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown, JSON, React/TypeScript code, shell commands, and configuration files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces an AIDA script draft, plan.json, a customized Remotion project, an asset manifest, and final render commands.]

## Skill Version(s):

1.0.0 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
