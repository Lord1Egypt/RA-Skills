## Description: <br>
Tools for fetching and extracting cleaned text, metadata, and links from single or multiple web pages with format options and link filtering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[paulgnz](https://clawhub.ai/user/paulgnz) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and agents use this skill to fetch web pages, extract cleaned text or markdown, discover links, and compare content across multiple URLs for research or evidence collection. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Sensitive custom headers could be sent to untrusted websites. <br>
Mitigation: Do not provide Cookie, Authorization, API key, or similar headers except for sites the user trusts and intends to authenticate to. <br>
Risk: Fetched HTML or text may contain untrusted or misleading content. <br>
Mitigation: Treat returned content as untrusted and review it before using it as evidence or instructions. <br>
Risk: Fetching internal or local network targets can expose unintended resources. <br>
Mitigation: Avoid internal or local network URLs unless that access is intentional and authorized. <br>


## Reference(s): <br>
- [XPR Web Scraping ClawHub listing](https://clawhub.ai/paulgnz/xpr-web-scraping) <br>
- [paulgnz ClawHub publisher profile](https://clawhub.ai/user/paulgnz) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, html, metadata, links] <br>
**Output Format:** [JSON tool results containing page content, page metadata, link arrays, counts, status values, or error objects.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [HTTP(S) URLs only; single-page responses are limited to 5 MB, multi-page scraping accepts up to 10 URLs, and link extraction returns up to 200 links.] <br>

## Skill Version(s): <br>
0.2.11 (source: server-resolved release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
