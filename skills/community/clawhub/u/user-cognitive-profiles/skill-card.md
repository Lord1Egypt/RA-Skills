## Description:

Analyze ChatGPT conversation exports to discover cognitive archetypes, optimize AI-human communication patterns, and enable personalized agent interactions based on detected user profiles.

This skill is ready for commercial/non-commercial use.

## Publisher:

[sebastianffx](https://clawhub.ai/user/sebastianffx)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent users use this skill to analyze exported ChatGPT conversations locally, generate a cognitive profile, and apply selected communication preferences to OpenClaw or other agent configuration files.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill processes highly sensitive ChatGPT export data and may produce a derived communication profile.

Mitigation: Run the analysis locally, keep raw exports private, and review or redact the generated profile before sharing or persisting it.

Risk: Persisting profile details in SOUL.md, AGENTS.md, or another agent file can expose sensitive preferences or conversation-derived traits.

Mitigation: Copy only high-level, non-sensitive communication preferences into persistent agent configuration.

Risk: Custom archetype YAML changes analysis behavior and should not be treated as trusted input by default.

Mitigation: Inspect custom archetype files before use and avoid loading archetype YAML from untrusted sources.

Risk: The WildChat test script can access a remote dataset when run.

Mitigation: Do not run the WildChat test script unless remote dataset access is intentional.

## Reference(s):

- [Methodology](references/methodology.md)
- [ClawHub Skill Page](https://clawhub.ai/sebastianffx/skills/user-cognitive-profiles)

## Skill Output:

**Output Type(s):** [Analysis, JSON, Markdown, Shell commands, Configuration instructions, Guidance]

**Output Format:** [Markdown guidance with shell commands and generated JSON or prompt-snippet files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Runs locally on exported conversation JSON; optional custom archetype YAML and the WildChat test script require extra review before use.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
