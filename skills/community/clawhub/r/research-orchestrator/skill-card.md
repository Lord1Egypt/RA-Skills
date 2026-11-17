## Description:

A bilingual deep-research workflow that helps agents plan multi-source research, evaluate source credibility, and produce structured Markdown research reports.

This skill is ready for commercial/non-commercial use.

## Publisher:

[tobewin](https://clawhub.ai/user/tobewin)

### License/Terms of Use:

MIT-0

## Use Case:

Developers, analysts, and agent users can use this skill to organize market, competitive, industry, or general research into a repeatable workflow with source tracking and Markdown report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Research topics and queries may be sent to external search or content services.

Mitigation: Use only approved search providers and network policy, and avoid confidential topics unless those providers are acceptable.

Risk: The skill includes shell command templates and security evidence flags risky shell and unpinned npm execution paths.

Mitigation: Review commands before execution, pin package versions, and run the skill in a restricted workspace.

Risk: The security summary says the skill overstates its capabilities, and generated reports may be incomplete or unsupported.

Mitigation: Require source review, citation checks, and clear marking of gaps before using reports for decisions.

Risk: Generated task and report files are written into workspace paths.

Mitigation: Validate output paths and task identifiers before writing files, especially in shared workspaces.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/tobewin/skills/research-orchestrator)
- [Publisher profile](https://clawhub.ai/user/tobewin)
- [arXiv API](http://export.arxiv.org/api/query)
- [DuckDuckGo Instant Answer API](https://api.duckduckgo.com/)
- [Wikipedia REST API](https://en.wikipedia.org/api/rest_v1/)

## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Guidance]

**Output Format:** [Markdown reports, structured research notes, JSON progress data, and optional shell command examples]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Produces bilingual research reports and may create local task, research, analysis, and output files under a deep-research workspace.]

## Skill Version(s):

2.0.1 (source: frontmatter and server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
