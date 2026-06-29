## Description: <br>
Access real-time public social media data from TikTok, Instagram, YouTube, Reddit, Twitter, Twitch, Snapchat, and Threads via EnsembleData's REST API. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[marktristy](https://clawhub.ai/user/marktristy) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, and researchers use this skill to guide authenticated EnsembleData REST API requests for public social media data, including platform endpoints, pagination, SDK examples, usage monitoring, and metered costs. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: API tokens can be exposed through query parameters in prompts, logs, or shared request URLs. <br>
Mitigation: Treat the EnsembleData token as a secret and redact full request URLs from logs, tickets, and shared prompts. <br>
Risk: Bulk collection of public social-media data may conflict with platform terms, privacy law, consent expectations, or retention policies. <br>
Mitigation: Confirm the intended use complies with applicable terms and policies, avoid unnecessary bulk collection, and define retention limits before use. <br>
Risk: Metered API calls can consume daily units or paid quota unexpectedly. <br>
Mitigation: Review endpoint unit costs before running bulk workflows and use the free account usage endpoints to monitor consumption. <br>


## Reference(s): <br>
- [ClawHub Skill Page](https://clawhub.ai/marktristy/skills/social-scraper-api) <br>
- [EnsembleData API Docs](https://ensembledata.com/apis/docs) <br>
- [EnsembleData Pricing](https://ensembledata.com/pricing) <br>
- [EnsembleData Python SDK](https://github.com/EnsembleData/ensembledata-python) <br>
- [EnsembleData Node.js SDK](https://github.com/EnsembleData/ensembledata-node) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Code, Shell commands, Configuration] <br>
**Output Format:** [Markdown guidance with endpoint tables and Python, Node.js, and shell command examples] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Describes JSON REST API requests and responses; no hidden execution or generated files.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
