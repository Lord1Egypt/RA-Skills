## Description:

Guides agents through ScholarGraph-based cancer fusion-gene literature research, including search, deduplication, information extraction, report writing, and Excel table generation.

This skill is ready for commercial/non-commercial use.

## Publisher:

[josephyb97](https://clawhub.ai/user/josephyb97)

### License/Terms of Use:


## Use Case:

Researchers, clinical genomics analysts, and developers use this skill to run a structured ScholarGraph workflow for cancer fusion-gene literature review, probe-design context, biomarker research, and tabular report generation.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Literature-research data may be sent to MiniMax or another configured AI provider during use.

Mitigation: Confirm the configured provider is acceptable for the data being processed before running the workflow.

Risk: API keys may be exposed if committed, logged, or copied into shared artifacts.

Mitigation: Keep provider keys in environment variables or local secret storage and avoid including them in reports, logs, or source files.

Risk: Spreadsheet generation depends on an unpinned `xlsx` package.

Mitigation: Pin or lock the dependency version and review updates before installation.

Risk: Fixed workspace output paths can retain sensitive research documents or generated reports.

Mitigation: Use controlled output directories and apply cleanup and access controls for sensitive literature or research outputs.

Risk: Generated cancer fusion-gene summaries may contain incomplete or outdated biomedical claims.

Mitigation: Require qualified human review of extracted evidence, PMIDs, frequencies, clinical significance, and drug information before clinical or business use.

## Reference(s):

- [ClawHub skill page](https://clawhub.ai/josephyb97/skills/scholargraph-cancer-fusiongenes-research-flow)
- [Europe PMC article PDF access pattern](https://europepmc.org/articles/PMC[ID]?pdf=render)
- [MiniMax API endpoint](https://api.minimaxi.com/v1)
- [Artifact skill definition](artifact/SKILL.md)
- [Artifact workflow](artifact/FLOW.md)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown guidance with shell commands and JavaScript code; generated workflow outputs include JSON search results, Markdown reports, and Excel workbooks.]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires bun, node, AI_PROVIDER, and MINIMAX_API_KEY; generated Excel workbooks organize fusion-gene summaries, probe-design recommendations, and cancer-type summaries.]

## Skill Version(s):

1.3.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
