## Description: <br>
Uses ScholarGraph v1.4 and later to run an end-to-end cancer fusion gene literature research workflow, including search, deduplication, information extraction, report generation, and Excel table creation. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Josephyb97](https://clawhub.ai/user/Josephyb97) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Researchers, clinical bioinformatics teams, and developers use this skill to structure cancer fusion gene literature searches, merge and deduplicate findings, and produce review reports and Excel summaries with traceable references. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses external AI and search providers and requires API credentials. <br>
Mitigation: Use scoped API keys, store them outside committed files, and only enable providers intended for the research environment. <br>
Risk: Generated literature summaries and fusion gene tables can contain incomplete or incorrect biomedical claims. <br>
Mitigation: Review source PMIDs, references, and generated reports before using outputs for research, clinical, or product decisions. <br>
Risk: The workflow installs or uses the xlsx dependency and writes reports to local output directories. <br>
Mitigation: Review or pin the dependency before installation and confirm output paths before running report-generation scripts. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/Josephyb97/scholargraph-cancer-fusiongenes-research-flow) <br>
- [Europe PMC PDF access pattern](https://europepmc.org/articles/PMC[ID]?pdf=render) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Code, Shell commands, Configuration, Files, Guidance] <br>
**Output Format:** [Markdown guidance with bash and JavaScript snippets; generated workflow files include JSON, Markdown reports, downloaded PDFs, and XLSX spreadsheets.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires bun, node, AI_PROVIDER, and MINIMAX_API_KEY; ScholarGraph download flows may also use SERPER_API_KEY.] <br>

## Skill Version(s): <br>
1.3.0 (source: ClawHub release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
