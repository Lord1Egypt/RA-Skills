## Description:

Compare research papers by retrieving full PDFs from titles, URLs, or files and synthesizing differences, strengths, weaknesses, and evidence-backed trade-offs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[quqxui](https://clawhub.ai/user/quqxui)

### License/Terms of Use:

MIT-0

## Use Case:

Researchers, developers, and analysts use this skill to compare multiple research papers from titles, URLs, or uploaded PDFs. It is intended for evidence-backed side-by-side analysis of methods, results, strengths, weaknesses, limitations, and comparability caveats.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The agent may search the web, open paper links, retrieve PDFs, or read PDFs supplied by the user.

Mitigation: Prefer trusted scholarly sources such as arXiv, OpenReview, ACL Anthology, publisher pages, or uploaded files, and avoid unknown or private-network URLs.

Risk: PDF extraction issues or mismatched experimental settings can make paper comparisons misleading.

Mitigation: Require usable full-text evidence, label extraction quality, and avoid direct metric comparisons when datasets, tasks, baselines, or protocols differ.

## Reference(s):

- [Evidence Policy](references/evidence-policy.md)
- [Memory Dimensions](references/memory-dimensions.md)
- [ClawHub Skill Page](https://clawhub.ai/quqxui/skills/research-paper-compare)

## Skill Output:

**Output Type(s):** [text, markdown, guidance]

**Output Format:** [Markdown with comparison tables, analytical synthesis, and confidence notes]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Requires full PDF evidence for every paper before substantive comparison; reports blockers when full text is unavailable.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
