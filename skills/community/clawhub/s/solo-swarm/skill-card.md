## Description: <br>
Swarm launches three parallel research agents focused on market, user, and technical analysis to investigate an idea and synthesize findings into a research report. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[fortunto2](https://clawhub.ai/user/fortunto2) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers, founders, and agent users use Swarm to research product or project ideas quickly from market, user, and technical perspectives. It is suited for coordinated idea investigation, competitor discovery, user-sentiment review, feasibility analysis, and GO / NO-GO / PIVOT recommendations. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill grants agents broad Bash, web search, web fetch, local session search, knowledge-base search, and project-code search capabilities. <br>
Mitigation: Review and approve the plan before deep research begins, restrict Bash unless commands are explicitly approved, and specify which local sources may be searched. <br>
Risk: The generated docs/research.md report may include private project, local knowledge-base, or past-session information when those search tools are enabled. <br>
Mitigation: Review docs/research.md before sharing it outside the project and remove private, confidential, or unrelated local context. <br>
Risk: Market, user, and technical findings may rely on unverified web results or public comments. <br>
Mitigation: Check source links and distinguish quoted sentiment from validated evidence before using the GO / NO-GO / PIVOT recommendation for decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/fortunto2/solo-swarm) <br>
- [SearXNG Docker Tavily adapter](https://github.com/fortunto2/searxng-docker-tavily-adapter) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown research synthesis with task coordination notes and a docs/research.md report] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses three coordinated research perspectives and may use web search, web fetch, optional solograph MCP search tools, and local project or session search when available.] <br>

## Skill Version(s): <br>
1.6.0 (source: SKILL.md frontmatter and server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
