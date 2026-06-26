## Description: <br>
A 6-step structured research skill that searches arXiv, converts selected papers to Markdown, uses an LLM to choose two papers, adds targeted web context, and writes a citation-backed five-bullet Markdown summary. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[goog](https://clawhub.ai/user/goog) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, developers, and technical analysts use this skill to turn an open-ended research topic into a concise Markdown summary grounded in selected arXiv papers and targeted web results. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research topics, selected paper text, and fetched webpage content are sent to outside services. <br>
Mitigation: Avoid confidential or proprietary topics, use limited-scope API keys, and only install when that external processing is acceptable. <br>
Risk: The skill includes advanced web-fetching behavior that may retrieve and cache external page content. <br>
Mitigation: Prefer a virtual environment and a user-local install path, review fetched sources before relying on summaries, and clear the /tmp/owl_papers cache after use. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/goog/q-research) <br>
- [arXiv API](https://export.arxiv.org/api/query) <br>
- [arXiv abstracts](https://arxiv.org/abs) <br>
- [arXiv PDFs](https://arxiv.org/pdf) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown research summary with selected paper links, five cited bullets, web source links, and an execution checklist.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May save the Markdown summary to a user-specified file; caches downloaded PDFs and converted Markdown under the configured papers directory.] <br>

## Skill Version(s): <br>
1.3.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
