## Description: <br>
Performs Google searches through the Serper.dev API and returns rich results for web, news, images, videos, places, shopping, scholar, patents, and search suggestions. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[minilozio](https://clawhub.ai/user/minilozio) <br>

### License/Terms of Use: <br>
MIT <br>


## Use Case: <br>
Developers and agent users use this skill to let an agent retrieve Google Search results and related search verticals through Serper.dev, with optional filters for time range, country, language, result count, page, and scholar year. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Search queries are sent to Serper.dev and Google-backed infrastructure. <br>
Mitigation: Do not submit secrets, private customer data, proprietary project names, or regulated information unless organizational policy allows that provider. <br>
Risk: Shopping searches consume 2 Serper.dev credits instead of 1 credit. <br>
Mitigation: Use shopping only when the user explicitly asks for prices or shopping results, and monitor the returned credit balance. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/minilozio/serper-google-search) <br>
- [Serper.dev API Reference](artifact/references/serper-api.md) <br>
- [Serper.dev](https://serper.dev) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, JSON] <br>
**Output Format:** [Formatted search-result text with links and snippets, or raw JSON when --json is requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Includes result metadata such as knowledge graph, answer box, people-also-ask, related searches, and credit balance when returned by Serper.dev.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release evidence and package.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
