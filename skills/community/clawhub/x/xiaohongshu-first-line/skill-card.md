## Description: <br>
Xiaohongshu First Line analyzes public Xiaohongshu profiles, recent posts, tags, comments, and search results to help a user discover shared interests and draft natural first messages. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[isolcat](https://clawhub.ai/user/isolcat) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
External users use this skill to browse or analyze Xiaohongshu profiles and posts, identify shared interests and communication style, and generate specific first-message options with follow-up guidance. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill uses a logged-in Xiaohongshu browser session to browse public profiles, capture screenshots, and profile real people. <br>
Mitigation: Use it only for explicit Xiaohongshu requests and public, user-selected targets; avoid private accounts, sensitive personal inferences, and unnecessary data retention. <br>
Risk: Generated outreach advice could support unwanted or repeated contact. <br>
Mitigation: Keep suggestions to genuine interest-based first messages, never send messages to profile owners automatically, and respect non-response without repeated follow-up. <br>
Risk: Keyword discovery can become broad people discovery with weak consent boundaries. <br>
Mitigation: Keep searches narrow, avoid bulk discovery, and let the requesting user choose which public profile to analyze before generating first-line advice. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/isolcat/xiaohongshu-first-line) <br>
- [Personality Analysis Framework](references/personality-framework.md) <br>
- [First Line Generation Framework](references/prompt-templates.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, guidance] <br>
**Output Format:** [Markdown response with profile analysis, screenshot/media references, ranked first-line suggestions, follow-up guidance, and browser command snippets when used by an agent.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include Xiaohongshu screenshots as media attachments during discovery and profile preview flows.] <br>

## Skill Version(s): <br>
0.1.0 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
