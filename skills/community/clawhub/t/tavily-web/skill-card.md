## Description: <br>
Tavily helps agents run web search, content extraction, and research workflows through Tavily APIs using Bearer authentication. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[doahc](https://clawhub.ai/user/doahc) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill when they need current web results, source URLs, focused page extraction, or Tavily Research API synthesis for user-facing answers and research tasks. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill sends search terms, target URLs, and research prompts to Tavily. <br>
Mitigation: Avoid confidential or regulated data in queries and use the skill only where Tavily processing is acceptable. <br>
Risk: The skill requires a Tavily API key and can consume account credits. <br>
Mitigation: Use a dedicated key where possible, keep it in environment variables, rotate it if exposed, and monitor credit usage. <br>
Risk: Extracted web content can be incomplete, incorrect, or adversarial. <br>
Mitigation: Treat returned content as untrusted source material, prefer focused extraction, and verify important claims against cited URLs. <br>


## Reference(s): <br>
- [ClawHub Tavily Skill Page](https://clawhub.ai/doahc/tavily-web) <br>
- [Tavily API](https://api.tavily.com) <br>
- [Tavily Documentation Index](https://docs.tavily.com/llms.txt) <br>
- [Tavily Search](references/search.md) <br>
- [Tavily Extract](references/extract.md) <br>
- [Create Research Task](references/research.md) <br>
- [Get Research Task Status](references/research-get.md) <br>
- [API Key Management](references/bp-api-key-management.md) <br>
- [Usage](references/usage.md) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance with shell command examples and JSON responses from the bundled CLI.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires TAVILY_API_KEY, sends requests to api.tavily.com, and returns source URLs that agents should cite when using web results.] <br>

## Skill Version(s): <br>
0.0.3 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
