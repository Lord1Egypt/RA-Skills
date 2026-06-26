## Description: <br>
Scrapling Safe helps agents scrape and extract data from public web pages using HTTP, stealth, or browser-based fetching. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[linshuikeji](https://clawhub.ai/user/linshuikeji) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and agents use this skill for authorized scraping and extraction of publicly accessible web content, including selector-based extraction and saving results for later review. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill can fetch arbitrary URLs with stealth and browser modes, while public-only and robots.txt claims are usage guidance rather than enforced safeguards. <br>
Mitigation: Use only for authorized public web scraping, review target URLs before execution, and run in a network-restricted environment when internal services or credentials are reachable. <br>
Risk: Cloudflare-solving and stealth modes can violate site terms or authorization boundaries if used without permission. <br>
Mitigation: Disable these modes unless explicit permission exists and confirm scraping complies with site terms and robots.txt. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/linshuikeji/scrapling-safe) <br>


## Skill Output: <br>
**Output Type(s):** [text, markdown, shell commands, configuration, guidance] <br>
**Output Format:** [Markdown guidance and shell commands; saved scrape results may be JSON, text, or Markdown.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [May write output files under the user's home directory when an output path is provided.] <br>

## Skill Version(s): <br>
1.0.0 (source: server release metadata and artifact _meta.json) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
