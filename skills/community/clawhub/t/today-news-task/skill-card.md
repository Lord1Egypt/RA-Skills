## Description: <br>
Fetches major Chinese news portal pages and summarizes domestic, international, and technology headlines, with optional handoff to today-task for publishing results. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[lzh2607](https://clawhub.ai/user/lzh2607) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Agents use this skill to gather current headline candidates from specified public news portals, filter duplicates and low-quality items, and prepare a structured Markdown briefing. It is intended for users who want a concise news digest covering domestic, international, and technology topics. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill makes outbound requests to public news or search pages and may expose requested URLs and raw page HTML to the agent session. <br>
Mitigation: Keep fetches limited to trusted public sources and avoid private, credentialed, or sensitive URLs. <br>
Risk: The optional publishing workflow depends on a separate today-task skill with its own authorization and behavior. <br>
Mitigation: Review and configure today-task separately before enabling publishing. <br>
Risk: Fetched pages can contain stale, duplicated, promotional, or misleading items. <br>
Mitigation: Apply the documented filtering rules, prefer stable article links, and preserve source attribution in the Markdown output. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/lzh2607/today-news-task) <br>
- [today-task optional integration](https://clawhub.ai/skills/today-task) <br>
- [today-task domestic mirror](https://cn.clawhub-mirror.com/skills/today-task) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown briefing with linked headlines, short summaries, sources, and times] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include status content for optional today-task publishing.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
