## Description: <br>
Search inside videos, generate summaries, and analyze video content using TwelveLabs video understanding AI. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[james-le-twelve-labs](https://clawhub.ai/user/james-le-twelve-labs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to work with TwelveLabs video understanding workflows, including video upload, indexing, search, summarization, chaptering, highlights, entity search, and embeddings. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can send selected videos, images, prompts, and analysis requests to TwelveLabs under the user's account. <br>
Mitigation: Use only organization-approved content and a scoped or revocable TwelveLabs API key; avoid confidential meetings, regulated data, or private recordings unless the provider and retention model are approved. <br>
Risk: Search and analysis results depend on successful asynchronous indexing and can be incomplete if used before assets are ready. <br>
Mitigation: Poll indexed asset status until it is ready before running search, analysis, entity search, or embedding retrieval. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/james-le-twelve-labs/twelvelabs-video-intelligence) <br>
- [TwelveLabs Documentation](https://docs.twelvelabs.io) <br>
- [TwelveLabs API Reference](https://docs.twelvelabs.io/reference) <br>
- [TwelveLabs Homepage](https://twelvelabs.io) <br>
- [TwelveLabs Python SDK](https://github.com/twelvelabs-io/twelvelabs-python) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown with Python and bash code blocks] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and TWELVE_LABS_API_KEY; video content must be indexed before search or analysis.] <br>

## Skill Version(s): <br>
1.0.2 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
