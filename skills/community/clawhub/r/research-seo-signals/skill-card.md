## Description:

Compatibility entry for existing SignalDig SEO-research users that routes SEO evidence requests to the unified research-growth-signals Skill and its research_seo_signals tool.

This skill is ready for commercial/non-commercial use.

## Publisher:

[jerrykik](https://clawhub.ai/user/jerrykik)

### License/Terms of Use:

MIT-0

## Use Case:

External users and developers who still invoke the legacy SEO Signal Research skill use it to preserve SEO-research intent while delegating execution to the maintained SignalDig Growth Research skill.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The compatibility entry depends on the separate research-growth-signals skill and SignalDig MCP connection for actual SEO research.

Mitigation: Confirm that the unified skill and MCP connection are installed and trusted before use; stop rather than falling back to legacy SEO tools if they are unavailable.

Risk: Legacy SEO request or pagination parameters could be reused by mistake during migration.

Mitigation: Route SEO requests only through research-growth-signals and its current research_seo_signals tool contract.

## Reference(s):

- [SignalDig](https://signaldig.com/)
- [ClawHub skill page](https://clawhub.ai/jerrykik/skills/research-seo-signals)

## Skill Output:

**Output Type(s):** [guidance, text]

**Output Format:** [Markdown guidance]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Delegates to the unified research-growth-signals skill; produces no independent API contract, setup guide, parameter guide, or execution examples.]

## Skill Version(s):

1.8.7 (source: SKILL.md frontmatter and server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
