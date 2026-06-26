## Description: <br>
Scrape any business website and generate 5 Meta-ready ad variants matching the brand's voice. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[chapagainashutosh8](https://clawhub.ai/user/chapagainashutosh8) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, marketers, and business operators use this skill to turn authorized business website content into Meta-ready ad copy, creative direction, targeting, and scheduling suggestions. It can generate ads from a URL, scrape site text for inspection, or generate ads from already-scraped content. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Website content, generated ad context, or submitted URLs may be sent to Apify and OpenAI. <br>
Mitigation: Use the skill only for websites you own or are authorized to analyze, and review data-sharing expectations before submitting site content. <br>
Risk: The security summary reports an under-disclosed mode for abusive ad copy. <br>
Mitigation: Remove or disable the offensive tone before installing or using the skill in normal workflows. <br>
Risk: Civic access tokens and related credentials may be exposed if handled in browser-facing code or committed accidentally. <br>
Mitigation: Keep tokens server-side, avoid exposing Civic access tokens to the browser, and never commit real API keys or access tokens. <br>
Risk: Scraped website content may remain in the local .cache directory. <br>
Mitigation: Clear the local .cache directory when scraped content should not remain on disk. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/chapagainashutosh8/skill2ads) <br>
- [Apify Website Content Crawler](https://apify.com/apify/website-content-crawler) <br>
- [Apify](https://apify.com) <br>
- [Civic](https://www.civic.com) <br>
- [OpenAI](https://openai.com) <br>
- [OpenClaw](https://openclaw.ai) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, configuration, guidance] <br>
**Output Format:** [Markdown-like text with structured ad variants, brand analysis, targeting, scheduling, and optional export guidance] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Each ad includes hook, body, CTA, visual direction, strategic rationale, Meta-compatible targeting, and daypart scheduling.] <br>

## Skill Version(s): <br>
1.0.1 (source: server release metadata and skill.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
