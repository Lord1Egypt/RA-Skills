## Description: <br>
zt-web-fetcher helps agents fetch webpage content by routing URLs through URL-to-Markdown services and returning readable text or Markdown. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[larriewong27](https://clawhub.ai/user/larriewong27) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agent users use this skill when an agent needs to retrieve public webpage content, such as search result pages, blog posts, or documentation, and convert it into readable Markdown or text. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Private, token-bearing, internal, or confidential URLs and fetched content may be processed by third-party conversion services. <br>
Mitigation: Use the skill mainly for public webpages and avoid submitting sensitive URLs or confidential page content to third-party converters. <br>
Risk: The optional Scrapling fallback requires installing an external package. <br>
Mitigation: Install Scrapling only after reviewing and approving the package source. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/larriewong27/zt-web-fetcher) <br>
- [markdown.new](https://markdown.new/) <br>
- [Jina Reader](https://r.jina.ai/) <br>
- [defuddle.md](https://defuddle.md/) <br>
- [Scrapling](https://github.com/D4Vinci/Scrapling) <br>


## Skill Output: <br>
**Output Type(s):** [Guidance, Markdown, Shell commands] <br>
**Output Format:** [Markdown with URL examples and optional shell commands] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Routes URLs through third-party conversion services; optional Scrapling fallback requires package installation.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
