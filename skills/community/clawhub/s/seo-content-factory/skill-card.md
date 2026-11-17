## Description:

Generates SEO-optimized blog posts and articles with keyword research, competitor analysis, SERP-aware structure, and on-page SEO assets.

This skill is ready for commercial/non-commercial use.

## Publisher:

[seanwyngaard](https://clawhub.ai/user/seanwyngaard)

### License/Terms of Use:


## Use Case:

External content marketers, SEO specialists, and client-service teams use this skill to draft SEO articles from a keyword or batch file, including metadata, schema markup, and linking suggestions.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The skill requests Bash access even though its SEO drafting workflow does not require shell execution.

Mitigation: Remove Bash from the allowed tools before installation unless a controlled batch-output workflow explicitly needs it.

Risk: The skill asks the agent to include statistics, implied sources, and first-person experience claims that may be unsupported.

Mitigation: Require explicit citations for statistics and forbid first-person testing or experience claims unless the user supplies evidence.

Risk: Batch mode writes generated articles and summaries to an output directory.

Mitigation: Run batch mode only in a controlled output directory where file creation and overwrites are acceptable.

## Reference(s):


## Skill Output:

**Output Type(s):** [Text, Markdown, Code, Configuration, Guidance]

**Output Format:** [Markdown articles, WordPress-ready HTML, YAML-style SEO metadata, JSON-LD schema markup, and batch summary files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Batch mode can write Markdown, HTML, and summary files under an output directory.]

## Skill Version(s):

1.0.0 (source: server-resolved release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
