## Description: <br>
Scrape AI chat conversations from ChatGPT, Gemini, Perplexity, Copilot, Google AI Mode, and Grok. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[scrapelesshq](https://clawhub.ai/user/scrapelesshq) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, analysts, AI SEO teams, and automation agents use this skill to collect structured responses, citations, links, and model metadata from supported LLM chat platforms through the Scrapeless API. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Prompts and returned task data are sent to Scrapeless and may include sensitive or confidential content. <br>
Mitigation: Do not send secrets, regulated personal data, or confidential business conversations unless approved for use with Scrapeless. <br>
Risk: The skill requires a Scrapeless API token for authenticated requests. <br>
Mitigation: Keep X_API_TOKEN scoped and protected, and monitor API usage for unexpected activity. <br>
Risk: Runtime dependencies are installed from Python packages. <br>
Mitigation: Install dependencies in an isolated environment with reviewed or pinned versions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/scrapelesshq/scrapeless-llm-chat-scraper-skill) <br>
- [Scrapeless homepage](https://www.scrapeless.com) <br>
- [Scrapeless LLM Scraper documentation](https://docs.scrapeless.com/en/llm-chat-scraper/quickstart/introduction/) <br>
- [Scrapeless ChatGPT scraper documentation](https://docs.scrapeless.com/en/llm-chat-scraper/scrapers/chatgpt/) <br>
- [Scrapeless Universal Scraping API documentation](https://docs.scrapeless.com/en/universal-scraping-api/) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, code, shell commands, configuration, guidance] <br>
**Output Format:** [JSON responses containing model-specific text, markdown, links, citations, status, task identifiers, and error objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires X_API_TOKEN and sends prompts to the Scrapeless API; task results are documented as available for 12 hours.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
