## Description: <br>
Tinyfish helps agents search the web, fetch URLs, read pages, extract information, and automate browser interactions when live web content is needed. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[tinyfish](https://clawhub.ai/user/tinyfish) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use Tinyfish to gather current web information, read pages, produce source-backed answers, extract structured data, and automate websites through the TinyFish CLI. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can give an agent broad authority to use API-authenticated web search and browser automation. <br>
Mitigation: Use it only in contexts where authenticated web access is acceptable, and review planned website interactions before execution. <br>
Risk: Browser automation may affect accounts, private pages, forms, purchases, or other sensitive workflows. <br>
Mitigation: Require explicit user confirmation before login, form submission, account changes, purchases, automated scraping, or actions on private pages. <br>
Risk: The skill requires sensitive TinyFish credentials. <br>
Mitigation: Provide credentials through approved secret handling, avoid exposing API keys in prompts or logs, and rotate credentials if disclosure is suspected. <br>


## Reference(s): <br>
- [ClawHub Tinyfish release page](https://clawhub.ai/tinyfish/tinyfish) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Markdown, JSON, Shell commands, Guidance] <br>
**Output Format:** [Markdown, JSON, and command-line output] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TinyFish CLI authentication through TINYFISH_API_KEY or login for API-authenticated web search and browser automation.] <br>

## Skill Version(s): <br>
1.0.6 (source: server release evidence) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
