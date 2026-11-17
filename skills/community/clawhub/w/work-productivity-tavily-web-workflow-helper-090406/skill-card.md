## Description:

Helps agent users and skill authors plan, debug, harden, and validate Tavily-style web-search productivity workflows on ClawHub.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and agent users use this skill to turn Tavily-style web-search productivity needs into practical plans, checklists, code changes, setup guidance, and validation notes.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad implicit trigger wording for Tavily and web-search workflow requests.

Mitigation: Narrow or disable implicit triggers if the skill should run only for explicit Tavily or web-search workflow requests.

Risk: Generated workflow or implementation guidance could be incorrect or incomplete for a user's environment.

Mitigation: Review the proposed plan, code, commands, and validation notes before applying them to production workflows.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub release page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-090406)
- [Ontology ClawHub demand signal](https://clawhub.ai/skills/ontology)
- [GitHub ClawHub demand signal](https://clawhub.ai/skills/github)
- [Multi Search Engine ClawHub demand signal](https://clawhub.ai/skills/multi-search-engine)
- [Weather ClawHub demand signal](https://clawhub.ai/skills/weather)
- [Agent Browser ClawHub demand signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Obsidian ClawHub demand signal](https://clawhub.ai/skills/obsidian)
- [AdMapix ClawHub demand signal](https://clawhub.ai/skills/admapix)
- [Tavily Search ClawHub demand signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [PollyReach ClawHub demand signal](https://clawhub.ai/skills/pollyreach)
- [V2EX workflow demand signal](https://www.v2ex.com/t/1229328)
- [Ask HN API reliability demand signal](https://news.ycombinator.com/item?id=49003232)
- [GitHub issue reliability demand signal](https://github.com/legend-esc/carbonchain/issues/508)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with checklists, plans, code snippets, shell commands, configuration examples, and validation notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, remaining risks, and next-step notes when useful.]

## Skill Version(s):

0.1.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
