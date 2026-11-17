## Description:

Scholar Search Skills helps agents search, filter, download, and summarize academic papers from sources such as arXiv, ICLR, ICML, and NeurIPS, including structured summaries and BibTeX citations.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wowcharlotte](https://clawhub.ai/user/wowcharlotte)

### License/Terms of Use:

MIT

## Use Case:

Researchers, students, and developer agents use this skill to collect academic papers for literature reviews, score papers by keyword relevance, download PDFs, and produce organized paper lists, summaries, and citations.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Unpinned global third-party installs can introduce dependency and supply-chain risk.

Mitigation: Install dependencies manually in an isolated environment and verify the source before using global install commands.

Risk: Paper downloads and generated research files may be written into broad user-controlled directories.

Mitigation: Choose a dedicated storage location for downloaded PDFs and generated research files, then review outputs before reuse.

## Reference(s):

- [ClawHub Skill Page](https://clawhub.ai/wowcharlotte/skills/scholar-search-skills)
- [Summary Template](references/summary_template.md)
- [BibTeX Template](references/bibtex_template.md)
- [arXiv Search](https://arxiv.org/search/)
- [ICLR OpenReview](https://openreview.net/group?id=ICLR.cc/2025/Conference)
- [NeurIPS Proceedings](https://proceedings.neurips.cc/)
- [PMLR Proceedings](https://proceedings.mlr.press/)

## Skill Output:

**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance]

**Output Format:** [Markdown, BibTeX, JSON scoring output, CSV-compatible paper lists, and shell commands]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May create paper directories, downloaded PDFs, markdown summaries, BibTeX files, literature review outlines, and relevance-scoring JSON.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
