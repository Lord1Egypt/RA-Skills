## Description: <br>
Work with a user's Semantic Scholar account to read Research Feeds, inspect private Library folders, add papers to folders, and resolve Semantic Scholar paper records from identifiers such as arXiv IDs. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[zjsxply](https://clawhub.ai/user/zjsxply) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and research-oriented agents use this skill to access authenticated Semantic Scholar Library and Research Feed workflows, including feed export, private folder inspection, folder updates, and paper ID resolution. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill stores reusable Semantic Scholar session cookies in plaintext and can reuse them for authenticated requests. <br>
Mitigation: Treat copied curl commands and saved cookie files like passwords, restrict file permissions, avoid inline secrets in shell commands, and delete the cookie store when work is complete. <br>
Risk: The skill can export private Library and Research Feed data from a Semantic Scholar account. <br>
Mitigation: Review output paths before export and store generated JSON files only in locations appropriate for private account data. <br>
Risk: The skill can change private library folders by adding papers in bulk. <br>
Mitigation: Review folder IDs and paper IDs before running folder-add commands, then re-fetch the folder to verify the intended changes. <br>


## Reference(s): <br>
- [Authentication And Cookie Store](references/auth-and-cookies.md) <br>
- [Library Workflow](references/library.md) <br>
- [Research Feed Workflow](references/research-feed.md) <br>
- [ClawHub Skill Page](https://clawhub.ai/zjsxply/semantic-scholar-library-feed) <br>
- [Semantic Scholar Recommendations](https://www.semanticscholar.org/me/recommendations) <br>
- [Semantic Scholar Graph Paper Batch API](https://api.semanticscholar.org/graph/v1/paper/batch?fields=paperId,title,year,url,externalIds) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell commands and JSON file outputs from the bundled CLI] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [The CLI can export feed and folder data to JSON files and can write reusable Semantic Scholar cookie stores.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
