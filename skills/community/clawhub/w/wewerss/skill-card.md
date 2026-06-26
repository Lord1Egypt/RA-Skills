## Description: <br>
Subscribe to WeChat public-account and RSS sources through WeWeRSS, then fetch raw article content for agent-built daily digests. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[eggyrooch-blip](https://clawhub.ai/user/eggyrooch-blip) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill to configure a trusted WeWeRSS instance, create channels, add feed or site sources, and retrieve recent raw article data or Atom feeds for downstream summarization, classification, or daily digest generation with their own LLM. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The configured WeWeRSS instance may process submitted URLs and article data, including private or internal sources. <br>
Mitigation: Use a trusted WeWeRSS instance and submit only sources that are intended for that instance to process. <br>
Risk: Delete commands can remove sources from a channel if the wrong channel or source ID is used. <br>
Mitigation: Verify channel and source IDs before running delete commands. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/eggyrooch-blip/wewerss) <br>
- [WeWeRSS homepage](https://github.com/punkpeye/wewerss) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, Shell commands, API calls, Configuration guidance] <br>
**Output Format:** [Markdown with inline bash commands and JSON API examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires curl, jq, and a trusted WEWERSS_BASE_URL.] <br>

## Skill Version(s): <br>
1.0.0 (source: frontmatter and release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
