## Description: <br>
Resolve one or more paper titles to reliable arXiv papers using Tavily search, then fetch compact arXiv metadata and abstracts with a local helper script. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[red0orange](https://clawhub.ai/user/red0orange) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and analysts use this skill to resolve supplied paper titles to canonical arXiv records, fetch title-author-abstract metadata, and leave a reusable JSONL log plus Markdown report. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The workflow uses Tavily search and requests to arxiv.org, so results depend on external service availability and returned search quality. <br>
Mitigation: Run the lookup only when those external requests are acceptable, process titles sequentially, and record errors or no_match results instead of guessing. <br>
Risk: The skill runs local Python helper scripts and writes fetched metadata into the selected work directory. <br>
Mitigation: Use a deliberate WORKDIR, keep generated files inside that folder, and review paper_fetches.jsonl and paper_fetch_report.md before relying on them. <br>


## Reference(s): <br>
- [Examples](examples.md) <br>
- [arXiv](https://arxiv.org/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, files, guidance] <br>
**Output Format:** [Markdown report with JSONL process log and compact JSON metadata from helper scripts] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Writes input_titles.md, paper_fetches.jsonl, and paper_fetch_report.md under the chosen WORKDIR.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
