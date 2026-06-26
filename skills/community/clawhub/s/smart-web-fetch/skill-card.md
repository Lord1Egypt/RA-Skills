## Description: <br>
Smart Web Fetch helps agents retrieve web pages as cleaned Markdown by routing URLs through Jina Reader, markdown.new, or defuddle.md, with fallback to raw content. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[Leochens](https://clawhub.ai/user/Leochens) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and external agent users use this skill when an agent needs to retrieve public web page content and work with cleaned Markdown instead of raw HTML. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Requested URLs and fetched content can be sent through third-party services, which may expose private dashboards, intranet pages, signed links, or URLs containing tokens. <br>
Mitigation: Use the skill only for public web pages unless URL restrictions, explicit consent controls, and handling rules for sensitive URLs are added. <br>
Risk: The artifact disables normal HTTPS certificate and hostname verification while fetching content. <br>
Mitigation: Re-enable standard HTTPS verification before using the skill in trusted or production workflows. <br>
Risk: Arbitrary URL fetching can reach localhost, intranet, or cloud metadata endpoints if the agent is given those URLs. <br>
Mitigation: Block localhost, private network ranges, cloud metadata addresses, and other internal targets before invoking the fetch scripts. <br>


## Reference(s): <br>
- [Smart Web Fetch ClawHub Page](https://clawhub.ai/Leochens/smart-web-fetch) <br>
- [Jina Reader endpoint pattern](https://r.jina.ai/http://{target}) <br>
- [markdown.new endpoint pattern](https://markdown.new/{target}) <br>
- [defuddle.md endpoint pattern](https://defuddle.md/{target}) <br>


## Skill Output: <br>
**Output Type(s):** [Markdown, JSON, Text] <br>
**Output Format:** [Markdown text by default, or JSON containing success, url, content, source, and error fields when requested.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Fetched URL content may be cleaned through third-party services before being returned to the agent.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
