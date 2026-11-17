## Description:

Scholar Deep Research runs an eight-phase scholarly research workflow across OpenAlex, arXiv, Crossref, and PubMed to produce structured reports with deduplication, transparent ranking, citation chasing, self-critique, and verifiable citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[agents365-ai](https://clawhub.ai/user/agents365-ai)

### License/Terms of Use:

MIT-0

## Use Case:

External users, developers, and research teams use this skill to turn scholarly questions into cited literature reviews, systematic or scoping reviews, comparative analyses, and grant background sections.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill can automatically update its own code from Git.

Mitigation: Prefer a package-manager install or set SCHOLAR_SKIP_UPDATE_CHECK=1 before use; if using a git-clone install, review and pin commits before accepting updates.

Risk: The skill can run another locally discovered skill script and accepts PAPER_FETCH_SCRIPT and direct PDF URLs as trusted inputs.

Mitigation: Use trusted local scripts and PDF URLs only, and review the configured inputs before execution.

Risk: The skill contacts scholarly services and writes research state in the workspace.

Mitigation: Install only when this network and workspace-write behavior is acceptable, and run dependencies in a dedicated virtual environment.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/agents365-ai/skills/scholar-deep-research)
- [Scholar Deep Research Documentation](https://agents365-ai.github.io/scholar-deep-research/)
- [Source Selection](references/source_selection.md)
- [Search Strategies](references/search_strategies.md)
- [Quality Assessment](references/quality_assessment.md)
- [Report Templates](references/report_templates.md)
- [Pitfalls](references/pitfalls.md)

## Skill Output:

**Output Type(s):** [text, markdown, shell commands, configuration, code, guidance]

**Output Format:** [Structured Markdown reports with citations, bibliography exports, JSON command envelopes, and shell commands for the research workflow.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create research_state.json, report files, bibliography exports, and PDF text extraction outputs in the workspace.]

## Skill Version(s):

0.5.0 (source: server release evidence and SKILL.md frontmatter metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
