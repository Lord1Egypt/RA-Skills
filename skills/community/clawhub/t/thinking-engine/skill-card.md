## Description:

Multi-Angle-Thinking helps agents perform deep, evidence-first analysis by gathering web data, applying 11 analytical lenses, and producing a grounded narrative simulation with findings and open questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[h7g7](https://clawhub.ai/user/h7g7)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, strategists, researchers, and decision-makers use this skill when they need a structured multi-angle analysis of a complex idea, decision, or scenario. It is especially suited to prompts asking the agent to challenge assumptions, surface hidden risks, compare perspectives, or simulate what could happen.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Optional hooks or session activators can steer agent behavior automatically when broad trigger phrases are present.

Mitigation: Prefer explicit invocation for deep analysis, review hook behavior before enabling it, and disable the hook when automatic reminders are not needed.

Risk: The skill encourages web research and realistic simulations that may involve sensitive topics or real people.

Mitigation: Use the documented guardrails: avoid private personal data, label real-person simulations as fictional inference, limit searches to public sources, and apply extra caution for sensitive topics.

## Reference(s):

- [README](artifact/README.md)
- [Example output](artifact/assets/example-output.md)
- [The 11 Lenses - Deep Reference Guide](artifact/references/lenses-guide.md)
- [Simulation Guide - Building Worlds That Reveal Truth](artifact/references/simulation-guide.md)
- [OpenClaw Hook](artifact/hooks/openclaw/HOOK.md)

## Skill Output:

**Output Type(s):** [analysis, markdown, guidance]

**Output Format:** [Markdown narrative with sourced intelligence, lens-by-lens analysis, scenario simulation, synthesis, and open questions]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include web-sourced facts, fictionalized simulation dialogue, and explicit uncertainty framing; the skill limits research to a maximum of 6 web searches per analysis.]

## Skill Version(s):

1.0.1 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
