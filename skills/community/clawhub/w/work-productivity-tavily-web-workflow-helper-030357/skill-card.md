## Description:

Helps agent users, skill authors, maintainers, and teams create practical Tavily-style web search productivity workflows, including plans, checklists, implementation support, reliability improvements, and safety hardening.

This skill is ready for commercial/non-commercial use.

## Publisher:

[kyro-ma](https://clawhub.ai/user/kyro-ma)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, skill authors, maintainers, and teams use this skill to turn Tavily-style web search workflow needs into concrete plans, artifacts, checklists, code changes, configuration guidance, or decision support. It is aimed at repeatable productivity workflows that remain feasible on ordinary local hardware.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill has broad routing language and may activate on generic web, search, or API requests.

Mitigation: Confirm that the user's request is specifically about Tavily-style search workflows, productivity workflow planning, implementation support, reliability, or safety hardening before applying the skill.

Risk: Search-provider workflows built from the skill's guidance may expose secrets or confidential data if users include sensitive inputs.

Mitigation: Keep credentials and confidential information out of prompts, queries, logs, examples, and generated workflow artifacts unless the user has explicitly provided a secure handling requirement.

## Reference(s):

- [Requirement Plan](references/requirement-plan.md)
- [ClawHub Skill Page](https://clawhub.ai/kyro-ma/skills/work-productivity-tavily-web-workflow-helper-030357)
- [Tavily Search Demand Signal](https://clawhub.ai/skills/openclaw-tavily-search)
- [Multi Search Engine Demand Signal](https://clawhub.ai/skills/multi-search-engine)
- [Agent Browser Demand Signal](https://clawhub.ai/skills/agent-browser-clawdbot)
- [Hacker News Web Access Signal](https://news.ycombinator.com/item?id=48985198)
- [V2EX Deployment Workflow Signal](https://www.v2ex.com/t/1228978)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown with optional code blocks, shell commands, configuration snippets, checklists, and concise verification notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May include assumptions, remaining risks, and next steps when they materially help the user act on the result.]

## Skill Version(s):

0.20260729.110214 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
