## Description: <br>
Uses Playwright with stealth browser tooling to retrieve pages that block simple fetches or require JavaScript rendering. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[sdt328606](https://clawhub.ai/user/sdt328606) <br>

### License/Terms of Use: <br>
MIT-0 <br>


## Use Case: <br>
Developers and automation users use this skill when ordinary web fetch tools cannot retrieve content because a page requires JavaScript rendering or blocks simple requests. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: Stealth scraping can be misused against site rules or access controls. <br>
Mitigation: Use only where permitted, respect robots.txt and site terms, and do not use the skill to bypass access controls. <br>
Risk: Browser-session reuse can expose cookies, credentials, or logged-in account state. <br>
Mitigation: Run the skill in an isolated browser profile and do not attach it to a normal logged-in Chrome session. <br>
Risk: The shell execution based tool entry point needs review before installation. <br>
Mitigation: Fix or remove the execSync-based entry point and validate URL inputs before enabling the tool. <br>
Risk: Bundled Goofish-specific scripts narrow the skill behavior and include unsafe search examples. <br>
Mitigation: Remove the bundled Goofish scripts if only a general scraper is needed, and do not use the skill to search for cheating or fraud services. <br>


## Reference(s): <br>
- [ClawHub skill page](https://clawhub.ai/sdt328606/stitch-playwright-scraper) <br>


## Skill Output: <br>
**Output Type(s):** [Text, Code, Shell commands, Configuration guidance] <br>
**Output Format:** [Markdown guidance with JavaScript and shell command examples; tool output is plain text page content.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Requires local Playwright and Chromium setup before use.] <br>

## Skill Version(s): <br>
2.0.0 (source: server release metadata and SKILL.md frontmatter) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
