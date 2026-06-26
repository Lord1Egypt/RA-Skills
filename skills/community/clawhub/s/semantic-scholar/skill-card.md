## Description: <br>
Search, retrieve, and organize scholarly metadata with the Semantic Scholar APIs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Grenzlinie](https://clawhub.ai/user/Grenzlinie) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, researchers, and research assistants use this skill to choose the right Semantic Scholar API workflow, search papers and authors, fetch metadata in batches, get related-paper recommendations, and plan offline dataset pulls. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Research queries, paper identifiers, and author identifiers may be sent to Semantic Scholar. <br>
Mitigation: Avoid sending sensitive research topics or private identifiers unless appropriate for the user's environment. <br>
Risk: Bundled scripts can write retrieved metadata to local JSONL or CSV files. <br>
Mitigation: Choose output paths deliberately and delete exports containing sensitive research topics when no longer needed. <br>
Risk: API key authentication is supported for repeated or larger jobs. <br>
Mitigation: Keep SEMANTIC_SCHOLAR_API_KEY private and avoid committing environment files or command histories that expose it. <br>


## Reference(s): <br>
- [Semantic Scholar API Overview](references/api-overview.md) <br>
- [Graph API](references/graph-api.md) <br>
- [Recommendations API](references/recommendations-api.md) <br>
- [Datasets API](references/datasets-api.md) <br>
- [Query Recipes](references/query-recipes.md) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Code, Shell commands, Configuration, Files] <br>
**Output Format:** [Markdown guidance with Python and shell command examples; bundled scripts can produce JSONL and CSV exports.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May call Semantic Scholar APIs and write local research exports; API key authentication uses SEMANTIC_SCHOLAR_API_KEY when available.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
