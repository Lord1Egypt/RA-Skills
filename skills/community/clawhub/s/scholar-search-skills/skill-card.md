## Description: <br>
Scholar Search Skills helps agents search, filter, download, score, and summarize academic papers from sources such as arXiv, ICLR, ICML, and NeurIPS, including BibTeX citation output. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[WOWCharlotte](https://clawhub.ai/user/WOWCharlotte) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Researchers, students, and developer agents use this skill to collect literature for a topic, score paper relevance, organize PDFs, and produce summaries, paper lists, BibTeX citations, and optional literature review outlines. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Broad or sensitive research topic names may create revealing local folder paths under ~/papers. <br>
Mitigation: Confirm the output folder before use and avoid sensitive path names. <br>
Risk: The workflow may propose pip, npx, or download commands for dependencies and PDFs. <br>
Mitigation: Review commands before execution and prefer a virtual environment or non-global install. <br>
Risk: Downloaded PDFs and generated notes may include irrelevant or rights-sensitive material. <br>
Mitigation: Use the workflow for research collection, review selected papers before saving or sharing, and keep summaries and citations traceable to their sources. <br>


## Reference(s): <br>
- [Summary Template](references/summary_template.md) <br>
- [BibTeX Template](references/bibtex_template.md) <br>
- [arXiv Search](https://arxiv.org/search/) <br>
- [ICLR 2025 OpenReview](https://openreview.net/group?id=ICLR.cc/2025/Conference) <br>
- [NeurIPS Proceedings](https://proceedings.neurips.cc/) <br>
- [Proceedings of Machine Learning Research](https://proceedings.mlr.press/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance, files] <br>
**Output Format:** [Markdown research notes, BibTeX entries, JSON scoring results, local PDF files, and shell command snippets] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Creates organized local research outputs such as PAPER_LIST.md, PAPER_SUMMARIES.md, references.bib, scored_papers.json, and PDF folders under the chosen papers directory.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
