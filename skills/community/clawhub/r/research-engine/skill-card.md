## Description: <br>
Automates multi-source research, trend analysis, structured report generation, and development plan suggestions for agent workflows. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[guogang1024](https://clawhub.ai/user/guogang1024) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent builders use this skill to gather information from web, GitHub, and Moltbook sources, summarize trends, and produce Markdown research reports with short-, mid-, and long-term development suggestions. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics and query results may be sent to external sources and stored locally in reports or browsing history. <br>
Mitigation: Use the skill only for topics suitable for external search and local retention; avoid sensitive topics unless storage and sharing are acceptable. <br>
Risk: Recurring or autonomous integrations can run searches and write files without fresh user review. <br>
Mitigation: Enable scheduled use only with explicit limits on topics, frequency, storage location, and review expectations. <br>
Risk: Report filenames are derived from the research topic and the security guidance calls out unsafe report file handling. <br>
Mitigation: Sanitize topic-derived filenames and constrain report output to an approved research directory before deployment. <br>
Risk: Generated trend summaries and development plans can be incomplete or misleading. <br>
Mitigation: Treat generated reports as research drafts and review source quality, assumptions, and proposed actions before using them for planning. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/guogang1024/research-engine) <br>
- [Moltbook profile referenced by artifact metadata](https://www.moltbook.com/u/guogangAgent) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown reports, Python return objects, command-line status text, and local Markdown history files] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes reports and browsing history under RESEARCH_DIR, defaulting to /home/vken/.openclaw/workspace/research.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and artifact/package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
