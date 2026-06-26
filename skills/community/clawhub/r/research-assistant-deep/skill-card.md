## Description: <br>
Deep research and synthesis assistant for investigating topics across multiple sources, comparing findings, producing structured research reports, and doing multi-step web research with citation tracking. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[terrycarter1985](https://clawhub.ai/user/terrycarter1985) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Researchers, analysts, developers, and other external users use this skill to structure multi-source investigations, track citations, compare evidence, and synthesize findings into briefings, tables, or research reports. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Fetched web pages and search results may contain inaccurate, outdated, biased, or misleading information. <br>
Mitigation: Treat fetched pages as untrusted source material, compare independent sources, and verify important conclusions from cited sources before relying on them. <br>
Risk: Search queries and fetched content can expose sensitive private data if users include it in research prompts. <br>
Mitigation: Do not include sensitive private data in search queries or fetched-source analysis unless the environment and data handling policy explicitly allow it. <br>


## Reference(s): <br>
- [Deep Dive Research Pattern](references/deep-dive.md) <br>
- [Credibility Scoring Helper](scripts/credibility.py) <br>
- [ClawHub Skill Page](https://clawhub.ai/terrycarter1985/research-assistant-deep) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, guidance, shell commands] <br>
**Output Format:** [Markdown research report with citations, findings, contradictions, source lists, and optional command guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Uses web search and fetch tools; users should verify important conclusions from cited sources.] <br>

## Skill Version(s): <br>
1.0.0 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
