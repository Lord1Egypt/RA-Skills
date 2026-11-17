## Description:

Helps AI-agent users, skill authors, maintainers, and teams plan, build, harden, and validate multi-search-engine productivity workflows and adjacent skills.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

AI-agent users, skill authors, maintainers, and teams use this skill to turn multi-search-engine productivity needs into practical plans, checklists, analyses, code changes, configuration, or implementation support. It is aimed at improving reliability, hardening setup and safety, fixing bugs, and creating adjacent workflows that remain feasible on ordinary local hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad implicit activation wording may cause the skill to trigger during unrelated search or productivity requests.

Mitigation: Invoke the skill explicitly by name or narrow activation keywords before deployment in environments where accidental activation matters.

Risk: The skill produces guidance, plans, code changes, shell commands, and configuration that may be incorrect for a specific environment.

Mitigation: Review outputs before use, validate them against the stated success criteria, and test any code, commands, or configuration in a controlled environment.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-multi-search-workflow-helper-130443)
- [Popular ClawHub skill demand: ontology](https://clawhub.ai/skills/ontology)
- [Popular ClawHub skill demand: Multi Search Engine](https://clawhub.ai/skills/multi-search-engine)
- [Popular ClawHub skill demand: Agent Browser](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Popular ClawHub skill demand: Nano Banana Pro](https://clawhub.ai/skills/nano-banana-pro)
- [Popular ClawHub skill demand: Tavily Search](https://clawhub.ai/skills/openclaw-tavily-search)
- [How Google decided to Destroy its Search Monopoly](https://news.ycombinator.com/item?id=48945074)
- [Where is your GitHub network building from?](https://news.ycombinator.com/item?id=48945115)
- [roadmap: grappa scripting engine - Lua via Luerl](https://github.com/vjt/grappa-irc/issues/288)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with optional code, shell commands, configuration snippets, checklists, analysis, or decision support.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, visible limits, validation notes, and remaining risks when relevant.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
