## Description:

Search, retrieve, and organize scholarly metadata with the Semantic Scholar APIs.

This skill is ready for commercial/non-commercial use.

## Publisher:

[grenzlinie](https://clawhub.ai/user/grenzlinie)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and researchers use this skill to choose Semantic Scholar API workflows, search papers and authors, fetch records in batches, retrieve related-paper recommendations, and plan offline dataset pulls.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The bundled workflows may contact Semantic Scholar APIs and use an optional API key.

Mitigation: Use a scoped Semantic Scholar API key when provided and avoid exposing it in prompts, logs, or shared output files.

Risk: The bundled scripts can write JSONL and CSV research outputs to local paths.

Mitigation: Choose output paths deliberately, review generated files before sharing, and preserve raw results for provenance.

Risk: The scripts rely on Python packages such as requests and optional pandas.

Mitigation: Install dependencies in an isolated environment and prefer pinned package versions for repeatable use.

## Reference(s):

- [Semantic Scholar API Overview](references/api-overview.md)
- [Graph API](references/graph-api.md)
- [Recommendations API](references/recommendations-api.md)
- [Datasets API](references/datasets-api.md)
- [Query Recipes](references/query-recipes.md)
- [Semantic Scholar bulk paper search endpoint](https://api.semanticscholar.org/graph/v1/paper/search/bulk)
- [Semantic Scholar paper batch endpoint](https://api.semanticscholar.org/graph/v1/paper/batch)
- [Semantic Scholar author batch endpoint](https://api.semanticscholar.org/graph/v1/author/batch)
- [Semantic Scholar recommendations endpoint](https://api.semanticscholar.org/recommendations/v1/papers)

## Skill Output:

**Output Type(s):** [Guidance, Shell commands, Code, API Calls, Files, Configuration]

**Output Format:** [Markdown guidance with optional Python or shell commands that can produce JSONL and CSV files]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [May contact Semantic Scholar APIs and write local research output files when the bundled scripts are used.]

## Skill Version(s):

1.0.0 (source: server release metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
