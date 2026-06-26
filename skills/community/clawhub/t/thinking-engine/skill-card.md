## Description: <br>
A bilingual deep-analysis skill that gathers current web evidence, examines a topic through 11 lenses, and produces a grounded scenario simulation with findings and open questions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[h7g7](https://clawhub.ai/user/h7g7) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users, developers, analysts, strategists, researchers, and decision-makers use this skill to examine complex questions, challenge assumptions, compare tradeoffs, and simulate likely outcomes from multiple angles. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow may use web search, which can be inappropriate for confidential or sensitive prompts. <br>
Mitigation: Avoid using the skill with confidential prompts, and keep searches to public, non-paywalled, non-private sources. <br>
Risk: The optional OpenClaw hook can over-trigger on broad words such as analyze. <br>
Mitigation: Enable the hook only when automatic reminders are desired, and disable it if it activates too often. <br>
Risk: Scenario simulations involving real people can be mistaken for factual claims. <br>
Mitigation: Clearly label simulated dialogue and behavior as fictional inference and avoid private individuals without clear public relevance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/h7g7/thinking-engine) <br>
- [The 11 Lenses - Deep Reference Guide](references/lenses-guide.md) <br>
- [Simulation Guide - Building Worlds That Reveal Truth](references/simulation-guide.md) <br>
- [Example Output](assets/example-output.md) <br>
- [OpenClaw Hook](hooks/openclaw/HOOK.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown analysis with evidence summary, lens-by-lens findings, narrative simulation, and final synthesis] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Responses should cite gathered sources, limit web searches to six queries, match the user's language, and label simulations of real people as fictional inference.] <br>

## Skill Version(s): <br>
1.0.1 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
