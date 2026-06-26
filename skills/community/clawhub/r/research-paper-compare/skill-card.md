## Description: <br>
Compare research papers by retrieving full PDFs from titles, URLs, or files and synthesizing differences, strengths, weaknesses, and evidence-backed trade-offs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[quqxui](https://clawhub.ai/user/quqxui) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users and developers use this skill to compare multiple research papers from titles, URLs, or uploaded PDFs. It is designed to produce evidence-backed comparison tables and concise synthesis only after full PDF text is available for every paper. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill may search the web, open paper links, and download or extract PDF text. <br>
Mitigation: Use public academic sources and avoid private URLs or confidential PDFs unless they are intended to be processed for comparison. <br>
Risk: Paper comparisons can be misleading when PDF text is unavailable, extraction quality is weak, or evaluation protocols differ. <br>
Mitigation: Block comparisons without usable full PDF text, mark evidence quality, and avoid direct metric comparison when datasets, baselines, or protocols differ. <br>


## Reference(s): <br>
- [Input Handling](input-handling.md) <br>
- [Comparison Schema](comparison-schema.md) <br>
- [Output Patterns](output-patterns.md) <br>
- [Evidence Policy](references/evidence-policy.md) <br>
- [Memory Dimensions](references/memory-dimensions.md) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Guidance] <br>
**Output Format:** [Markdown with an acquisition summary, comparison table, analytical synthesis, and confidence notes] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires readable full PDF text for each paper before substantive comparison.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata; artifact frontmatter says 0.1.0) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
