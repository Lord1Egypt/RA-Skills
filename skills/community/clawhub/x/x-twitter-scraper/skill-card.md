## Description: <br>
Scrapes public Twitter/X profiles and recent tweets using browser automation with anti-detection and optional profile discovery through Google or DuckDuckGo. <br>

This skill is ready for commercial/non-commercial use. <br>

## Publisher: <br>
[ArulmozhiV](https://clawhub.ai/user/ArulmozhiV) <br>

### License/Terms of Use: <br>


## Use Case: <br>
Developers and analysts use this skill to discover public Twitter/X accounts by location or category and scrape profile, recent tweet, engagement, and media metadata into structured outputs. Use should be limited to authorized, lawful collection of public data. <br>

### Deployment Geography for Use: <br>
Global <br>

## Known Risks and Mitigations: <br>
Risk: The skill is designed for social-media scraping with stealth and residential-proxy support, which can create legal, policy, or platform-terms risk. <br>
Mitigation: Confirm the scraping use case is authorized and lawful before installation or execution, and avoid large unsupervised scraping runs. <br>
Risk: The skill may collect and persist profile, tweet, engagement, and media data from public accounts. <br>
Mitigation: Store outputs only in approved locations, restrict access to exported data and thumbnails, and delete collected data when it is no longer needed. <br>
Risk: Proxy, search API, and scraper credentials may be needed for operation. <br>
Mitigation: Use restricted credentials with the minimum required permissions and inspect external code before running it. <br>


## Reference(s): <br>
- [ClawHub release page](https://clawhub.ai/ArulmozhiV/x-twitter-scraper) <br>
- [ScrapeClaw suite](https://www.scrapeclaw.cc/) <br>
- [Google Cloud Console](https://console.cloud.google.com/) <br>
- [Google Programmable Search Engine](https://programmablesearchengine.google.com/) <br>


## Skill Output: <br>
**Output Type(s):** [JSON, CSV, Files, Shell commands, Configuration] <br>
**Output Format:** [JSON and CSV data files with optional downloaded media thumbnails; Markdown documentation includes shell commands and configuration examples.] <br>
**Output Parameters:** [1D] <br>
**Other Properties Related to Output:** [Stores queue, scrape, export, and thumbnail files under the configured data and thumbnails directories.] <br>

## Skill Version(s): <br>
0.1.2 (source: server release metadata) <br>

## Ethical Considerations: <br>
Users should evaluate whether this skill is appropriate for their environment, review any generated or modified files before relying on them, and apply their organization's safety, security, and compliance requirements before deployment. <br>
