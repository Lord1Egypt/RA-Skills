## Description:

Find Buddhist temples, Taoist shrines, Confucian temples, and sacred sites with etiquette guidance, visiting-hour context, meditation opportunities, and Fliggy-powered travel booking support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[dingtom336-gif](https://clawhub.ai/user/dingtom336-gif)

### License/Terms of Use:

MIT-0

## Use Case:

External users can use this skill to ask an agent for temple, shrine, monastery, and sacred-site discovery in supported cities, with Markdown summaries based on flyai CLI results. The skill also supports related travel-planning outputs such as booking links, itinerary context, and service options when returned by the CLI.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill directs agents to install an unpinned third-party npm CLI globally.

Mitigation: Preinstall a reviewed and pinned version of the flyai CLI in an isolated environment instead of allowing automatic global installation.

Risk: The skill depends on external Fliggy/flyai travel queries and commercial booking links in outputs.

Mitigation: Use it only where external travel-service calls and booking-link presentation are acceptable, and review output links before relying on them.

## Reference(s):

- [Temple Guide on ClawHub](https://clawhub.ai/dingtom336-gif/skills/temple-guide)

## Skill Output:

**Output Type(s):** [Text, Markdown, Shell commands, Guidance]

**Output Format:** [Markdown with comparison tables and booking links derived from flyai CLI output]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should match the user's language and include booking links for listed results when available.]

## Skill Version(s):

3.2.0 (source: frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
