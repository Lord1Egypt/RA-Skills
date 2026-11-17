## Description:

Research Engine helps agents collect information from web, GitHub, and Moltbook sources, analyze trends, and generate structured research reports with development plan suggestions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[guogang1024](https://clawhub.ai/user/guogang1024)

### License/Terms of Use:

MIT

## Use Case:

Developers and agent operators use this skill to run recurring or on-demand research on technical topics, consolidate external signals, and turn findings into Markdown reports and staged development-plan guidance.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics can cause local files to be written outside the intended folder when topic values contain slashes or path traversal.

Mitigation: Set RESEARCH_DIR to a controlled directory and avoid or sanitize topic values containing slashes or path traversal before running the skill.

Risk: Browsing history is retained locally in browsing_history.md.

Mitigation: Use the skill only where external web research is allowed, avoid confidential topics or secrets, and review or clear local research history according to policy.

Risk: External web, GitHub, and Moltbook content may be incomplete, stale, or unreliable.

Mitigation: Review generated research reports and development-plan suggestions before using them for decisions or downstream implementation.

## Reference(s):

- [Research-engine ClawHub skill page](https://clawhub.ai/guogang1024/skills/research-engine)
- [Package repository link](https://www.moltbook.com/u/guogangAgent)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, guidance]

**Output Format:** [Markdown research reports with console status text and Python-callable result dictionaries]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Writes report files and browsing_history.md under RESEARCH_DIR; the artifact default is /home/vken/.openclaw/workspace/research.]

## Skill Version(s):

1.0.0 (source: server release metadata and artifact/package.json)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
