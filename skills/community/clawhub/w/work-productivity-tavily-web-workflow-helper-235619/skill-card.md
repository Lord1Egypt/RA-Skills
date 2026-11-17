## Description:

Helps AI-agent users, skill authors, maintainers, and teams turn Tavily-style web workflow needs into practical plans, checklists, analysis, code changes, or decision support.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

External AI-agent users, skill authors, maintainers, and teams use this skill to structure Tavily-style web search and workflow tasks into actionable local-hardware-friendly outputs. It is suited for bug fixing, setup hardening, reliability improvements, adjacent skill creation, and repeatable work-productivity workflows.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill may activate too broadly for generic web-search or workflow requests because its trigger language is broad.

Mitigation: Narrow trigger keywords and invocation examples so the skill is used for Tavily-style workflow support only when that context is clear.

Risk: Workflow, checklist, or code guidance can be incomplete or mismatched to the user's actual setup.

Mitigation: State assumptions, ask only for missing information that materially changes the output, and validate the result against explicit success criteria before use.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-235619)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Hacker News Workflow Demand Signal](https://news.ycombinator.com/item?id=49003232)
- [V2EX Work Productivity Demand Signal](https://www.v2ex.com/t/1229141)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown or plain text with optional code blocks, shell commands, configuration snippets, checklists, and verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Outputs should state assumptions, visible limits, validation performed, and remaining risks when relevant.]

## Skill Version(s):

0.20260729.110214 (source: ClawHub release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
