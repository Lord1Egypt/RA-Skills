## Description:

TopHotCN helps an agent fetch TopHub hot-list items for supported Chinese and international sites into JSON files, then optionally fetch article body content as Markdown.

This skill is ready for commercial/non-commercial use.

## Publisher:

[hanqiudeng](https://clawhub.ai/user/hanqiudeng)

### License/Terms of Use:

MIT-0

## Use Case:

Developers and content-focused agents use this skill to collect public trending-topic metadata from TopHub-supported sites and enrich selected items with fetched page content for downstream reading, summarization, or analysis.

### Deployment Geography for Use:

Global

## Known Risks and Mitigations:

Risk: The article-content fetcher can browse any URL present in a local JSON file.

Mitigation: Run it in an isolated environment or restricted network context, and use trusted TopHub-generated JSON inputs.

Risk: Running the content fetcher without an output path modifies the original JSON files.

Mitigation: Use the --output option when preserving originals matters, or keep a backup before batch fetching.

Risk: Runtime dependencies are installed from package managers and are not pinned by the artifact.

Mitigation: Pin and review dependencies before installation in managed or production environments.

## Reference(s):

- [TopHub Today](https://tophub.today)
- [Crawl4AI](https://github.com/unclecode/crawl4ai)
- [ClawHub skill page](https://clawhub.ai/hanqiudeng/skills/tophot-chinese)

## Skill Output:

**Output Type(s):** [Shell commands, Files, Markdown, Guidance]

**Output Format:** [JSON files containing hot-list metadata and optional Markdown article content, plus command-line guidance for running the included scripts]

**Output Parameters:** [1D]

**Other Properties Related to Output:** [The content fetcher can update source JSON files in place unless an output path is supplied.]

## Skill Version(s):

1.0.0 (source: server release evidence)

## Ethical Considerations:

Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment.
