## Description: <br>
Run Tavily web search through AISA with filters for depth, topic, and time range. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[aisadocs](https://clawhub.ai/user/aisadocs) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill to run filtered Tavily web searches through AISA when recency, topic, depth, or time-range controls are needed. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The release is advertised as Tavily search, but the bundled runtime also exposes broader AISA search, extraction, and AI synthesis commands. <br>
Mitigation: Use the Tavily command path for Tavily searches, review available subcommands before use, and avoid invoking extraction or synthesis features unless they are intended. <br>
Risk: Search, extraction, sonar, and verity requests may send prompts, URLs, or retrieved content to AISA services. <br>
Mitigation: Do not send private URLs, internal documents, secrets, or sensitive prompts unless AISA's data handling is acceptable for the user's environment. <br>
Risk: The skill requires an AISA_API_KEY credential. <br>
Mitigation: Provide the key through the environment, keep it out of prompts and logs, and rotate it if exposure is suspected. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/aisadocs/tavily-search-aisa) <br>
- [AISA](https://aisa.one) <br>
- [AISA API endpoint](https://api.aisa.one/apis/v1) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Shell commands, Guidance] <br>
**Output Format:** [Command-line text output with search results, answers, citations, and usage details when returned by the API.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires python3 and an AISA_API_KEY environment variable.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and skill frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
