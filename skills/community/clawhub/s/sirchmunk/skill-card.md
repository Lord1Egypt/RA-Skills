## Description:

Local file search using sirchmunk API. Use when you need to search for files or content by asking natural language questions.

This skill is ready for commercial/non-commercial use.

## Publisher:

[wangxingjun778](https://clawhub.ai/user/wangxingjun778)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and external users use this skill to issue natural-language searches against configured local files through Sirchmunk when they need relevant file or content matches without building an embedding database, index, or ETL pipeline.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: Broad local search paths or matched file contents could expose sensitive project files to the configured Sirchmunk backend or LLM endpoint.

Mitigation: Restrict SIRCHMUNK_SEARCH_PATHS and optional path arguments to approved project folders, and exclude secret, credential, and private data directories.

Risk: The skill depends on a local Sirchmunk service, package installation, and a configured LLM endpoint that may not be equally trusted in every environment.

Mitigation: Install only trusted and pinned Sirchmunk versions, run the service in an isolated environment, and use an approved LLM endpoint.

Risk: Free-form query and path inputs can affect wrapper behavior and the contents sent to the search API.

Mitigation: Use controlled query inputs for automated workflows and review path values before execution.

## Reference(s):

- [Sirchmunk homepage](https://github.com/modelscope/sirchmunk)

## Skill Output:

**Output Type(s):** [Text, Shell commands, Guidance]

**Output Format:** [Plain text or formatted JSON from the local Sirchmunk search API]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [Uses one natural-language query with optional search paths; results depend on the configured local Sirchmunk server, approved search paths, and LLM endpoint.]

## Skill Version(s):

1.0.0 (source: server release metadata and target metadata)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
