## Description: <br>
Analyze and generate robots.txt files with AI crawler awareness. Detect which AI bots (GPTBot, ClaudeBot, PerplexityBot, Google-Extended, etc.) are blocked or allowed on any website. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sharozdawa](https://clawhub.ai/user/sharozdawa) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers, site owners, and content teams use this skill to analyze robots.txt behavior for AI crawlers, generate crawler-specific rules, and audit existing robots.txt files for gaps or unintended crawler access. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Generated robots.txt rules can affect search visibility and AI crawler access if deployed without review. <br>
Mitigation: Review generated robots.txt content before deployment and confirm that each crawler rule matches the site owner's indexing and AI access policy. <br>
Risk: Analyzing a live site may require the agent to fetch a URL supplied by the user. <br>
Mitigation: Use the skill only with URLs the user intends the agent to access. <br>
Risk: Crawler user-agent lists may become outdated as AI crawlers change over time. <br>
Mitigation: Check crawler documentation periodically before relying on generated rules for production policy decisions. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sharozdawa/robotstxt-ai) <br>


## Skill Output: <br>
**Output Type(s):** [Analysis, Markdown, Configuration, Guidance] <br>
**Output Format:** [Markdown with robots.txt code blocks and concise explanations] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May include crawler allow/block summaries, suggested robots.txt rules, sitemap directives, and improvement recommendations.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
